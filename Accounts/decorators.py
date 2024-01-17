from django.http import HttpResponse
from django.shortcuts import redirect
from django.conf import settings
import base64


def unauthenticated_user(view_func):
    def wrapper_func(request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect("home")
        else:
            return view_func(request, *args, **kwargs)

    return wrapper_func


def allowed_users(allowed_roles=[]):
    def decorator(view_func):
        def wrapper_func(request, *args, **kwargs):
            if request.user.groups.exists():
                flag = False
                for group_name in request.user.groups.all():
                    for allowed_roles_name in allowed_roles:
                        if group_name.name == allowed_roles_name:
                            flag = True
                            break
                    if flag:
                        break
                if flag:
                    return view_func(request, *args, **kwargs)
                else:
                    image_path = (
                        settings.BASE_DIR / "static/images/forbidden_with_text.png"
                    )
                    with open(image_path, "rb") as f:
                        image_data = f.read()
                        content_type = "image/png"
                        # image_data = base64.b64encode(
                        #     f.read()).decode('utf-8')

                    return HttpResponse(image_data, content_type=content_type)
                    # return HttpResponse(
                    #     f'<div style="text-align:center; padding: 150px 0;"><div><img src="{image_data}" style="width:24px;height:24px;" alt="JG"></div><h4>You are not allowed to view this page.<br> Your user role is: {group_name.name}</h4></div>', content_type=content_type)
            else:
                return HttpResponse(
                    f'<div style="text-align:center; padding: 150px 0;"><h4>You are not allowed to view this page.</h4></div>'
                )

        return wrapper_func

    return decorator


def admin_only(view_func):
    def wrapper_function(request, *args, **kwargs):
        group = None
        if request.user.groups.exists():
            group = request.user.groups.all()[0].name
        if group == "User":
            return redirect("user-page")
        if group == "Admin":
            return view_func(request, *args, **kwargs)

    return wrapper_function
