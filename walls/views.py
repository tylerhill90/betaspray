from django.shortcuts import render, get_object_or_404
from django.core.exceptions import PermissionDenied
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy

from .models import (
    Wall,
    Route
)

from .forms import (RouteForm)


class WallListView(ListView):

    model = Wall     

    template_name = 'walls/list.html'

    context_object_name = 'walls'

class WallTagListView(WallListView):

    template_name = 'walls/taglist.html'

    # Custom method
    def get_tag(self):
        return self.kwargs.get('tag')

    def get_queryset(self):
        return self.model.objects.filter(tags__slug=self.get_tag())

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["tag"] = self.get_tag()
        return 
        
class WallDetailView(DetailView):

    model = Wall

    template_name = 'walls/detail.html'

    context_object_name = 'wall'

class WallCreateView(LoginRequiredMixin, CreateView):

    model = Wall

    fields = ['name', 'image']

    template_name = 'walls/create.html'

    success_url = reverse_lazy('walls:list')

    def form_valid(self, form):

        form.instance.owner = self.request.user

        return super().form_valid(form)

class UserIsSubmitter(UserPassesTestMixin):
    # Custom method
    def get_wall(self):
        return get_object_or_404(Wall, pk=self.kwargs.get('pk'))

    def test_func(self):

        if self.request.user.is_authenticated:
            return self.request.user == self.get_wall().owner
        else:
            raise PermissionDenied('Sorry you are not allowed here')

class WallUpdateView(UserIsSubmitter, UpdateView):

    template_name = 'walls/update.html'

    model = Wall

    fields = ['name']

    success_url = reverse_lazy('walls:list')

class WallDeleteView(UserIsSubmitter, DeleteView):

    template_name = 'walls/delete.html'

    model = Wall

    success_url = reverse_lazy('walls:list')

class RouteCreateView(LoginRequiredMixin, CreateView):

    model = Route

    form_class = RouteForm

    template_name = 'walls/add_route.html'

    def get_success_url(self):
        return reverse_lazy('walls:detail', kwargs={'pk': self.object.wall_id})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['wall'] = Wall.objects.filter(image=self.object)
        return context

    def form_valid(self, form):
        form.instance.owner = self.request.user
        form.instance.wall_id = self.kwargs.get('pk')

        return super().form_valid(form)