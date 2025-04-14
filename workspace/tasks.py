# workspace/tasks.py

import logging
from django.core.mail import send_mail
from django.conf import settings
from django.utils import timezone
from datetime import timedelta
from django.contrib import messages
from .models import Chapter, Submission, Workspace
from users.models import User


def send_assignment_notification(request, workspace):
    """Notify student and mentor of workspace assignment."""
    subject = f"Workspace Assignment Notification"
    message = f"You've been assigned to {workspace.student.first_name}'s workspace ({workspace.title})."

    recipient_list = [workspace.student.email, workspace.mentor.email] if workspace.mentor else [workspace.student.email]


    try:
        send_mail(subject, message, settings.EMAIL_HOST_USER, recipient_list, fail_silently=False)
        messages.success(request, message, extra_tags="assignment")
    except Exception as e:
        logging.error(f"Failed to send assignment notification: {str(e)}")
        messages.error(request, "Failed to send assignment notification.", extra_tags="assignment")


def send_submission_notification(request, submission):
    """Notify mentor of a new student submission."""
    
    try:
        mentor_email = submission.chapter.workspace.mentor.email
        subject = f"New Submission for {submission.chapter.chapter_name}"
        message = (
            f"{submission.student.first_name} submitted draft {submission.draft_number} for {submission.chapter.chapter_name}."
        )
        send_mail(subject, message, settings.EMAIL_HOST_USER, [mentor_email], fail_silently=False)
        messages.success(request, message, extra_tags="submission")
    except Exception as e:
        logging.error(f"Failed to send submission notification: {str(e)}")
        messages.error(request, "Failed to send submission notification.", extra_tags="submission")


def _send_submission_notification(request, submission):
    """Helper function to send notifications on submission updates."""
    try:
        if submission.status == "approved":
            message = (
                f"Your submission (Draft {submission.draft_number}) for {submission.chapter.chapter_name} has been approved."
            )
        else:
            message = (
                f"Your submission (Draft {submission.draft_number}) for {submission.chapter.chapter_name} needs editing. Comment: {submission.comment or 'No comment provided.'}"
            )

        send_mail(
            f"Update on submission for {submission.chapter.chapter_name}",
            message,
            settings.EMAIL_HOST_USER,
            [submission.student.email],
            fail_silently=False,
        )
        messages.success(request, message, extra_tags="submission-update")

    except Exception as e:
        logging.error(f"Failed to send submission update notification: {str(e)}")
        messages.error(request, "Failed to send submission update notification.", extra_tags="submission-update")



def send_deadline_reminder(request, chapter):
    """Notify student of approaching chapter deadline."""
    try:
        if Submission.objects.filter(chapter=chapter, status="approved").exists():
            messages.info(request, f"No reminder sent for {chapter.chapter_name}; already submitted.", extra_tags="deadline-reminder")
            return
        student_email = chapter.workspace.student.email
        subject = f"Reminder: Deadline for {chapter.chapter_name}"
        message = (
            f"The deadline for chapter {chapter.chapter_name} is {chapter.deadline.strftime('%Y-%m-%d %H:%M')}. Please submit your work on time."
        )
        send_mail(subject, message, settings.EMAIL_HOST_USER, [student_email], fail_silently=False)
        messages.success(request, f"Deadline reminder sent for {chapter.chapter_name}.", extra_tags="deadline-reminder")
    except Exception as e:
        logging.error(f"Failed to send deadline reminder: {str(e)}")
        messages.error(request, "Failed to send deadline reminder.", extra_tags="deadline-reminder")

def send_forum_notification(request, forum, post_or_reply):
    """Notify forum participants (except creator) of new posts or replies."""
    if not post_or_reply:
        return
    
    is_reply = isinstance(post_or_reply, Reply)
    subject = (
        f"New Reply in {forum.title}" if is_reply else f"New Post in {forum.title}"
    )
    message = (
        f"{post_or_reply.created_by.first_name} added a {'reply' if is_reply else 'post'} "
        f"to '{forum.title}':\n\n{post_or_reply.content[:100]}{'...' if len(post_or_reply.content) > 100 else ''}\n\n"
    )
    
    recipients = [
        user.email for user in forum.participants.all()
        if user != post_or_reply.created_by and user.email
    ]
    
    if not recipients:
        messages.info(request, f"No notification sent; no other participants in {forum.title}.", extra_tags="forum")
        return
    
    try:
        send_mail(subject, message, settings.EMAIL_HOST_USER, recipients, fail_silently=False)
        messages.info(request, f'Notification sent for new activity in forum {forum.title}.')
    except Exception as e:
        logging.error(f"Failed to send forum notification: {str(e)}")
        messages.error(request, "Failed to send forum notification.", extra_tags="forum")