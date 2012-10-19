__author__ = 'Nick'

import os
os.environ['DJANGO_SETTINGS_MODULE'] = r'vote_climate.settings'
from voteclimate import utils

utils._fix_photo_urls(r'C:\Users\Nick\workspace\voteclimate')