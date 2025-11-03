from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from accounts.services.user_display_name import get_user_display_name
from django.core.paginator import Paginator
from blog.models.blog_model import Blog
from django.http import JsonResponse
from django.template.loader import render_to_string


@login_required
def greet_view(request):
    """
    Muestra 'Hola, <nombre>' y un feed paginado de blogs.
    """
    display_name = get_user_display_name(request.user)

    # paginación simple (6 por página)
    page = request.GET.get('page', 1)
    qs = Blog.objects.all().order_by('-created_at').only('id', 'title', 'created_at', 'author')
    paginator = Paginator(qs, 6)
    page_obj = paginator.get_page(page)

    return render(request, "accounts/greet.html", {"display_name": display_name, "blogs": page_obj})


@login_required
def greet_posts_view(request):
    """Endpoint que devuelve el HTML parcial de posts para una página dada (usado por scroll infinito)."""
    page = request.GET.get('page', 1)
    qs = Blog.objects.all().order_by('-created_at').only('id', 'title', 'created_at', 'author')
    paginator = Paginator(qs, 6)
    page_obj = paginator.get_page(page)

    html = render_to_string('accounts/_post_list.html', {'blogs': page_obj})
    data = {
        'html': html,
        'has_next': page_obj.has_next(),
        'next_page': page_obj.next_page_number() if page_obj.has_next() else None,
    }
    return JsonResponse(data)
