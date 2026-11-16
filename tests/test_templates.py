from django.template.loader import render_to_string


def test_notification_template(rf, bob):
    request = rf.get("/")
    request.user = bob

    html = render_to_string("hijack/notification.html", {"request": request})

    assert "<dialog" in html
    assert " open" in html
    assert 'formmethod="dialog"' in html
    assert "onclick" not in html
