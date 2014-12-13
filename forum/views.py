from django.views.generic import ListView
from forum.models import Post, Category, Board, Topic


class HomeView(ListView):
    model = Category


class BoardView(ListView):
    def get_queryset(self):
        return Board.objects.get(id=int(self.kwargs['id'])).topic_set.all()

    def get_context_data(self, **kwargs):
        context = super(BoardView, self).get_context_data(**kwargs)
        context.update({
            'board': Board.objects.get(id=int(self.kwargs['id']))
        })
        return context

class TopicView(ListView):
    model = Post
    paginate_by = 20

    def get_queryset(self):
        return Post.objects.filter(topic__id=int(self.kwargs['topic_id']))


    def get_context_data(self, **kwargs):
        context = super(TopicView, self).get_context_data(**kwargs)
        context.update({
            'board': Board.objects.get(id=int(self.kwargs['board_id'])),
            'topic': Topic.objects.get(id=int(self.kwargs['topic_id']))
        })
        return context
