from django.middleware.csrf import get_token
from django.template.loader import render_to_string
from django.utils.translation import gettext_lazy as _


class HijackUserAdminMixin:
    def get_hijack_user(self, obj):
        return obj

    def get_changelist_instance(self, request):
        def hijack_field(obj):
            user = self.get_hijack_user(obj)
            return render_to_string(
                "hijack/contrib/admin/button.html",
                {
                    "request": request,
                    "csrf_token": get_token(request),
                    "another_user": user,
                },
            )

        hijack_field.short_description = _("hijack user")

        list_display = self.get_list_display(request)
        list_display_links = self.get_list_display_links(request, list_display)
        # Add the action checkboxes if any actions are available.
        if self.get_actions(request):
            list_display = ["action_checkbox", *list_display, hijack_field]
        sortable_by = self.get_sortable_by(request)
        ChangeList = self.get_changelist(request)
        return ChangeList(
            request,
            self.model,
            list_display,
            list_display_links,
            self.get_list_filter(request),
            self.date_hierarchy,
            self.get_search_fields(request),
            self.get_list_select_related(request),
            self.list_per_page,
            self.list_max_show_all,
            self.list_editable,
            self,
            sortable_by,
        )
