from rest_framework.permissions import DjangoModelPermissions

class StrictDjangoModelPermissions(DjangoModelPermissions):
    def __init__(self):
        # Por defecto DjangoModelPermissions permite GET
        # Vamos a exigir permisos explícitos también para SAFE_METHODS
        self.perms_map['GET'] = ['%(app_label)s.view_%(model_name)s']
        self.perms_map['OPTIONS'] = ['%(app_label)s.view_%(model_name)s']
        self.perms_map['HEAD'] = ['%(app_label)s.view_%(model_name)s']
