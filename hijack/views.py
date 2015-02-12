from django.contrib.admin.views.decorators import staff_member_required


from django.contrib.auth.decorators import login_required


from django.shortcuts import get_object_or_404
from django.http import HttpResponseBadRequest, HttpResponseRedirect


from hijack.helpers import login_user
from hijack.helpers import release_hijack as release_hijack_fx
from compat import get_user_model

@staff_member_required
def login_with_id(request, userId):
    # input(userId) is unicode
    try:
        userId = int(userId)
    except:
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


@login_required
def release_hijack(request):
    return release_hijack_fx(request)

@login_required
def disable_hijack_warning(request):
    request.session['is_hijacked_user']=False
    return HttpResponseRedirect(request.GET.get('next','/'))
