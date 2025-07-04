import re
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


class ValidadorPassword:

    def validate(self, password, user=None):
        #verificar si contiene una o + mayusculas
        if not re.search(r'[A-Z]', password):
            raise ValidationError(
                _("La contraseña debe contener al menos una mayúscula."),
                code='password_no_mayuscula',
            )
        #verificar si contiene una o + numero
        if not re.search(r'[0-9]', password):
            raise ValidationError(
                _("La contraseña debe contener al menos un numero."),
                code='password_no_numero',
            )
        #verificar si contiene una o + caracter especial
        if not re.search(r'[!@#$%^&*()<>_-]', password):
            raise ValidationError(
                _("La contraseña debe contener al menos un caracter especial (!@#$%^&*()<>_-)."),
                code='password_no_caracter',
            )
    def get_help_text(self):
        return _("La contraseña debe contener al menos una mayúscula, un número y un caracter especial (!@#$%^&*()<>_-).")