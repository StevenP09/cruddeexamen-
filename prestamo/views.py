from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from core.models import *
from django.core.paginator import Paginator
from prestamo.forms import PrestamoForm
from django.db.models import Q
from django.db import connection

# Create your views here.
def prestamo_create(request):
    context={'title':'Ingresar Prestamo'}
    if request.method == "GET":
        form = PrestamoForm()
        context['form'] = form
        return render(request, 'prestamo/create.html', context)
    else:
        print("entro por post")
        form = PrestamoForm(request.POST)
        print(form)
        if form.is_valid():
            
            form.save()
            return redirect('prestamo:list')
        else:
            context['form'] = form
            return render(request, 'prestamo/create.html',context)

def prestamo_list(request):
    prestamos = Prestamo.objects.all()
    context={'title':'Consultar Prestamo'}
    query_name = request.GET.get('name', None)
    query_departamento = request.GET.get('departamento', None)
    
    if query_name: prestamos = Prestamo.objects.filter(nombre__icontains=query_name)
    
    if query_departamento: prestamos = Prestamo.objects.filter(departamento__descripcion__icontains=query_departamento)
    
    if query_name and query_departamento: 
        prestamos = Prestamo.objects.filter(
        Q(nombre__icontains=query_name)
        & Q(departamento__descripcion__icontains=query_departamento)
        )
        
    paginator = Paginator(prestamos, 5)  # Número de empleados por página
    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)
    context = {
        'title': 'Consultar Prestamo',
        'prestamos': page_obj,
        'query': query_name
    }
    return render(request, 'prestamo/list.html', context)

def prestamo_update(request, id):
    context={'title':'Actualizar Prestamo'}
    prestamo = get_object_or_404(Prestamo, pk=id)
    if request.method == "GET":
        form = PrestamoForm(instance=prestamo)
        context['form'] = form
        return render(request, 'prestamo/create.html', context)
    else:
        form = PrestamoForm(request.POST, instance=prestamo)
        if form.is_valid():
            form.save()
            return redirect('prestamo:list')
        else:
            context['form'] = form
            return render(request, 'prestamo/create.html', context)

       
def prestamo_delete(request, id):
    prestamo = get_object_or_404(Prestamo, pk=id)

    if request.method == "GET":
        prestamo.delete()
        
        last_id = Prestamo.objects.order_by('-id').first().id if Prestamo.objects.exists() else 0
        with connection.cursor() as cursor:
            cursor.execute(f"UPDATE sqlite_sequence SET seq = {last_id} WHERE name = 'core_prestamo'")
            
        return redirect('prestamo:list')

    return redirect('prestamo:list')



def get_tipoPrestamo(request, id):
    tipo = TipoPrestamo.objects.get(pk=id)
    
    data = {
        'tasa': tipo.tasa
    }
    
    return JsonResponse(data, safe=False)

def get_rol(request, id):
    rol = Rol.objects.get(pk=id)
    return render(request, 'rol/detail.html', {'rol': rol, 'title': 'Datos del Rol'})