from django.shortcuts import render
from django.views.generic import TemplateView, ListView, DetailView, CreateView, UpdateView, DeleteView

# Create your views here.


def index(request):
    return render(request, "accounts/dashboard.html", {"data": "This is Data"})


# class PostsCreateView(CreateView):
#     form_class = PostForm

#     template_name = 'posts/post_create.html' # no default value

#     def get_success_url(self):
#         return reverse('posts-list')

#     # Optional: Overwrite form data (before save)
#     def form_valid(self, form):
#         if self.request.user.is_authenticated:
#             from.instance.author = self.request.user

#         return super().form_valid(form)
