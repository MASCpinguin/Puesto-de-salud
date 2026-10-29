from django.contrib import messages
from django.db.models import Count, Q, Sum
from django.shortcuts import redirect, render

from .forms import EquipoForm
from .models import Equipo

# (campo del modelo, nombre a mostrar, tarifa)
TIPOS_PRUEBA = [
    ('microbiologia', 'Microbiología', Equipo.TARIFA_MICROBIOLOGIA),
    ('bacteriologia', 'Bacteriología', Equipo.TARIFA_BACTERIOLOGIA),
    ('quimica', 'Química', Equipo.TARIFA_QUIMICA),
]


def estadisticas_por_puesto():
    """Para cada puesto: cuántos usuarios hay, cuántas personas hay por tipo
    de prueba y el porcentaje de cada tipo sobre el total de pruebas del puesto."""
    resultado = []
    for codigo, nombre in Equipo.PUESTOS:
        consulta = {'usuarios': Count('id'), 'recaudo': Sum('valor_total', default=0)}
        for campo, _, _ in TIPOS_PRUEBA:
            # Personas = usuarios con al menos una prueba de ese tipo
            consulta[f'personas_{campo}'] = Count('id', filter=Q(**{f'{campo}__gt': 0}))
            consulta[f'pruebas_{campo}'] = Sum(campo, default=0)
        datos = Equipo.objects.filter(puesto=codigo).aggregate(**consulta)

        total_pruebas = sum(datos[f'pruebas_{campo}'] for campo, _, _ in TIPOS_PRUEBA)
        tipos = []
        for campo, etiqueta, tarifa in TIPOS_PRUEBA:
            pruebas = datos[f'pruebas_{campo}']
            tipos.append({
                'nombre': etiqueta,
                'personas': datos[f'personas_{campo}'],
                'pruebas': pruebas,
                'porcentaje': round(pruebas * 100 / total_pruebas, 2) if total_pruebas else 0,
            })

        resultado.append({
            'nombre': nombre,
            'usuarios': datos['usuarios'],
            'total_pruebas': total_pruebas,
            'recaudo': datos['recaudo'],
            'tipos': tipos,
        })
    return resultado


def lista_equipos(request):
    """Muestra los usuarios registrados y el informe por puesto."""
    return render(request, 'equipos/lista_equipos.html', {
        'equipos': Equipo.objects.all(),
        'puestos': estadisticas_por_puesto(),
        'tipos_prueba': TIPOS_PRUEBA,
    })


def registrar_equipo(request):
    """GET: muestra el formulario. POST: valida, guarda y calcula el valor a pagar."""
    if request.method == 'POST':
        form = EquipoForm(request.POST)
        if form.is_valid():
            equipo = form.save()
            valor = f'{equipo.valor_total:,}'.replace(',', '.')
            messages.success(
                request,
                f'{equipo.nombre} registrado en {equipo.get_puesto_display()}: '
                f'{equipo.total_pruebas} prueba(s), valor a pagar ${valor}',
            )
            return redirect('lista_equipos')
    else:
        form = EquipoForm()

    return render(request, 'equipos/registrar_equipo.html', {
        'form': form,
        'tipos_prueba': TIPOS_PRUEBA,
    })
