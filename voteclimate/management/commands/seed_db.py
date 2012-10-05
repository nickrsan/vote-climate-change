__author__ = 'Nick Santos'

from django.core.management.base import BaseCommand, CommandError
from voteclimate import seed_db

class Command(BaseCommand):
	args = ''
	help = 'runs the seed_db file to load the initial data into the database'

	def handle(self, *args, **options):
		seed_db.seed()
		self.stdout.write("Done - running this again will double up the data\n")