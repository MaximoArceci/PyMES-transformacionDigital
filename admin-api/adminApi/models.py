# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models
from django.db.models.signals import pre_delete, pre_save
from django.dispatch import receiver
from django.core.exceptions import ValidationError
from django.contrib import messages
from django.utils.translation import gettext_lazy as _


class Pyme(models.Model):
    
    class work_type_options(models.TextChoices):
        transformacionDigital = 'Transformación Digital',
        innovacion = 'innovacion',
        sustentabilidad = 'Sustentabilidad'
    
    name = models.TextField(blank=True, null=True)
    work_type = models.CharField(
        max_length=100,
        choices=work_type_options.choices,
        default=work_type_options.transformacionDigital,
    )
    enterprise_type = models.TextField(blank=True, null=True)
    sector = models.TextField(blank=True, null=True)
    latitud = models.TextField(blank=True, null=True)
    longitud = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.id} - {self.name}"

