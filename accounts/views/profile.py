from django.contrib.auth.decorators import login_required
from django.shortcuts import render


@login_required
def profile_view(request):
    """Simple profile page for the current user."""
    user = request.user
    return render(request, "accounts/profile.html", {"user": user})
