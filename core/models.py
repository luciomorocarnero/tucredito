from datetime import date

from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator
from django.db import models
from django.db.models import CheckConstraint, F, Q
from phonenumber_field.modelfields import PhoneNumberField

from .validators import MinAgeValidator # pyright: ignore


class TimeStampedModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Cliente(TimeStampedModel):
    class TipoPersona(models.IntegerChoices):
        NATURAL = 1, "NATURAL"
        JURIDICO = 2, "JURIDICO"

    banco = models.ForeignKey("Banco", on_delete=models.PROTECT)

    nombre_completo = models.CharField(max_length=50)
    fecha_de_nacimiento = models.DateField(validators=[MinAgeValidator(18)])
    nacionalidad = models.CharField(max_length=50, blank=True)
    direccion = models.CharField(max_length=50, blank=True)
    email = models.EmailField(null=False, blank=False, unique=True)
    telefono = PhoneNumberField(null=False, blank=False, unique=True)
    tipo_persona = models.IntegerField(choices=TipoPersona.choices)

    def __str__(self) -> str:
        return f"{self.nombre_completo} - {self.banco.nombre}"

    @property
    def edad(self):
        now = date.today()
        edad = now.year - self.fecha_de_nacimiento.year
        if (
            self.fecha_de_nacimiento.month,
            self.fecha_de_nacimiento.day,
        ) > (now.month, now.day):
            edad -= 1
        return edad


class Credito(TimeStampedModel):
    MAX_DIGITS = 6

    class TipoCredito(models.IntegerChoices):
        AUTOMOTRIZ = 1, "AUTOMOTRIZ"
        HIPOTECARIO = 2, "HIPOTECARIO"
        COMERCIAL = 3, "COMERCIAL"

    cliente = models.ForeignKey("Cliente", on_delete=models.PROTECT)
    banco = models.ForeignKey("Banco", on_delete=models.PROTECT)
    descripcion = models.CharField(max_length=100, blank=True)
    pago_minimo = models.DecimalField(
        decimal_places=2,
        max_digits=MAX_DIGITS,
        validators=[MinValueValidator(0.01)],
    )
    pago_maximo = models.DecimalField(
        decimal_places=2,
        max_digits=MAX_DIGITS,
        validators=[MinValueValidator(0.01)],
    )
    plazo_meses = models.IntegerField(validators=[MinValueValidator(1)])
    tipo_credito = models.IntegerField(choices=TipoCredito.choices)

    # Fecha_Registro -> created_at

    def __str__(self) -> str:
        return f"{self.cliente} - {self.tipo_credito}"

    def clean(self):
        super().clean()
        if self.pago_minimo > self.pago_maximo:
            raise ValidationError(
                {
                    "pago_minimo": "El pago minimo no puede ser mayor al pago maximo",
                    "pago_maximo": "El pago maximo debe ser mayor o igual al pago minimo",
                }
            )

    class Meta:
        constraints = [
            CheckConstraint(
                condition=Q(pago_minimo__lte=F("pago_maximo")),
                name="pago_minimo_lte_pago_maximo",
            )
        ]


class Banco(TimeStampedModel):

    class Tipo(models.IntegerChoices):
        PRIVADO = 1, "PRIVADO"
        GOBIERNO = 2, "GOBIERNO"

    nombre = models.CharField(max_length=50)
    tipo = models.IntegerField(choices=Tipo.choices)
    direccion = models.CharField(max_length=50, blank=True)

    def __str__(self) -> str:
        return f"{self.nombre}"
