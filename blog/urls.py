from django.urls import path
import blog.views.blog_views as blog_views
import blog.views.comment_views as comment_views
app_name = "blogs"

urlpatterns = [
    path("", blog_views.BlogIndex.as_view(), name="blog-index"),
    path("<int:pk>/", blog_views.BlogDetailView.as_view(), name="blog-detail"),
    path("create/", blog_views.BlogCreateView.as_view(), name="blog-create"),
    path("<int:pk>/edit/", blog_views.BlogUpdateView.as_view(), name="blog-edit"),
    path("<int:pk>/delete/", blog_views.BlogDeleteView.as_view(), name="blog-delete"),
    path("comment/<int:pk>/edit/", comment_views.CommentUpdateView.as_view(), name="comment-edit"),
    path("comment/<int:pk>/delete/", comment_views.CommentDeleteView.as_view(), name="comment-delete"),
]
