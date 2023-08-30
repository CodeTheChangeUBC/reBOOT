from django.db import models
from django.forms import ModelForm
from django.forms import modelform_factory
from django.forms import CheckboxSelectMultiple
from django import forms

from .models import RefurbishedItem

RefurbishedItemForm = modelform_factory(RefurbishedItem,
                                        fields=('builder',
                                                'date',
                                                'make',
                                                'item_model',
                                                'serial_no',
                                                'CPU_core',
                                                'CPU_generation',
                                                'windows_os_no',
                                                'storage_size',
                                                'storage_type',),
                                        widgets={"storage_type": forms.CheckboxSelectMultiple,
                                                 "screen_port": forms.CheckboxSelectMultiple,
                                                 "audio_features": forms.CheckboxSelectMultiple,
                                                 "LAN_type": forms.CheckboxSelectMultiple,
                                                 "installed_apps": forms.CheckboxSelectMultiple,
                                                 }
                                        ) 
# class RefurbishedItemForm(ModelForm):
#     class Meta:
#         model = RefurbishedItem
#         fields = {"storage_type"}
