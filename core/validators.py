from datetime import date
from django.core.exceptions import ValidationError
from django.utils.deconstruct import deconstructible


@deconstructible
class MinAgeValidator:
    def __init__(self, edad_minima=18):
        self.edad_minima = edad_minima

    def __call__(self, fecha_nacimiento):
        today = date.today()
        edad = today.year - fecha_nacimiento.year

        if (fecha_nacimiento.month, fecha_nacimiento.day) > (today.month, today.day):
            edad -= 1

        if edad < self.edad_minima:
            raise ValidationError(
                f"El cliente debe ser mayor de {self.edad_minima} años"
            )
