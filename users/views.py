from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from .forms import UserProfileForm
from .models import UserProfile
from workspace.models import Workspace

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
    profile = None  # Default value
    is_own_profile = False

    # Check if a student_id was passed in the query parameters
    student_id = request.GET.get('student_id')

    if student_id:  # Viewing a student's profile (for mentors)
        try:
            # Get the student's user object
            student_user = User.objects.get(pk=student_id)
            # Get or create the student's profile
            profile, created = UserProfile.objects.get_or_create(user=student_user)
        except User.DoesNotExist:
            # Handle the case where the student or profile doesn't exist
            raise Http404("Student not found")

    else:  # Viewing own profile
        # Show the current user's profile
        if not isinstance(request.user, User):
            raise ValueError(f"Invalid user object: {request.user} ({type(request.user)})")
        profile, created = UserProfile.objects.get_or_create(user=request.user)
        is_own_profile = True

    return render(request, 'users/profile_view.html', {'profile': profile, 'is_own_profile': is_own_profile})

@login_required
def dashboard(request):
    student_workspace_progress = {}
    mentor_workspaces_progress = {}

    if hasattr(request.user, 'workspace') and request.user.workspace:
        for chapter in request.user.workspace.chapters.all():
            approved_submissions = chapter.submissions.filter(student=request.user, status='approved')
            submissions = chapter.submissions.filter(student=request.user)
            progress_percentage = 0
            if submissions.count() > 0 :
                progress_percentage = (approved_submissions.count() / submissions.count()) * 100
            student_workspace_progress[chapter.id] = {
              'progress_percentage': progress_percentage,
              'is_completed': approved_submissions.exists(),
            }

    if hasattr(request.user, 'mentored_workspaces') and request.user.mentored_workspaces.all():
        for workspace in request.user.mentored_workspaces.all():
              mentor_workspaces_progress[workspace.id] = {}
              for chapter in workspace.chapters.all():
                  approved_submissions = chapter.submissions.filter(student=workspace.student, status='approved')
                  submissions = chapter.submissions.filter(student=workspace.student)
                  progress_percentage = 0
                  if submissions.count() > 0 :
                        progress_percentage = (approved_submissions.count() / submissions.count()) * 100
                  mentor_workspaces_progress[workspace.id][chapter.id] = {
                        'progress_percentage': progress_percentage,
                        'is_completed': approved_submissions.exists(),
                    }

    context = {
      'student_workspace_progress': student_workspace_progress,
      'mentor_workspaces_progress': mentor_workspaces_progress,
    }

    return render(request, 'users/dashboard.html', context)