from django.urls import path
import blog.views.blog_views as blog_views

app_name = "blogs"

urlpatterns = [
    path("", blog_views.BlogIndex.as_view(), name="blog-index"),
    path("<int:pk>/", blog_views.BlogDetailView.as_view(), name="blog-detail"),
    path("create/", blog_views.BlogCreateView.as_view(), name="blog-create"),
    path("<int:pk>/update/", blog_views.BlogUpdateView.as_view(), name="blog-update"),
    path("<int:pk>/delete/", blog_views.BlogDeleteView.as_view(), name="blog-delete"),
]
