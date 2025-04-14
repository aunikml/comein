# from django.core.mail import send_mail
# from django.conf import settings
# from django.utils import timezone
# from django.contrib import messages
# from discussion_forum.models import Post, Reply, Forum
# from workspace.models import Chapter, Submission, Workspace
# from users.models import User
# import logging

# # Set up logging
# logger = logging.getLogger(__name__)

# def send_assignment_notification(request, workspace):
#     """Notify student and mentor of workspace assignment."""
#     subject = f"Workspace Assignment Notification"
#     message = f"You have been assigned to {workspace.student.first_name}'s workspace ({workspace.title})."
    
#     recipient_list = [workspace.student.email]
#     if workspace.mentor:
#         recipient_list.append(workspace.mentor.email)
    
#     try:
#         send_mail(
#             subject,
#             message,
#             settings.EMAIL_HOST_USER,
#             recipient_list,
#             fail_silently=False,
#         )
#         messages.success(request, "Assignment notification sent successfully.", extra_tags="assignment")
#     except Exception as e:
#         logger.error(f"Failed to send assignment notification: {str(e)}")
#         messages.error(request, "Failed to send assignment notification.", extra_tags="assignment")

# def send_submission_notification(request, submission):
#     """Notify mentor of a new student submission."""
#     if not submission.chapter.workspace.mentor:
#         messages.warning(request, "No mentor assigned to this workspace.", extra_tags="submission")
#         return
    
#     subject = f"New Submission for {submission.chapter.chapter_name}"
#     message = (
#         f"{submission.student.first_name} submitted draft {submission.draft_number} "
#         f"for {submission.chapter.chapter_name}. "
#         f"View it at: {request.build_absolute_uri(submission.get_absolute_url())}"
#     )
    
#     try:
#         send_mail(
#             subject,
#             message,
#             settings.EMAIL_HOST_USER,
#             [submission.chapter.workspace.mentor.email],
#             fail_silently=False,
#         )
#         messages.success(request, "Submission notification sent to mentor.", extra_tags="submission")
#     except Exception as e:
#         logger.error(f"Failed to send submission notification: {str(e)}")
#         messages.error(request, "Failed to send submission notification.", extra_tags="submission")

# def send_submission_update_notification(request, submission):
#     """Notify student of mentor's action on their submission."""
#     subject = f"Submission Update for {submission.chapter.chapter_name}"
#     if submission.status == "approved":
#         message = (
#             f"Your submission (Draft {submission.draft_number}) for {submission.chapter.chapter_name} "
#             f"has been approved by your mentor."
#         )
#     else:
#         message = (
#             f"Your submission (Draft {submission.draft_number}) for {submission.chapter.chapter_name} "
#             f"needs editing. Mentor comment: {submission.comment or 'No comment provided.'}"
#         )
    
#     try:
#         send_mail(
#             subject,
#             message,
#             settings.EMAIL_HOST_USER,
#             [submission.student.email],
#             fail_silently=False,
#         )
#         messages.success(request, "Submission update notification sent to student.", extra_tags="submission-update")
        
#         # Optional: Notify mentor of their own action for confirmation
#         if submission.chapter.workspace.mentor:
#             mentor_message = (
#                 f"You updated {submission.student.first_name}'s submission "
#                 f"(Draft {submission.draft_number}) for {submission.chapter.chapter_name} "
#                 f"to '{submission.status}'."
#             )
#             send_mail(
#                 subject,
#                 mentor_message,
#                 settings.EMAIL_HOST_USER,
#                 [submission.chapter.workspace.mentor.email],
#                 fail_silently=False,
#             )
#     except Exception as e:
#         logger.error(f"Failed to send submission update notification: {str(e)}")
#         messages.error(request, "Failed to send submission update notification.", extra_tags="submission-update")

# def send_deadline_reminder(request, chapter):
#     """Notify student of approaching chapter deadline."""
#     if Submission.objects.filter(chapter=chapter, status="approved").exists():
#         messages.info(request, f"No reminder sent for {chapter.chapter_name}; already submitted.", extra_tags="deadline-reminder")
#         return
    
#     subject = f"Reminder: Deadline for {chapter.chapter_name}"
#     message = (
#         f"The deadline for chapter {chapter.chapter_name} is {chapter.deadline.strftime('%Y-%m-%d %H:%M')}. "
#         f"Please submit your work on time."
#     )
    
#     try:
#         send_mail(
#             subject,
#             message,
#             settings.EMAIL_HOST_USER,
#             [chapter.workspace.student.email],
#             fail_silently=False,
#         )
#         messages.success(request, f"Deadline reminder sent for {chapter.chapter_name}.", extra_tags="deadline-reminder")
#     except Exception as e:
#         logger.error(f"Failed to send deadline reminder: {str(e)}")
#         messages.error(request, "Failed to send deadline reminder.", extra_tags="deadline-reminder")

# def send_forum_notification(request, forum, post_or_reply):
#     """Notify forum participants (except creator) of new posts or replies."""
#     is_reply = isinstance(post_or_reply, Reply)
#     subject = (
#         f"New Reply in {forum.title}" if is_reply else f"New Post in {forum.title}"
#     )
#     message = (
#         f"{post_or_reply.created_by.first_name} added a {'reply' if is_reply else 'post'} "
#         f"to '{forum.title}':\n\n{post_or_reply.content[:100]}{'...' if len(post_or_reply.content) > 100 else ''}\n\n"
#         f"View it at: {request.build_absolute_uri(post_or_reply.get_absolute_url())}"
#     )
    
#     recipients = [
#         user.email for user in forum.participants.all()
#         if user != post_or_reply.created_by and user.email
#     ]
    
#     if not recipients:
#         messages.info(request, f"No notification sent; no other participants in {forum.title}.", extra_tags="forum")
#         return
    
#     try:
#         send_mail(
#             subject,
#             message,
#             settings.EMAIL_HOST_USER,
#             recipients,
#             fail_silently=False,
#         )
#         messages.success(request, f"Forum notification sent for {forum.title}.", extra_tags="forum")
#     except Exception as e:
#         logger.error(f"Failed to send forum notification: {str(e)}")
#         messages.error(request, "Failed to send forum notification.", extra_tags="forum")