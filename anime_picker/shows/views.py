from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.views.decorators.http import require_POST

from .forms import QuickAddForm, ShowForm
from .models import Show


def home(request):
    context = {
        "watching_count": Show.objects.filter(status=Show.Status.WATCHING).count(),
        "planned_count": Show.objects.filter(status=Show.Status.PLANNING).count(),
        "done_count": Show.objects.filter(status=Show.Status.WATCHED).count(),
        "recent": Show.objects.all()[:5],
        "quick_form": QuickAddForm(),
    }
    return render(request, "shows/home.html", context)


@require_POST
def quick_add(request):
    form = QuickAddForm(request.POST)
    if form.is_valid():
        form.save()
    return redirect("home")


def add_show(request):
    if request.method == "POST":
        form = ShowForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("home")
    else:
        form = ShowForm()
    return render(request, "shows/add.html", {"form": form})


def pick(request):
    """Return one random show as JSON.

    ?mode=surprise  any show
    ?mode=continue  something you're currently watching
    ?mode=new       something you're planning to watch
    ?exclude=<id>   don't return this one (for "Find Another World")
    """
    mode = request.GET.get("mode", "surprise")
    qs = Show.objects.all()
    if mode == "continue":
        qs = qs.filter(status=Show.Status.WATCHING)
    elif mode == "new":
        qs = qs.filter(status=Show.Status.PLANNING)

    exclude = request.GET.get("exclude", "")
    if exclude.isdigit():
        remaining = qs.exclude(pk=int(exclude))
        # If excluding leaves nothing, fall back to the full set.
        qs = remaining if remaining.exists() else qs

    show = qs.order_by("?").first()
    if show is None:
        return JsonResponse({"found": False})
    return JsonResponse(
        {
            "found": True,
            "id": show.pk,
            "name": show.name,
            "type": show.media_type,
            "genre": show.genre,
            "status": show.status,
        }
    )
