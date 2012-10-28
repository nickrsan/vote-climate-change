__author__ = 'Nick Santos'

from django.core.management.base import BaseCommand, CommandError
from voteclimate import utils

class Command(BaseCommand):
	args = ''
	help = 'Updates urls for candidate photos'

	def handle(self, *args, **options):
		utils._fix_photo_urls(r'C:\Users\Nick\workspace\voteclimate')
		self.stdout.write("Done\n")