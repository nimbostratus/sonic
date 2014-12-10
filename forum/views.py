from django.views.generic import ListView
from forum.models import Post, Category, Board, Topic


class HomeView(ListView):
    model = Category

class BoardView(ListView):
    model = Topic

    def get_queryset(self):
        return Board.objects.get(id=int(self.kwargs['id'])).topic_set.all()

    def get_context_data(self, **kwargs):
        context = super(BoardView, self).get_context_data(**kwargs)
        context.update({
            'board': Board.objects.get(id=int(self.kwargs['id']))
        })
        return context

class ThreadView(ListView):
    model = Post
    paginate_by = 20

