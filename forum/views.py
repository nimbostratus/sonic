from django.views.generic import ListView
from forum.models import Post


class HomeView(ListView):
    model = Post

