__author__ = 'Nick Santos'

from django.core.management.base import BaseCommand, CommandError
from voteclimate.utils import make_acknowledgements_page

class Command(BaseCommand):
	args = ''
	help = 'makes the acknowledgements page'

	def handle(self, *args, **options):
		make_acknowledgements_page()
		self.stdout.write("Done\n")