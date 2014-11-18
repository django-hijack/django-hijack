from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import get_object_or_404
from django.http import HttpResponseBadRequest

from .models import get_user_model
from .helpers import login_user

@staff_member_required
def login_with_id(request, userId):
    if isinstance(userId, int):
        return HttpResponseBadRequest('userId must be an integer value.')
    user = get_object_or_404(get_user_model(), pk=userId)
    return login_user(request, user)

@staff_member_required
def login_with_email(request, email):
    user = get_object_or_404(get_user_model(), email=email)
    return login_user(request, user)

@staff_member_required
def login_with_username(request, username):
    user = get_object_or_404(get_user_model(), username=username)
    return login_user(request, user)
