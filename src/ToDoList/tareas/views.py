from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import redirect
from django.db.models import Q
from tareas.forms import AddTaskForm, EditTaskForm
import datetime

from .models import Task


@login_required
def add_tarea(request):
    form = AddTaskForm()
    form.instance.user = request.user
    error = False
    if request.method == 'POST':
        form = AddTaskForm(request.POST)
        if form.is_valid():
            form.save(commit=True)
        else:
            error = True
    return render(request, 'agregar_tarea.html', context={'tarea': tarea,
                                                            'form': form})


@login_required
def get_tareas(request):
    busqueda = request.GET.get("buscar")
    tareas = Task.objects.all()

    if busqueda:
        tareas = Task.objects.filter(
            Q(task_name__icontains = busqueda) |
            Q(task_description__icontains = busqueda) |
            Q(status__icontains = busqueda)
        ).distinct()

    return render(request, 'tareas_list.html', context={'tareas': tareas})


@login_required
def tarea(request, id_tarea):
    tarea = Task.objects.get(pk=id_tarea)
    return render(request, 'tarea.html', context={'tarea': tarea})


@login_required
def eliminar_tarea(request, task_id):
    try:
        task = Task.objects.get(pk=task_id)
    except Task.DoesNotExist:
        messages.error(request, "Ya no existe esta tarea")
        return redirect("../")

    if task.user != request.user:
        messages.error(request, "Usted no es el creador de la tarea")
        return redirect("../")
    else:
        task.delete()
        messages.success(request, f"la tarea  {task.task_name} ha sido eliminada")
        return redirect("../")


@login_required
def editar_tarea(request, task_id):
    task = Task.objects.get(pk=task_id)
    form = EditTaskForm(instance=task)
    if request.method == 'POST':
        form = EditTaskForm(request.POST, instance=task)
    if form.is_valid():
        form.save(commit=True)
    return render(request, 'editar_tarea.html', context={'form': form, 'task': task})

