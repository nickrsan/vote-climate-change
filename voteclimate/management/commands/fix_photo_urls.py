__author__ = 'Nick Santos'

from django.core.management.base import BaseCommand, CommandError
from voteclimate import utils

import os

class Command(BaseCommand):
	args = ''
	help = 'Updates urls for candidate photos'

	def handle(self, *args, **options):
		path = os.getcwd()
		utils._fix_photo_urls(path)
		self.stdout.write("Done\n")