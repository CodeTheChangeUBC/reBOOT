from django.db import models
from django.utils import timezone


class RefurbishedItem(models.Model):
    storage_type_choices = [
            ("HDD", "HDD"),
            ("SSD", "SSD"),
            ("M.2", "M.2"),
    ]

    screen_port_choices = [
            ("V", "VGA"),
            ("HDMI", "HDMI"),
            ("Display port", "Display port"),
    ]

    audio_feature_choices = [
            ("Speakers", "Speakers"),
            ("Headphones", "Headphones"),
            ("MIC", "MIC"),
            ("Headset MIC", "Headset MIC"),
    ]

    LAN_type_choices = [
            ("Ethernet", "Ethernet"),
            ("Wifi", "Wifi"),
    ]

    installed_apps_choices = [
            ("Open Office", "Open Office"),
            ("VLC", "VLC"),
            ("Firefox", "Firefox"),
    ]

    builder = models.CharField(max_length=200)
    date = models.DateTimeField("Date", default=timezone.now)
    make = models.CharField(max_length=200)
    item_model = models.CharField(max_length=200)
    serial_no = models.CharField("Serial number", max_length=200, null=True, default=None)

    CPU_core = models.CharField(max_length=200, null=True, default=None)
    CPU_generation = models.IntegerField("Generation", null=True, default=None)

    windows_os_no = models.IntegerField("Windows version (ex. '10' for Windows 10)", null=True, default=None)

    storage_size = models.IntegerField("Storage size (GB)", null=True, default=None)
    storage_type = models.CharField("Storage type", choices=storage_type_choices, null=True, default=None)

    screen_size = models.IntegerField("Screen size (inches)", null=True, default=None)
    screen_port = models.CharField("Screen port", choices=screen_port_choices, null=True, default=None, blank=True)

    audio_features = models.CharField("Audio features", choices=audio_feature_choices, null=True, default=None)

    battery_ok_or_charged = models.BooleanField("OK/Charged?", default=None)
    ram_size = models.IntegerField("Ram size (GB)", null=True, default=None)
    LAN_type = models.CharField("LAN type", choices=LAN_type_choices, null=True, default=None)

    installed_apps = models.CharField("Pre-installed apps", choices=installed_apps_choices, null=True, default=None, blank=True)
    misc_info = models.TextField("Miscellaneous info", null=True, default=None, blank=True)
    
    def __str__(self):
        return self.item_model 
