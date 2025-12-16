from rest_framework import serializers


class ChoiceDisplayField(serializers.Field):
    """Campo personalizado para mostrar ID y Nombre de un ChoiceField"""

    def to_representation(self, value):
        method_name = f"get_{self.field_name}_display"
        display = getattr(self.parent.instance, method_name)()
        return {"id": value, "nombre": display}

    def to_internal_value(self, data):
        return data
