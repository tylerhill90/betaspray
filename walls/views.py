from django.shortcuts import render, get_object_or_404
from django.core.exceptions import PermissionDenied, ValidationError
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy, reverse
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.contrib import messages

from .models import (
    Wall,
    Route
)

from .forms import (
    WallForm,
    RouteForm, 
    WallHoldForm
)


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

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super(WallCreateView, self).form_valid(form)

    def get_success_url(self):
        print(self.kwargs)
        return reverse('walls:add_holds', kwargs={'pk': self.object.id})


@login_required
def add_wall_holds(request, pk):
    wall = get_object_or_404(Wall, pk=pk)

    if request.method == 'POST':
        pass

    else:
        form = WallHoldForm()
        context = {
            'form': form,
            'pk': pk
        }
        return render(request, 'walls/add_hold.html', context)


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


@login_required
def create_wall(request):
    form = WallForm()

    if request.method == 'POST':
        form = WallForm(request.POST, request.FILES, owner=request.user)
        if form.is_valid():
            new_wall = Wall(
                owner = request.user,
                name = form.cleaned_data['name'],
                image = form.cleaned_data['image'],
            )
            new_wall.save()
            return HttpResponseRedirect(reverse_lazy('walls:add_holds', kwargs={'pk': new_wall.id}))
    
    context = {'form': form}
    return render(request, 'walls/create.html', context)


@login_required
def create_route(request, pk):
    form = RouteForm()
    wall = get_object_or_404(Wall, pk=pk)

    if request.method == 'POST':
        form = RouteForm(request.POST, wall_id=wall.pk)
        if form.is_valid():
            Route(
                owner = request.user,
                wall = wall,
                name = form.cleaned_data['name'],
                grade = form.cleaned_data['grade'],
                tags = form.cleaned_data['tags'],
                notes = form.cleaned_data['notes']
            ).save()
            return HttpResponseRedirect(reverse_lazy('walls:detail', kwargs={'pk': pk}))
        
    context = {
        'form': form,
        'pk': pk
    }
    return render(request, 'walls/add_route.html', context)
