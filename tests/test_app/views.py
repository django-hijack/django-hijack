from django.contrib.auth import get_user_model
from django.http import HttpResponse, JsonResponse
from django.views import generic


class UserListView(generic.ListView):
    model = get_user_model()
    template_name = "user_list.html"


class UserDetailView(generic.View):
    def get(self, request, *args, **kwargs):
        return JsonResponse({"username": request.user.username})


class SessionOnlyView(generic.View):
    def get(self, request, *args, **kwargs):
        request.session["cart"] = [1]
        return HttpResponse("<html><body>ok</body></html>")
