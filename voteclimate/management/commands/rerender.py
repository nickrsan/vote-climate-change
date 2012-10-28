__author__ = 'Nick Santos'

from django.core.management.base import BaseCommand, CommandError
from voteclimate import utils

class Command(BaseCommand):
	args = ''
	help = 'Rerenders all of the cached statements in the database'

	def handle(self, *args, **options):
		utils._rerender_statements()
		self.stdout.write("Done\n")