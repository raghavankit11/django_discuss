from django.shortcuts import render, get_object_or_404, get_list_or_404
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView
)
from .models import Post, Comment, Subscription, Notification


def home(request):
    context = {
        'posts': Post.objects.all()
    }
    return render(request, 'blog/home.html', context)


class PostListView(ListView):
    model = Post
    template_name = 'blog/home.html'  # <app>/<model>_<viewtype>.html
    context_object_name = 'posts'
    ordering = ['-date_posted']
    paginate_by = 5

    def get_queryset(self):
        user = self.request.user
        posts = Post.objects.order_by('-date_posted').all()
        for p in posts:
            p.is_user_subscribed = p.subscriptions.filter(user__id__exact=user.id).exists()
            p.is_user_subscribed_not = not p.is_user_subscribed

        return posts


class UserPostListView(ListView):
    model = Post
    template_name = 'blog/user_posts.html'  # <app>/<model>_<viewtype>.html
    context_object_name = 'posts'
    paginate_by = 5

    def get_queryset(self):
        user = self.request.user
        posts = Post.objects.filter(author=user).order_by('-date_posted').all()
        for p in posts:
            p.is_user_subscribed = p.subscriptions.filter(user__id__exact=user.id).exists()
            p.is_user_subscribed_not = not p.is_user_subscribed

        return posts


# region Post - Views


class PostDetailView(DetailView):
    model = Post

    def get_object(self, queryset=None):
        obj = super(PostDetailView, self).get_object()
        user = self.request.user
        obj.is_user_subscribed = obj.subscriptions.filter(user__id__exact=user.id).exists()
        obj.is_user_subscribed_not = not obj.is_user_subscribed
        return obj


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    fields = ['title', 'content', 'anonymous']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    fields = ['title', 'content', 'anonymous']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False


class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    success_url = '/'

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False


# endregion

# region Comment - Views
class CommentDetailView(DetailView):
    model = Comment


class CommentCreateView(LoginRequiredMixin, CreateView):
    model = Comment
    fields = ['content', 'anonymous']

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.post = Post.objects.get(pk=self.kwargs.get('post_id'))
        return super().form_valid(form)


class CommentUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Comment
    fields = ['content', 'anonymous']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False


class CommentDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Comment
    success_url = '/'

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False


# endregion


def about(request):
    return render(request, 'blog/about.html', {'title': 'About'})


# region - Subscription

def subscribe_post(request, post_id):
    user = request.user
    post = Post.objects.get(pk=post_id)

    is_already_subscribed = Subscription.objects.filter(user__id__exact=user.id, post__id__exact=post.id).exists()
    if not is_already_subscribed:
        s = Subscription(user=user, post=post)  # Creating Like Object
        s.save()  # saving it to store in database
        is_saved = Subscription.objects.filter(user__id__exact=user.id, post__id__exact=post.id).exists()
    else:
        is_saved = True

    data = {
        'result': is_saved
    }
    return JsonResponse(data)


def unsubscribe_post(request, post_id):
    user = request.user
    post = Post.objects.get(pk=post_id)

    ss = Subscription.objects.filter(user__id__exact=user.id, post__id__exact=post.id)
    ss.delete()
    is_deleted = not Subscription.objects.filter(user__id__exact=user.id, post__id__exact=post.id).exists()

    data = {
        'result': is_deleted
    }
    return JsonResponse(data)


# endregion

def user_notifications_get(request, username):
    user = request.user

    nn = Notification.objects.filter(subscription__user=user)

    result = []
    for n in nn:
        user_notification = {'comment_id': n.comment.id,
                             'comment_text': n.comment.content,
                             'username': n.comment.author.username,
                             'post_title': n.comment.post.title,
                             'posted_on': n.comment.date_posted}
        result.append(user_notification)

    data = {'result': result}
    final = JsonResponse(data, safe=False)

    return final
