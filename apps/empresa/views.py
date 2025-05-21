from django.shortcuts import render, redirect, render
from django.contrib.auth.decorators import login_required, permission_required
from apps.empresa.models import Empresas, Ciudades
from apps.empresa.forms import EmpresaForm
from django.contrib import messages
from django.http import JsonResponse

@login_required
@permission_required('empresa.editar_empresa', raise_exception=True)
def configuracion(request):
    empresa = Empresas.objects.get(idempresa=100)
    empresa_form = EmpresaForm(instance=empresa)
    if request.method == "POST":
        empresa_form = EmpresaForm(request.POST, request.FILES, instance=empresa)
        if empresa_form.is_valid():
            empresa_form.save()
            messages.success(request, "¡Información de la Empresa Modificada Correctamente!")
            return redirect("empresa:configuracion")
        else:
            messages.error(request, "¡Por favor, corrige los errores en el formulario!")
    return render(request, 'configuracion.html', {"form": empresa_form, "empresa": empresa})

# AJAX
def ciudades_por_provincia(request, provincia_id):
    ciudades = Ciudades.objects.filter(idprovincia=provincia_id).values('pk', 'nombre_ciudad').order_by('nombre_ciudad')
    return JsonResponse({'ciudades': list(ciudades)})
