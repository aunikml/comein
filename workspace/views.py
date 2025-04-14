from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Workspace, Resource, Chapter, Submission
from .forms import ResourceForm, ChapterForm, SubmissionForm, SubmissionReviewForm
from django.http import Http404
from django.db import IntegrityError, transaction
from .tasks import _send_submission_notification


@login_required
def workspace_view(request, student_id):
    try:
        workspace = Workspace.objects.get(student__id=student_id)
    except Workspace.DoesNotExist:
        raise Http404("Workspace does not exist.")

    is_mentor = workspace.mentor == request.user or request.user.is_superuser
    
    if not is_mentor and workspace.student != request.user:
        raise Http404("You do not have permission to view this workspace.")

    resources = workspace.resources.all()
    chapters = workspace.chapters.all()

    chapter_submissions = {}
    chapter_progress = {}

    for chapter in chapters:
        submissions = chapter.submissions.filter(student=workspace.student).order_by('-submission_date')
        chapter_submissions[chapter.id] = submissions

        approved_submissions = chapter.submissions.filter(student=workspace.student, status='approved')
        progress_percentage = 0
        if submissions.count() > 0:
            progress_percentage = (approved_submissions.count() / submissions.count()) * 100
        chapter_progress[chapter.id] = {
            'progress_percentage': progress_percentage,
            'is_completed': approved_submissions.exists(),
        }

    if request.method == 'POST':
        # Handle form submissions (resource/chapter)
        if 'add_resource' in request.POST:
            form = ResourceForm(request.POST, request.FILES)
            if form.is_valid():
                resource = form.save(commit=False)
                resource.workspace = workspace
                resource.save()
                return redirect('workspace_view', student_id=student_id)

        elif 'add_chapter' in request.POST:
            form = ChapterForm(request.POST)
            if form.is_valid():
                try:
                    with transaction.atomic():  # Crucial!
                        chapter = form.save(commit=False)
                        chapter.workspace = workspace
                        chapter.save()
                    return redirect('workspace_view', student_id=student_id)
                except IntegrityError as e:
                    context['errors'] = str(e)
                    return render(request, 'workspace/workspace_page.html', context)


    context = {
        'workspace': workspace,
        'resources': resources,
        'chapters': chapters,
        'chapter_progress': chapter_progress,
        'chapter_submissions': chapter_submissions,
        'resource_form': ResourceForm(),
        'chapter_form': ChapterForm(),
        'is_mentor': is_mentor,
    }

    return render(request, 'workspace/workspace_page.html', context)



@login_required
def submit_chapter(request, chapter_id):
    chapter = get_object_or_404(Chapter, id=chapter_id)
    workspace = chapter.workspace
    is_mentor = workspace.mentor == request.user or request.user.is_superuser
    if workspace.student != request.user and not is_mentor:
        raise Http404("You do not have permission to view this page")

    submission_form = SubmissionForm()
    if request.method == "POST":
        submission_form = SubmissionForm(request.POST, request.FILES)
        if submission_form.is_valid():
            new_submission = submission_form.save(commit=False)
            new_submission.chapter = chapter
            new_submission.student = request.user
            new_submission.save()
            return redirect('workspace_view', student_id=workspace.student.id)

    submissions = chapter.submissions.filter(student=request.user).order_by('-submission_date')
    return render(request, 'workspace/submission.html', {'chapter': chapter, 'submission_form': submission_form, 'submissions': submissions, 'is_mentor': is_mentor})


@login_required
def review_submission(request, submission_id):
    submission = get_object_or_404(Submission, id=submission_id)
    workspace = submission.chapter.workspace

    if workspace.mentor != request.user and not request.user.is_superuser:
        raise Http404("You do not have permission to review this submission.")

    if request.method == 'POST':
        review_form = SubmissionReviewForm(request.POST, request.FILES, instance=submission)
        if review_form.is_valid():
            review_form.save()
            _send_submission_notification(request, submission)
            return redirect('workspace_view', student_id=workspace.student.id)
    else:
        review_form = SubmissionReviewForm(instance=submission)

    return render(request, 'workspace/review_submission.html', {'review_form': review_form, 'submission': submission})

@login_required
def edit_chapter(request, chapter_id):
    chapter = get_object_or_404(Chapter, id=chapter_id)
    workspace = chapter.workspace

    if not request.user.is_superuser and workspace.mentor != request.user:
        raise Http404("You do not have permission to edit this chapter.")

    if request.method == 'POST':
        form = ChapterForm(request.POST, instance=chapter)
        if form.is_valid():
            try:
                with transaction.atomic():
                    form.save()
                    return redirect('workspace_view', student_id=workspace.student.id)
            except ValidationError as e:
                # Pass errors to the template for display
                return render(
                    request,
                    'workspace/edit_chapter.html',
                    {
                        'form': form,
                        'chapter': chapter,
                        'workspace': workspace,
                        'errors': e.error_dict,
                    },
                )
    else:
        form = ChapterForm(instance=chapter)

    context = {'form': form, 'chapter': chapter, 'workspace': workspace}
    return render(request, 'workspace/edit_chapter.html', context)


@login_required
def delete_chapter(request, chapter_id):
    chapter = get_object_or_404(Chapter, id=chapter_id)
    workspace = chapter.workspace
    if not request.user.is_superuser and workspace.mentor != request.user:
        raise Http404("You do not have permission to delete this chapter.")

    if request.method == 'POST':
        try:
            with transaction.atomic():
                chapter.delete()
                return redirect('workspace_view', student_id=workspace.student.id)
        except Exception as e:
            #Handle potential errors during deletion
            return render(request, 'workspace/delete_chapter.html', {'chapter': chapter, 'errors': str(e)}) #pass the error message to template

    return render(request, 'workspace/delete_chapter.html', {'chapter': chapter, 'workspace': workspace})

@login_required
def edit_resource(request, resource_id):
    resource = get_object_or_404(Resource, id=resource_id)
    workspace = resource.workspace
    if not request.user.is_superuser and workspace.mentor != request.user:
        raise Http404("You do not have permission to edit this resource.")
    
    if request.method == 'POST':
        form = ResourceForm(request.POST, request.FILES, instance=resource)
        if form.is_valid():
            form.save()
            return redirect('workspace_view', student_id=workspace.student.id)
    else:
        form = ResourceForm(instance=resource)

    return render(request, 'workspace/edit_resource.html', {'form': form, 'resource': resource, 'workspace': workspace})


@login_required
def delete_resource(request, resource_id):
    resource = get_object_or_404(Resource, id=resource_id)
    workspace = resource.workspace

    if not request.user.is_superuser and workspace.mentor != request.user:
        raise Http404("You do not have permission to delete this resource.")
        
    if request.method == 'POST':
        resource.delete()
        return redirect('workspace_view', student_id=workspace.student.id)
    return render(request, 'workspace/delete_resource.html', {'resource': resource})