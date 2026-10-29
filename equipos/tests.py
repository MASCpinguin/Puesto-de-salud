from django.test import TestCase
from django.urls import reverse

from .models import Equipo
from .views import estadisticas_por_puesto


class EquipoTest(TestCase):
    def test_tabla_y_valor(self):
        self.assertEqual(Equipo._meta.db_table, 'equipos_equipo')
        e = Equipo.objects.create(nombre='Ana', documento='1', puesto='RODEO',
                                  microbiologia=2, bacteriologia=1, quimica=1)
        self.assertEqual(e.valor_total, 90000)   # 2x15000 + 25000 + 35000
        self.assertEqual(e.total_pruebas, 4)

    def test_estadisticas(self):
        Equipo.objects.create(nombre='A', documento='1', puesto='RODEO', microbiologia=2)
        Equipo.objects.create(nombre='B', documento='2', puesto='RODEO', microbiologia=1, quimica=1)
        rodeo = {p['nombre']: p for p in estadisticas_por_puesto()}['Rodeo']
        self.assertEqual(rodeo['usuarios'], 2)
        self.assertEqual([t['personas'] for t in rodeo['tipos']], [2, 0, 1])
        self.assertEqual([t['porcentaje'] for t in rodeo['tipos']], [75.0, 0, 25.0])

    def test_registrar_y_listar(self):
        r = self.client.post(reverse('registrar_equipo'), {
            'nombre': 'Luis', 'documento': '123', 'puesto': 'PETECUY',
            'microbiologia': 1, 'bacteriologia': 0, 'quimica': 2})
        self.assertRedirects(r, reverse('lista_equipos'))
        self.assertEqual(Equipo.objects.get().valor_total, 85000)
        self.assertContains(self.client.get(reverse('lista_equipos')), 'Luis')

    def test_sin_pruebas_no_registra(self):
        r = self.client.post(reverse('registrar_equipo'), {
            'nombre': 'X', 'documento': '9', 'puesto': 'RODEO',
            'microbiologia': 0, 'bacteriologia': 0, 'quimica': 0})
        self.assertEqual(r.status_code, 200)
        self.assertEqual(Equipo.objects.count(), 0)
