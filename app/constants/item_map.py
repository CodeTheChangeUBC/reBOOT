from app.enums import ItemCategoryEnum
'''
ITEM_MAP is a dict of format:
{
    'legacy item description': {
        'category': ItemCategoryEnum.categoryA.name, 'device_type': 'device type a'
    }
}
'''
ITEM_MAP = {
    '': {'category': ItemCategoryEnum.MISCELLANEOUS.name, 'device_type': 'N/A'},
    'access point': {'category': ItemCategoryEnum.NETWORK.name, 'device_type': 'Access Point'},
    'access point (wireless)': {'category': ItemCategoryEnum.NETWORK.name, 'device_type': 'Access Point'},
    'access point - wireless': {'category': ItemCategoryEnum.NETWORK.name, 'device_type': 'Access Point'},
    'audio streamer': {'category': ItemCategoryEnum.AUDIO.name, 'device_type': 'Streamer'},
    'base station (wireless)': {'category': ItemCategoryEnum.NETWORK.name, 'device_type': 'Access Point'},
    'battery (li-ion)': {'category': ItemCategoryEnum.BATTERY.name, 'device_type': 'Li-ion'},
    'battery (ni-mh)': {'category': ItemCategoryEnum.BATTERY.name, 'device_type': 'Ni-MH'},
    'battery (power bank)': {'category': ItemCategoryEnum.BATTERY.name, 'device_type': 'Power Bank'},
    'battery (ups)': {'category': ItemCategoryEnum.BATTERY.name, 'device_type': 'UPS'},
    'battery (vrla)': {'category': ItemCategoryEnum.BATTERY.name, 'device_type': 'VRLA'},
    'battery - ups': {'category': ItemCategoryEnum.BATTERY.name, 'device_type': 'UPS'},
    'bookshelf stereo': {'category': ItemCategoryEnum.AUDIO.name, 'device_type': 'Stereo'},
    'boombox': {'category': ItemCategoryEnum.AUDIO.name, 'device_type': 'Boombox'},
    'broadband router': {'category': ItemCategoryEnum.NETWORK.name, 'device_type': 'Router'},
    'cable lock': {'category': ItemCategoryEnum.PERIPHERAL.name, 'device_type': 'Cable Lock'},
    'camcorder': {'category': ItemCategoryEnum.CAMERA.name, 'device_type': 'Video'},
    'camera': {'category': ItemCategoryEnum.CAMERA.name, 'device_type': 'Camera'},
    'camera (cctv)': {'category': ItemCategoryEnum.CAMERA.name, 'device_type': 'CCTV'},
    'camera (digital)': {'category': ItemCategoryEnum.CAMERA.name, 'device_type': 'Digital'},
    'camera (film)': {'category': ItemCategoryEnum.CAMERA.name, 'device_type': 'Film'},
    'camera (video)': {'category': ItemCategoryEnum.CAMERA.name, 'device_type': 'Video'},
    'camera (wi-fi)': {'category': ItemCategoryEnum.CAMERA.name, 'device_type': 'Wifi Camera'},
    'camera - cctv': {'category': ItemCategoryEnum.CAMERA.name, 'device_type': 'CCTV'},
    'camera - digital': {'category': ItemCategoryEnum.CAMERA.name, 'device_type': 'Digital'},
    'camera - film': {'category': ItemCategoryEnum.CAMERA.name, 'device_type': 'Film'},
    'camera - video': {'category': ItemCategoryEnum.CAMERA.name, 'device_type': 'Video'},
    'cell phone': {'category': ItemCategoryEnum.PHONE.name, 'device_type': 'Cell Phone'},
    'cellphone': {'category': ItemCategoryEnum.PHONE.name, 'device_type': 'Cell Phone'},
    'charging cradle': {'category': ItemCategoryEnum.PERIPHERAL.name, 'device_type': 'Charging Cradle'},
    'compuer - tower': {'category': ItemCategoryEnum.COMPUTER.name, 'device_type': 'Tower'},
    'computer': {'category': ItemCategoryEnum.COMPUTER.name, 'device_type': 'Computer'},
    'computer (all-in-one)': {'category': ItemCategoryEnum.COMPUTER.name, 'device_type': 'All in One'},
    'computer (desktop)': {'category': ItemCategoryEnum.COMPUTER.name, 'device_type': 'Desktop'},
    'computer (laptop)': {'category': ItemCategoryEnum.COMPUTER.name, 'device_type': 'Laptop'},
    'computer (pocket pc)': {'category': ItemCategoryEnum.COMPUTER.name, 'device_type': 'Pocket PC'},
    'computer (server)': {'category': ItemCategoryEnum.COMPUTER.name, 'device_type': 'Server'},
    'computer (tablet)': {'category': ItemCategoryEnum.TABLET.name, 'device_type': 'Tablet'},
    'computer (thin client)': {'category': ItemCategoryEnum.COMPUTER.name, 'device_type': 'Thin Client'},
    'computer (tower)': {'category': ItemCategoryEnum.COMPUTER.name, 'device_type': 'Tower'},
    'computer (workstation)': {'category': ItemCategoryEnum.COMPUTER.name, 'device_type': 'Computer'},
    'computer - all-in-one': {'category': ItemCategoryEnum.COMPUTER.name, 'device_type': 'All in One'},
    'computer - complete': {'category': ItemCategoryEnum.COMPUTER.name, 'device_type': 'Desktop'},
    'computer - desktop': {'category': ItemCategoryEnum.COMPUTER.name, 'device_type': 'Desktop'},
    'computer - laptop': {'category': ItemCategoryEnum.COMPUTER.name, 'device_type': 'Laptop'},
    'computer - server': {'category': ItemCategoryEnum.COMPUTER.name, 'device_type': 'Server'},
    'computer - sff': {'category': ItemCategoryEnum.COMPUTER.name, 'device_type': 'SFF'},
    'computer - ssf': {'category': ItemCategoryEnum.COMPUTER.name, 'device_type': 'SSF'},
    'computer - tablet': {'category': ItemCategoryEnum.TABLET.name, 'device_type': 'Tablet'},
    'computer - thin client': {'category': ItemCategoryEnum.COMPUTER.name, 'device_type': 'Thin Client'},
    'computer - tower': {'category': ItemCategoryEnum.COMPUTER.name, 'device_type': 'Tower'},
    'computer - usff': {'category': ItemCategoryEnum.COMPUTER.name, 'device_type': 'USSF'},
    'computer - workstation': {'category': ItemCategoryEnum.COMPUTER.name, 'device_type': 'Desktop'},
    'computer case': {'category': ItemCategoryEnum.PERIPHERAL.name, 'device_type': 'Computer Case'},
    'controller card': {'category': ItemCategoryEnum.COMPONENT.name, 'device_type': 'Controller Card'},
    'copier (digital)': {'category': ItemCategoryEnum.PRINTER.name, 'device_type': 'Digital'},
    'copier (personal)': {'category': ItemCategoryEnum.PRINTER.name, 'device_type': 'Copier'},
    'copier - digital': {'category': ItemCategoryEnum.PRINTER.name, 'device_type': 'Copier'},
    'docking station': {'category': ItemCategoryEnum.PERIPHERAL.name, 'device_type': 'Docking Station'},
    'e-reader': {'category': ItemCategoryEnum.TABLET.name, 'device_type': 'eReader'},
    'earphones': {'category': ItemCategoryEnum.AUDIO.name, 'device_type': 'Earphones'},
    'earphones (wireless)': {'category': ItemCategoryEnum.AUDIO.name, 'device_type': 'Earphones'},
    'ereader': {'category': ItemCategoryEnum.TABLET.name, 'device_type': 'eReader'},
    'ethernet adapter': {'category': ItemCategoryEnum.COMPONENT.name, 'device_type': 'NIC'},
    'ethernet adaptor': {'category': ItemCategoryEnum.NETWORK.name, 'device_type': 'Ethernet'},
    'fax imaging film': {'category': ItemCategoryEnum.PRINTER.name, 'device_type': 'Fax Imaging Film'},
    'fax machine': {'category': ItemCategoryEnum.PRINTER.name, 'device_type': 'Fax Machine'},
    'firewall appliance': {'category': ItemCategoryEnum.NETWORK.name, 'device_type': 'Firewall'},
    'firewall/router': {'category': ItemCategoryEnum.NETWORK.name, 'device_type': 'Security Appliance'},
    'flash drive (usb)': {'category': ItemCategoryEnum.STORAGE.name, 'device_type': 'USB'},
    'floppy drive': {'category': ItemCategoryEnum.STORAGE.name, 'device_type': 'Floppy Drive'},
    'gateway': {'category': ItemCategoryEnum.NETWORK.name, 'device_type': 'Gateway'},
    'gps unit': {'category': ItemCategoryEnum.SMALL_ELECTRIC_NON_IT.name, 'device_type': 'GPS'},
    'graphics card': {'category': ItemCategoryEnum.COMPONENT.name, 'device_type': 'Graphic Card'},
    'graphics processor': {'category': ItemCategoryEnum.COMPONENT.name, 'device_type': 'Graphic Card'},
    'graphics tablet': {'category': ItemCategoryEnum.TABLET.name, 'device_type': 'Graphics'},
    'hard drive': {'category': ItemCategoryEnum.STORAGE.name, 'device_type': 'Hard Drive'},
    'hard drive (ata)': {'category': ItemCategoryEnum.STORAGE.name, 'device_type': 'HDD ATA'},
    'hard drive (external)': {'category': ItemCategoryEnum.STORAGE.name, 'device_type': 'HDD External'},
    'hard drive (fcal)': {'category': ItemCategoryEnum.STORAGE.name, 'device_type': 'HDD FC-AL'},
    'hard drive (ide)': {'category': ItemCategoryEnum.STORAGE.name, 'device_type': 'HDD IDE'},
    'hard drive (pata)': {'category': ItemCategoryEnum.STORAGE.name, 'device_type': 'HDD PATA'},
    'hard drive (sas)': {'category': ItemCategoryEnum.STORAGE.name, 'device_type': 'HDD SAS'},
    'hard drive (sata)': {'category': ItemCategoryEnum.STORAGE.name, 'device_type': 'HDD SATA'},
    'hard drive (scsi)': {'category': ItemCategoryEnum.STORAGE.name, 'device_type': 'HDD SCSI'},
    'hard drive (ssd)': {'category': ItemCategoryEnum.STORAGE.name, 'device_type': 'HDD SSD'},
    'hard drive - ata': {'category': ItemCategoryEnum.STORAGE.name, 'device_type': 'HDD ATA'},
    'hard drive - external': {'category': ItemCategoryEnum.STORAGE.name, 'device_type': 'external'},
    'hard drive - ide': {'category': ItemCategoryEnum.STORAGE.name, 'device_type': 'HDD IDE'},
    'hard drive - sas': {'category': ItemCategoryEnum.STORAGE.name, 'device_type': 'HDD SAS'},
    'hard drive - sata': {'category': ItemCategoryEnum.STORAGE.name, 'device_type': 'HDD SATA'},
    'hard drive - scsi': {'category': ItemCategoryEnum.STORAGE.name, 'device_type': 'HDD SCSI'},
    'hard drive - ssd': {'category': ItemCategoryEnum.STORAGE.name, 'device_type': 'HDD SSD'},
    'hard drive enclosure': {'category': ItemCategoryEnum.STORAGE.name, 'device_type': 'Hard Drive Enclosure'},
    'hard drives': {'category': ItemCategoryEnum.STORAGE.name, 'device_type': 'Hard Drive'},
    'hdd': {'category': ItemCategoryEnum.STORAGE.name, 'device_type': 'HDD'},
    'hdd (sata)': {'category': ItemCategoryEnum.STORAGE.name, 'device_type': 'HDD SATA'},
    'headphones': {'category': ItemCategoryEnum.PERIPHERAL.name, 'device_type': 'Headphones'},
    'headphones (bt)': {'category': ItemCategoryEnum.PERIPHERAL.name, 'device_type': 'Headphones'},
    'headphones (wireless)': {'category': ItemCategoryEnum.PERIPHERAL.name, 'device_type': 'Headphones'},
    'headset': {'category': ItemCategoryEnum.PERIPHERAL.name, 'device_type': 'Headset'},
    'headset (bluetooth)': {'category': ItemCategoryEnum.PERIPHERAL.name, 'device_type': 'Headset'},
    'headset (bt)': {'category': ItemCategoryEnum.PERIPHERAL.name, 'device_type': 'Headset'},
    'headset (wireless)': {'category': ItemCategoryEnum.PERIPHERAL.name, 'device_type': 'Headset'},
    'home theatre (2.1)': {'category': ItemCategoryEnum.VIDEO.name, 'device_type': 'Home Theater'},
    'home theatre (5.1)': {'category': ItemCategoryEnum.VIDEO.name, 'device_type': 'Home Theater'},
    'home theatre system': {'category': ItemCategoryEnum.VIDEO.name, 'device_type': 'Home Theater'},
    'hub (ethernet)': {'category': ItemCategoryEnum.NETWORK.name, 'device_type': 'Ethernet'},
    'hub (rackmount)': {'category': ItemCategoryEnum.NETWORK.name, 'device_type': 'Hub'},
    'ink cartridge': {'category': ItemCategoryEnum.PRINTER.name, 'device_type': 'Ink'},
    'ink cartridge (new)': {'category': ItemCategoryEnum.PRINTER.name, 'device_type': 'Ink New'},
    'keyboard': {'category': ItemCategoryEnum.PERIPHERAL.name, 'device_type': 'Keyboard'},
    'keyboard (bluetooth)': {'category': ItemCategoryEnum.PERIPHERAL.name, 'device_type': 'Keyboard'},
    'keyboard (bt)': {'category': ItemCategoryEnum.PERIPHERAL.name, 'device_type': 'Keyboard'},
    'keyboard (ps/2)': {'category': ItemCategoryEnum.PERIPHERAL.name, 'device_type': 'Keyboard'},
    'keyboard (rf)': {'category': ItemCategoryEnum.PERIPHERAL.name, 'device_type': 'Keyboard'},
    'keyboard (usb)': {'category': ItemCategoryEnum.PERIPHERAL.name, 'device_type': 'Keyboard'},
    'keyboard (wireless)': {'category': ItemCategoryEnum.PERIPHERAL.name, 'device_type': 'Keyboard'},
    'keypad': {'category': ItemCategoryEnum.PERIPHERAL.name, 'device_type': 'Keypad'},
    'laptop': {'category': ItemCategoryEnum.COMPUTER.name, 'device_type': 'Laptop'},
    'laptop bag': {'category': ItemCategoryEnum.PERIPHERAL.name, 'device_type': 'Laptop Bag'},
    'lock': {'category': ItemCategoryEnum.PERIPHERAL.name, 'device_type': 'Lock'},
    'ltv - lcd': {'category': ItemCategoryEnum.MONITOR.name, 'device_type': 'LCD'},
    'm isc cables': {'category': ItemCategoryEnum.CABLES.name, 'device_type': 'Cable'},
    'media player': {'category': ItemCategoryEnum.VIDEO.name, 'device_type': 'Media Player'},
    'media streamer': {'category': ItemCategoryEnum.VIDEO.name, 'device_type': 'Streamer'},
    'misc cables': {'category': ItemCategoryEnum.CABLES.name, 'device_type': 'Misc'},
    'misc cords/cables': {'category': ItemCategoryEnum.CABLES.name, 'device_type': 'Misc'},
    'misc dispose': {'category': ItemCategoryEnum.DISPOSE.name, 'device_type': 'Dispose'},
    'misc scarp': {'category': ItemCategoryEnum.RECYCLE.name, 'device_type': 'Misc'},
    'misc small electronics': {'category': ItemCategoryEnum.SMALL_ELECTRIC_NON_IT.name, 'device_type': 'Misc'},
    'misc software': {'category': ItemCategoryEnum.SOFTWARE.name, 'device_type': 'Software'},
    'misc. cords/cables': {'category': ItemCategoryEnum.CABLES.name, 'device_type': 'Misc'},
    'misc. electronics': {'category': ItemCategoryEnum.SMALL_ELECTRIC_NON_IT.name, 'device_type': 'Misc'},
    'misc. small electronics': {'category': ItemCategoryEnum.SMALL_ELECTRIC_NON_IT.name, 'device_type': 'Misc'},
    'miscellaneous': {'category': ItemCategoryEnum.ASSORTED.name, 'device_type': 'Misc'},
    'modem': {'category': ItemCategoryEnum.NETWORK.name, 'device_type': 'Modem'},
    'modem (cable)': {'category': ItemCategoryEnum.NETWORK.name, 'device_type': 'Cable'},
    'modem (dsl)': {'category': ItemCategoryEnum.NETWORK.name, 'device_type': 'Modem'},
    'modem (telephony)': {'category': ItemCategoryEnum.NETWORK.name, 'device_type': 'Modem'},
    'modem - broadband': {'category': ItemCategoryEnum.NETWORK.name, 'device_type': 'Router'},
    'modem - cable': {'category': ItemCategoryEnum.NETWORK.name, 'device_type': 'Cable'},
    'modem - dsl': {'category': ItemCategoryEnum.NETWORK.name, 'device_type': 'Modem'},
    'modem/router': {'category': ItemCategoryEnum.NETWORK.name, 'device_type': 'Modem'},
    'monetary donation': {'category': ItemCategoryEnum.CASH.name, 'device_type': 'Cash'},
    'monitor': {'category': ItemCategoryEnum.MONITOR.name, 'device_type': 'Monitor'},
    'monitor (crt)': {'category': ItemCategoryEnum.MONITOR.name, 'device_type': 'CRT'},
    'monitor (lcd)': {'category': ItemCategoryEnum.MONITOR.name, 'device_type': 'LCD'},
    'monitor (touchscreen)': {'category': ItemCategoryEnum.MONITOR.name, 'device_type': 'Touchscreen'},
    'monitor - crt': {'category': ItemCategoryEnum.MONITOR.name, 'device_type': 'CRT'},
    'monitor - flat': {'category': ItemCategoryEnum.MONITOR.name, 'device_type': 'Flat Screen'},
    'monitor - lcd': {'category': ItemCategoryEnum.MONITOR.name, 'device_type': 'LCD'},
    'monitor - led': {'category': ItemCategoryEnum.MONITOR.name, 'device_type': 'LED'},
    'monitor - plasma': {'category': ItemCategoryEnum.MONITOR.name, 'device_type': 'Plasma'},
    'monitor stand': {'category': ItemCategoryEnum.PERIPHERAL.name, 'device_type': 'Stand/Mount/Frame Enclosure'},
    'motherboard': {'category': ItemCategoryEnum.COMPONENT.name, 'device_type': 'Motherboard'},
    'mouse': {'category': ItemCategoryEnum.PERIPHERAL.name, 'device_type': 'Mouse'},
    'mouse (bluetooth)': {'category': ItemCategoryEnum.PERIPHERAL.name, 'device_type': 'Mouse'},
    'mouse (bt)': {'category': ItemCategoryEnum.PERIPHERAL.name, 'device_type': 'Mouse'},
    'mouse (ps/2)': {'category': ItemCategoryEnum.PERIPHERAL.name, 'device_type': 'Mouse'},
    'mouse (rf)': {'category': ItemCategoryEnum.PERIPHERAL.name, 'device_type': 'Mouse'},
    'mouse (usb)': {'category': ItemCategoryEnum.PERIPHERAL.name, 'device_type': 'Mouse'},
    'mouse (wireless)': {'category': ItemCategoryEnum.PERIPHERAL.name, 'device_type': 'Mouse'},
    'multimedia projector': {'category': ItemCategoryEnum.VIDEO.name, 'device_type': 'TV Plasma'},
    'network adapter': {'category': ItemCategoryEnum.COMPONENT.name, 'device_type': 'NIC'},
    'network adapter (bluetooth)': {'category': ItemCategoryEnum.PERIPHERAL.name, 'device_type': 'Bluetooth Adapter'},
    'network adapter (cardbus)': {'category': ItemCategoryEnum.PERIPHERAL.name, 'device_type': 'CardBus Card'},
    'network adapter (expresscard)': {'category': ItemCategoryEnum.PERIPHERAL.name, 'device_type': 'USB Adapter'},
    'network adapter (hspa)': {'category': ItemCategoryEnum.PERIPHERAL.name, 'device_type': 'HSPA Adapter'},
    'network adapter (pci)': {'category': ItemCategoryEnum.NETWORK.name, 'device_type': 'PCI Adapter'},
    'network adapter (pcmcia)': {'category': ItemCategoryEnum.PERIPHERAL.name, 'device_type': 'PCMCIA Card'},
    'network adapter (usb)': {'category': ItemCategoryEnum.PERIPHERAL.name, 'device_type': 'Wifi Adapter'},
    'network adapter (wi-fi)': {'category': ItemCategoryEnum.NETWORK.name, 'device_type': 'Wifi Adapter'},
    'network adapter (wifi)': {'category': ItemCategoryEnum.PERIPHERAL.name, 'device_type': 'Wifi Adapter'},
    'network adapter - wireless': {'category': ItemCategoryEnum.PERIPHERAL.name, 'device_type': 'Wifi Adapter'},
    'no value': {'category': ItemCategoryEnum.DISPOSE.name, 'device_type': 'Dispose'},
    'notebook adapter': {'category': ItemCategoryEnum.POWER_SUPPLY.name, 'device_type': 'Charger'},
    'notebook adaptor': {'category': ItemCategoryEnum.POWER_SUPPLY.name, 'device_type': 'Charger'},
    'optical drive': {'category': ItemCategoryEnum.STORAGE.name, 'device_type': 'Optical Drive'},
    'pci adapter': {'category': ItemCategoryEnum.COMPONENT.name, 'device_type': 'PCI Adapter'},
    'perinter - inkjet': {'category': ItemCategoryEnum.PRINTER.name, 'device_type': 'Ink Jet'},
    'phone handset': {'category': ItemCategoryEnum.PHONE.name, 'device_type': 'Handset'},
    'photo copier +50lbs': {'category': ItemCategoryEnum.PRINTER.name, 'device_type': 'Copier'},
    'port replicator': {'category': ItemCategoryEnum.PERIPHERAL.name, 'device_type': 'Port Replicator'},
    'power adapter': {'category': ItemCategoryEnum.POWER_SUPPLY.name, 'device_type': 'Charger'},
    'power adaptor': {'category': ItemCategoryEnum.POWER_SUPPLY.name, 'device_type': 'Charger'},
    'power distribution unit': {'category': ItemCategoryEnum.POWER_SUPPLY.name, 'device_type': 'Power Supply Unit'},
    'power supply module': {'category': ItemCategoryEnum.COMPONENT.name, 'device_type': 'Power Supply Module'},
    'power supply unit': {'category': ItemCategoryEnum.POWER_SUPPLY.name, 'device_type': 'Power Supply Unit'},
    'power tap': {'category': ItemCategoryEnum.POWER_SUPPLY.name, 'device_type': 'Power Tap'},
    'print server': {'category': ItemCategoryEnum.PRINTER.name, 'device_type': 'Print Server'},
    'print server - wireless': {'category': ItemCategoryEnum.PRINTER.name, 'device_type': 'Print Server'},
    'printer': {'category': ItemCategoryEnum.PRINTER.name, 'device_type': 'Printer'},
    'printer (all-in-one)': {'category': ItemCategoryEnum.PRINTER.name, 'device_type': 'MFP'},
    'printer (impact)': {'category': ItemCategoryEnum.PRINTER.name, 'device_type': 'Impact'},
    'printer (inkjet)': {'category': ItemCategoryEnum.PRINTER.name, 'device_type': 'Ink Jet'},
    'printer (label maker)': {'category': ItemCategoryEnum.PRINTER.name, 'device_type': 'Label Maker'},
    'printer (laser)': {'category': ItemCategoryEnum.PRINTER.name, 'device_type': 'Laser'},
    'printer (multifunction)': {'category': ItemCategoryEnum.PRINTER.name, 'device_type': 'MFP'},
    'printer (plotter)': {'category': ItemCategoryEnum.PRINTER.name, 'device_type': 'Plotter'},
    'printer (thermal)': {'category': ItemCategoryEnum.PRINTER.name, 'device_type': 'Thermal'},
    'printer - all-in-one': {'category': ItemCategoryEnum.PRINTER.name, 'device_type': 'MFP'},
    'printer - dot matirx': {'category': ItemCategoryEnum.PRINTER.name, 'device_type': 'Dot Matrix'},
    'printer - dot matrix': {'category': ItemCategoryEnum.PRINTER.name, 'device_type': 'Dot Matrix'},
    'printer - impact': {'category': ItemCategoryEnum.PRINTER.name, 'device_type': 'Impact'},
    'printer - ink': {'category': ItemCategoryEnum.PRINTER.name, 'device_type': 'Ink'},
    'printer - ink jet': {'category': ItemCategoryEnum.PRINTER.name, 'device_type': 'Ink Jet'},
    'printer - inkjet': {'category': ItemCategoryEnum.PRINTER.name, 'device_type': 'Ink Jet'},
    'printer - label maker': {'category': ItemCategoryEnum.PRINTER.name, 'device_type': 'Label Maker'},
    'printer - laser': {'category': ItemCategoryEnum.PRINTER.name, 'device_type': 'Laser'},
    'printer - multifunction': {'category': ItemCategoryEnum.PRINTER.name, 'device_type': 'MFP'},
    'printer - multifuntion': {'category': ItemCategoryEnum.PRINTER.name, 'device_type': 'MFP'},
    'printer - plotter': {'category': ItemCategoryEnum.PRINTER.name, 'device_type': 'Plotter'},
    'printer - thermal': {'category': ItemCategoryEnum.PRINTER.name, 'device_type': 'Thermal'},
    'printer -laser': {'category': ItemCategoryEnum.PRINTER.name, 'device_type': 'Laser'},
    'projector (dlp)': {'category': ItemCategoryEnum.VIDEO.name, 'device_type': 'TV Plasma'},
    'projector (lcd)': {'category': ItemCategoryEnum.VIDEO.name, 'device_type': 'LCD Projector'},
    'projector (led)': {'category': ItemCategoryEnum.VIDEO.name, 'device_type': 'TV Plasma'},
    'psu': {'category': ItemCategoryEnum.POWER_SUPPLY.name, 'device_type': 'Power Supply Unit'},
    'ram (per chip)': {'category': ItemCategoryEnum.STORAGE.name, 'device_type': 'RAM'},
    'ram chip': {'category': ItemCategoryEnum.STORAGE.name, 'device_type': 'RAM'},
    'ram per chip': {'category': ItemCategoryEnum.STORAGE.name, 'device_type': 'RAM'},
    'receiver': {'category': ItemCategoryEnum.AUDIO.name, 'device_type': 'Receiver'},
    'receiver (bt)': {'category': ItemCategoryEnum.AUDIO.name, 'device_type': 'Receiver'},
    'receiver (catv)': {'category': ItemCategoryEnum.VIDEO.name, 'device_type': 'CATV Receiver'},
    'receiver (hdtv)': {'category': ItemCategoryEnum.VIDEO.name, 'device_type': 'HDTV'},
    'receiver (rf)': {'category': ItemCategoryEnum.AUDIO.name, 'device_type': 'Receiver'},
    'remote control': {'category': ItemCategoryEnum.VIDEO.name, 'device_type': 'Remote Control'},
    'replicator port': {'category': ItemCategoryEnum.PERIPHERAL.name, 'device_type': 'Port Replicator'},
    'router': {'category': ItemCategoryEnum.NETWORK.name, 'device_type': 'Router'},
    'router (broadband)': {'category': ItemCategoryEnum.NETWORK.name, 'device_type': 'Router'},
    'router (integrated)': {'category': ItemCategoryEnum.NETWORK.name, 'device_type': 'Router'},
    'router (isr)': {'category': ItemCategoryEnum.NETWORK.name, 'device_type': 'Router'},
    'router (vpn)': {'category': ItemCategoryEnum.NETWORK.name, 'device_type': 'Router'},
    'router - broadband': {'category': ItemCategoryEnum.NETWORK.name, 'device_type': 'Router'},
    'router - network': {'category': ItemCategoryEnum.NETWORK.name, 'device_type': 'Router'},
    'router/ap': {'category': ItemCategoryEnum.NETWORK.name, 'device_type': 'Access Point'},
    'router/nas': {'category': ItemCategoryEnum.STORAGE.name, 'device_type': 'NAS'},
    'scanner': {'category': ItemCategoryEnum.PRINTER.name, 'device_type': 'Scanner'},
    'security appliance': {'category': ItemCategoryEnum.NETWORK.name, 'device_type': 'Security Appliance'},
    'server': {'category': ItemCategoryEnum.COMPUTER.name, 'device_type': 'Server'},
    'server (rackmount)': {'category': ItemCategoryEnum.COMPUTER.name, 'device_type': 'Server'},
    'shredder': {'category': ItemCategoryEnum.SMALL_ELECTRIC_NON_IT.name, 'device_type': 'Shredder'},
    'smartphone': {'category': ItemCategoryEnum.PHONE.name, 'device_type': 'Smartphone'},
    'software': {'category': ItemCategoryEnum.SOFTWARE.name, 'device_type': 'Software'},
    'solid state drive (sata)': {'category': ItemCategoryEnum.STORAGE.name, 'device_type': 'HDD SSD SATA'},
    'sound card': {'category': ItemCategoryEnum.COMPONENT.name, 'device_type': 'Sound Card'},
    'soundbar': {'category': ItemCategoryEnum.AUDIO.name, 'device_type': 'Soundbar'},
    'speaker': {'category': ItemCategoryEnum.AUDIO.name, 'device_type': 'Speaker'},
    'speaker (bluetooth)': {'category': ItemCategoryEnum.AUDIO.name, 'device_type': 'Speaker'},
    'speaker (bookshelf)': {'category': ItemCategoryEnum.AUDIO.name, 'device_type': 'Speaker'},
    'speaker (hi-fi)': {'category': ItemCategoryEnum.AUDIO.name, 'device_type': 'Speaker'},
    'speaker (smart)': {'category': ItemCategoryEnum.AUDIO.name, 'device_type': 'Speaker'},
    'speaker (wireless)': {'category': ItemCategoryEnum.AUDIO.name, 'device_type': 'Speaker'},
    'speaker dock': {'category': ItemCategoryEnum.AUDIO.name, 'device_type': 'Speaker Dock'},
    'speakers': {'category': ItemCategoryEnum.AUDIO.name, 'device_type': 'Speaker'},
    'speakers (2.0)': {'category': ItemCategoryEnum.AUDIO.name, 'device_type': 'Speaker'},
    'speakers (2.1)': {'category': ItemCategoryEnum.AUDIO.name, 'device_type': 'Speaker'},
    'speakers (5.1)': {'category': ItemCategoryEnum.AUDIO.name, 'device_type': 'Speaker'},
    'speakers (hi-fi)': {'category': ItemCategoryEnum.AUDIO.name, 'device_type': 'Hi-Fi'},
    'stereo (bookshelf)': {'category': ItemCategoryEnum.AUDIO.name, 'device_type': 'Speaker'},
    'storage (flash)': {'category': ItemCategoryEnum.STORAGE.name, 'device_type': 'Flash'},
    'storage (nas)': {'category': ItemCategoryEnum.STORAGE.name, 'device_type': 'NAS'},
    'storage (raid)': {'category': ItemCategoryEnum.STORAGE.name, 'device_type': 'RAID'},
    'storage (usb)': {'category': ItemCategoryEnum.STORAGE.name, 'device_type': 'USB'},
    'storage array': {'category': ItemCategoryEnum.STORAGE.name, 'device_type': 'Array'},
    'subwoofer': {'category': ItemCategoryEnum.AUDIO.name, 'device_type': 'Subwoofer'},
    'surge protector': {'category': ItemCategoryEnum.POWER_SUPPLY.name, 'device_type': 'Surge Protector'},
    'switch': {'category': ItemCategoryEnum.NETWORK.name, 'device_type': 'Switch'},
    'switch (desktop)': {'category': ItemCategoryEnum.NETWORK.name, 'device_type': 'Switch'},
    'switch (ethernet)': {'category': ItemCategoryEnum.NETWORK.name, 'device_type': 'Ethernet'},
    'switch (gigabit)': {'category': ItemCategoryEnum.NETWORK.name, 'device_type': 'Switch'},
    'switch (kvm)': {'category': ItemCategoryEnum.PERIPHERAL.name, 'device_type': 'KVM Switch'},
    'switch (network)': {'category': ItemCategoryEnum.NETWORK.name, 'device_type': 'Switch'},
    'switch (rackmount)': {'category': ItemCategoryEnum.NETWORK.name, 'device_type': 'Switch'},
    'switch (vpn)': {'category': ItemCategoryEnum.NETWORK.name, 'device_type': 'Switch'},
    'switch (wemo)': {'category': ItemCategoryEnum.NETWORK.name, 'device_type': 'Switch'},
    'switch - desktop': {'category': ItemCategoryEnum.NETWORK.name, 'device_type': 'Switch'},
    'switch - kvm': {'category': ItemCategoryEnum.PERIPHERAL.name, 'device_type': 'KVM Switch'},
    'switch - rack mount': {'category': ItemCategoryEnum.NETWORK.name, 'device_type': 'Switch'},
    'switch - rackmount': {'category': ItemCategoryEnum.NETWORK.name, 'device_type': 'Switch'},
    'tape drive': {'category': ItemCategoryEnum.STORAGE.name, 'device_type': 'Tape Drive'},
    'telephone': {'category': ItemCategoryEnum.PHONE.name, 'device_type': 'Telephone'},
    'telephone (business)': {'category': ItemCategoryEnum.PHONE.name, 'device_type': 'Business'},
    'telephone (conference)': {'category': ItemCategoryEnum.PHONE.name, 'device_type': 'Conference'},
    'telephone (cordless)': {'category': ItemCategoryEnum.PHONE.name, 'device_type': 'Cordless'},
    'telephone (voip)': {'category': ItemCategoryEnum.PHONE.name, 'device_type': 'VOIP'},
    'telephone - business': {'category': ItemCategoryEnum.PHONE.name, 'device_type': 'Business'},
    'telephone - conference': {'category': ItemCategoryEnum.PHONE.name, 'device_type': 'Conference'},
    'telephone - cordless': {'category': ItemCategoryEnum.PHONE.name, 'device_type': 'Cordless'},
    'telephone - voip': {'category': ItemCategoryEnum.PHONE.name, 'device_type': 'VOIP'},
    'telephone kit': {'category': ItemCategoryEnum.PHONE.name, 'device_type': 'Kit'},
    'telephone receiver': {'category': ItemCategoryEnum.PHONE.name, 'device_type': 'Receiver'},
    'terminal - thin client': {'category': ItemCategoryEnum.COMPUTER.name, 'device_type': 'Thin Client'},
    'toner': {'category': ItemCategoryEnum.PRINTER.name, 'device_type': 'Toner New'},
    'toner (new)': {'category': ItemCategoryEnum.PRINTER.name, 'device_type': 'Toner New'},
    'toner (used)': {'category': ItemCategoryEnum.PRINTER.name, 'device_type': 'Toner'},
    'toner / ink cartridge': {'category': ItemCategoryEnum.PRINTER.name, 'device_type': 'Toner New'},
    'toner/ink cartridge': {'category': ItemCategoryEnum.PRINTER.name, 'device_type': 'Toner New'},
    'tower computer': {'category': ItemCategoryEnum.COMPUTER.name, 'device_type': 'Tower'},
    'tv': {'category': ItemCategoryEnum.VIDEO.name, 'device_type': 'TV'},
    'tv  - plasma': {'category': ItemCategoryEnum.VIDEO.name, 'device_type': 'TV Plasma'},
    'tv (crt)': {'category': ItemCategoryEnum.VIDEO.name, 'device_type': 'CRT'},
    'tv (dlp)': {'category': ItemCategoryEnum.VIDEO.name, 'device_type': 'TV'},
    'tv (lcd)': {'category': ItemCategoryEnum.VIDEO.name, 'device_type': 'LCD'},
    'tv (led)': {'category': ItemCategoryEnum.VIDEO.name, 'device_type': 'LED'},
    'tv (plasma)': {'category': ItemCategoryEnum.VIDEO.name, 'device_type': 'TV Plasma'},
    'tv - crt': {'category': ItemCategoryEnum.VIDEO.name, 'device_type': 'TV CRT'},
    'tv - lcd': {'category': ItemCategoryEnum.VIDEO.name, 'device_type': 'TV LCD'},
    'tv - led': {'category': ItemCategoryEnum.VIDEO.name, 'device_type': 'TV LED'},
    'tv - plasma': {'category': ItemCategoryEnum.VIDEO.name, 'device_type': 'TV Plasma'},
    'tv - rear projection': {'category': ItemCategoryEnum.VIDEO.name, 'device_type': 'TV Projection'},
    'tv stand': {'category': ItemCategoryEnum.VIDEO.name, 'device_type': 'Stand/Mount/Frame Enclosure'},
    'ups': {'category': ItemCategoryEnum.POWER_SUPPLY.name, 'device_type': 'UPS'},
    'usb drive': {'category': ItemCategoryEnum.STORAGE.name, 'device_type': 'USB'},
    'various': {'category': ItemCategoryEnum.ASSORTED.name, 'device_type': 'Various'},
    'video card': {'category': ItemCategoryEnum.COMPONENT.name, 'device_type': 'Video Card'},
    'webcam': {'category': ItemCategoryEnum.PERIPHERAL.name, 'device_type': 'Webcam'},
    'wireless adapter - usb': {'category': ItemCategoryEnum.PERIPHERAL.name, 'device_type': 'Wifi Adapter'},
    'workstation': {'category': ItemCategoryEnum.COMPUTER.name, 'device_type': 'Desktop'}}
