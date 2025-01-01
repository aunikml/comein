from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Workspace, Resource, Chapter, Submission
from .forms import ResourceForm, ChapterForm, SubmissionForm, SubmissionReviewForm
from django.http import Http404

@login_required
def workspace_view(request, student_id):
    try:
       workspace = Workspace.objects.get(student__id=student_id)
    except Workspace.DoesNotExist:
        raise Http404("Workspace does not exist.")
    
    is_mentor = workspace.mentor == request.user or request.user.is_superuser
    
    resource_form = ResourceForm()
    chapter_form = ChapterForm()

    if request.method == 'POST':
        if 'add_resource' in request.POST and is_mentor:
           resource_form = ResourceForm(request.POST, request.FILES)
           if resource_form.is_valid():
                new_resource = resource_form.save(commit=False)
                new_resource.workspace = workspace
                new_resource.save()
                return redirect('workspace_view', student_id=student_id)
        elif 'add_chapter' in request.POST and is_mentor:
          chapter_form = ChapterForm(request.POST)
          if chapter_form.is_valid():
              new_chapter = chapter_form.save(commit=False)
              new_chapter.workspace = workspace
              new_chapter.save()
              return redirect('workspace_view', student_id=student_id)

    resources = workspace.resources.all()
    chapters = workspace.chapters.all()

    chapter_submissions = {}
    for chapter in chapters:
        chapter_submissions[chapter.id] = chapter.submissions.filter(student=request.user)
    
    chapter_progress = {}
    for chapter in chapters:
         approved_submissions = chapter.submissions.filter(student=workspace.student, status='approved')
         submissions = chapter.submissions.filter(student=workspace.student)
         progress_percentage = 0
         if submissions.count() > 0 :
            progress_percentage = (approved_submissions.count() / submissions.count()) * 100
         chapter_progress[chapter.id] = {
              'progress_percentage': progress_percentage,
              'is_completed': approved_submissions.exists(),
          }
    
    context = {
        'workspace': workspace,
        'resources': resources,
        'chapters': chapters,
        'chapter_progress': chapter_progress,
        'chapter_submissions': chapter_submissions,
        'resource_form':resource_form,
        'chapter_form':chapter_form,
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
        raise Http404("You do not have permission to view this page")

    if request.method == 'POST':
        review_form = SubmissionReviewForm(request.POST, request.FILES, instance=submission)
        if review_form.is_valid():
            review_form.save()
            return redirect('workspace_view', student_id=workspace.student.id)
    else:
        review_form = SubmissionReviewForm(instance=submission)

    return render(request, 'workspace/review_submission.html', {'review_form': review_form, 'submission': submission})