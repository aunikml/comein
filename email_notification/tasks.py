from django.core.mail import send_mail
from django.conf import settings
from django.utils import timezone
from datetime import timedelta

def send_assignment_notification(workspace):
    subject = f'You have been assigned to a Workspace'
    message = f'You have been assigned to the workspace for {workspace.student.first_name}.'
    send_mail(subject, message, settings.EMAIL_HOST_USER, [workspace.student.email, workspace.mentor.email], fail_silently=False)

def send_submission_notification(submission):
    subject = f'New submission for chapter {submission.chapter.chapter_name}'
    message = f'A new submission (Draft {submission.draft_number}) has been made by {submission.student.first_name} for chapter {submission.chapter.chapter_name}.'
    send_mail(subject, message, settings.EMAIL_HOST_USER, [submission.chapter.workspace.mentor.email], fail_silently=False)

def send_submission_update_notification(submission):
    subject = f'Update on submission for chapter {submission.chapter.chapter_name}'
    if submission.status == 'approved':
        message = f'Your submission (Draft {submission.draft_number}) for chapter {submission.chapter.chapter_name} has been approved.'
    else:
        message = f'Your submission (Draft {submission.draft_number}) for chapter {submission.chapter.chapter_name} needs editing. Comment: {submission.comment}'
    send_mail(subject, message, settings.EMAIL_HOST_USER, [submission.student.email], fail_silently=False)

def send_deadline_reminder():
    from workspace.models import Chapter, Submission  # Import here to avoid circular dependency
    impending_deadline = timezone.now() + timedelta(days=1)
    chapters = Chapter.objects.filter(deadline__lte=impending_deadline)
    
    for chapter in chapters:
        submissions = Submission.objects.filter(chapter=chapter, status__in=['pending', 'needs_editing'])
        if submissions.exists():
            student_email = chapter.workspace.student.email
            subject = f'Reminder: Deadline for chapter {chapter.chapter_name} is approaching'
            message = f'The deadline for chapter {chapter.chapter_name} is {chapter.deadline.strftime("%Y-%m-%d %H:%M")}. Please submit your work on time.'
            send_mail(subject, message, settings.EMAIL_HOST_USER, [student_email], fail_silently=False)