from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model, update_session_auth_hash
from .forms import UserProfileForm
from .models import UserProfile
from workspace.models import Workspace, Chapter, Submission
from forum.models import Forum
from django.http import Http404
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib import messages
from scheduler.forms import CalendlyLinkForm

@login_required
def profile_edit(request):
    User = get_user_model()  # Get the custom user model

    # Debugging to ensure `request.user` is an instance of the custom User model
    if not isinstance(request.user, User):
        raise ValueError(f"Invalid user object: {request.user} ({type(request.user)})")

    # Ensure the profile exists or create one
    profile, created = UserProfile.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('profile_view')  # Redirect to profile view
    else:
        form = UserProfileForm(instance=profile)

    return render(request, 'users/profile_edit.html', {'form': form})

@login_required
def profile_view(request):
    User = get_user_model()  # Get the custom user model
    profile = None
    is_own_profile = False # Initialize to False

    # Check if a student_id was passed in the query parameters
    student_id = request.GET.get('student_id')
    if student_id:
        try:
            # Get the student's user object
            student_user = User.objects.get(pk=student_id)
            # Get or create the student's profile
            profile, created = UserProfile.objects.get_or_create(user=student_user)
        except User.DoesNotExist:
            # Handle the case where the student or profile doesn't exist
            raise Http404("Student not found")
    else:
        # Show the current user's profile
        if not isinstance(request.user, User):
            raise ValueError(f"Invalid user object: {request.user} ({type(request.user)})")
        profile, created = UserProfile.objects.get_or_create(user=request.user)
        is_own_profile = True  # Set to True when viewing own profile

    return render(request, 'users/profile_view.html', {'profile': profile, 'is_own_profile': is_own_profile})

@login_required
def dashboard(request):
    student_workspace_progress = {}
    mentor_workspaces_progress = {}
    mentor_profile = None
    calendly_form = None

    if hasattr(request.user, 'workspace') and request.user.workspace:
        for chapter in request.user.workspace.chapters.all():
            submissions = chapter.submissions.filter(student=request.user)
            approved_submissions = submissions.filter(status='approved')
            progress_percentage = 100 if approved_submissions.exists() else 0
            student_workspace_progress[chapter.id] = {
                'progress_percentage': progress_percentage,
                'is_completed': approved_submissions.exists(),
                'status_text': f'{approved_submissions.count()} draft{"s" if approved_submissions.count() != 1 else ""} approved' if approved_submissions.exists() else 'No drafts approved'
            }

    if hasattr(request.user, 'mentored_workspaces') and request.user.mentored_workspaces.all():
        for workspace in request.user.mentored_workspaces.all():
            mentor_workspaces_progress[workspace.id] = {}
            for chapter in workspace.chapters.all():
                submissions = chapter.submissions.filter(student=workspace.student)
                approved_submissions = submissions.filter(status='approved')
                progress_percentage = 100 if approved_submissions.exists() else 0
                mentor_workspaces_progress[workspace.id][chapter.id] = {
                    'progress_percentage': progress_percentage,
                    'is_completed': approved_submissions.exists(),
                    'status_text': f'{approved_submissions.count()} draft{"s" if approved_submissions.count() != 1 else ""} approved' if approved_submissions.exists() else 'No drafts approved'
                }
            # Get mentor's profile for mentored workspace
            if workspace.mentor == request.user:
                mentor_profile = UserProfile.objects.get(user=workspace.mentor)

    # Get the forums the user is participating in
    user_forums = Forum.objects.filter(participants=request.user)

    # Initialize Calendly form for mentors
    if request.user.user_type == 'mentor':
        profile, _ = UserProfile.objects.get_or_create(user=request.user)
        calendly_form = CalendlyLinkForm(instance=profile)

    context = {
        'student_workspace_progress': student_workspace_progress,
        'mentor_workspaces_progress': mentor_workspaces_progress,
        'user_forums': user_forums,
        'mentor_profile': mentor_profile,
        'calendly_form': calendly_form,
    }

    return render(request, 'users/dashboard.html', context)

@login_required
def password_change(request):
    User = get_user_model()
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important, to keep the user logged in
            request.user.password_changed = True
            request.user.save()
            return redirect('dashboard')  # Redirect to some success page
        else:
            print("Form Errors:", form.errors)
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'registration/password_change_form.html', {'form': form})