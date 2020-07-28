# -*- coding: utf-8 -*-
"""
@author = 'ethan'
"""
import sys
from pathlib import Path
import os
import django
from channels.routing import get_default_application

ROOT_DIR = Path(__file__).resolve(strict=True).parent.parent
sys.path.append(str(ROOT_DIR / "couple"))

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
django.setup()
application = get_default_application()
