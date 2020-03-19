from functools import wraps

from django.shortcuts import redirect


def institution_required(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if "institution_id" in request.session:
            return view_func(request, *args, **kwargs)
        else:
            return redirect("select_institution")
    return _wrapped_view
