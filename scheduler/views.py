from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import CalendlyLinkForm
from users.models import UserProfile

def mentor_required(view_func):
    def wrapper(request, *args, **kwargs):
        if request.user.user_type != 'mentor':
            messages.error(request, "Only mentors can perform this action.")
            return redirect('dashboard')
        return view_func(request, *args, **kwargs)
    return wrapper

@login_required
@mentor_required
def update_calendly_link(request):
    profile = UserProfile.objects.get(user=request.user)
    if request.method == 'POST':
        form = CalendlyLinkForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, "Calendly link updated successfully.")
            return redirect('dashboard')
    else:
        form = CalendlyLinkForm(instance=profile)
    return redirect('dashboard')  # Fallback, form handled in template