from django.db import models


class Equipo(models.Model):
    """Registro de un usuario atendido en un puesto de salud y sus M pruebas de laboratorio.

    Django crea la tabla con el nombre <app>_<modelo>: equipos_equipo (ver diagrama).
    """

    # Puestos de salud del pueblo
    PUESTOS = [
        ('RODEO', 'Rodeo'),
        ('RIVERA', 'Rivera'),
        ('PETECUY', 'Petecuy'),
    ]

    # Tarifas por tipo de prueba (en pesos)
    TARIFA_MICROBIOLOGIA = 15000
    TARIFA_BACTERIOLOGIA = 25000
    TARIFA_QUIMICA = 35000

    nombre = models.CharField('Nombre del usuario', max_length=100)
    documento = models.CharField('Documento de identidad', max_length=20)
    puesto = models.CharField('Puesto de salud', max_length=10, choices=PUESTOS)

    # Cantidad de pruebas de cada tipo que se tomó el usuario
    microbiologia = models.PositiveIntegerField('Pruebas de Microbiología', default=0)
    bacteriologia = models.PositiveIntegerField('Pruebas de Bacteriología', default=0)
    quimica = models.PositiveIntegerField('Pruebas de Química', default=0)

    valor_total = models.PositiveIntegerField('Valor a pagar', default=0, editable=False)
    fecha_registro = models.DateTimeField('Fecha de registro', auto_now_add=True)

    class Meta:
        ordering = ['-fecha_registro']

    def __str__(self):
        return f'{self.nombre} ({self.get_puesto_display()})'

    @property
    def total_pruebas(self):
        """M: número total de pruebas del usuario."""
        return self.microbiologia + self.bacteriologia + self.quimica

    def calcular_valor(self):
        """Valor a pagar = cantidad de cada tipo x su tarifa."""
        return (
            self.microbiologia * self.TARIFA_MICROBIOLOGIA
            + self.bacteriologia * self.TARIFA_BACTERIOLOGIA
            + self.quimica * self.TARIFA_QUIMICA
        )

    def save(self, *args, **kwargs):
        # El valor a pagar siempre lo calcula el servidor
        self.valor_total = self.calcular_valor()
        super().save(*args, **kwargs)
