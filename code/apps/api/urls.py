from django.contrib.auth import REDIRECT_FIELD_NAME
from django.contrib.auth.decorators import user_passes_test
from ninja import NinjaAPI

from apps.eventManager.api import router as EventRouter


def superuser_required(
    view_func=None, redirect_field_name=REDIRECT_FIELD_NAME, login_url="/"
):
    actual_decorator = user_passes_test(
        lambda u: u.is_active and u.is_superuser,
        login_url=login_url,
        redirect_field_name=redirect_field_name,
    )
    if view_func:
        return actual_decorator(view_func)
    return actual_decorator


api = NinjaAPI(
    csrf=False,
    docs_url="/docs",
    title="mziuri API",
    docs_decorator=superuser_required,
)


api.add_router("/eventManager/", EventRouter, tags=["Events"])
