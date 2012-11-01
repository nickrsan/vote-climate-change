__author__ = 'Nick Santos'

from django.core.management.base import BaseCommand, CommandError
from voteclimate import utils

class Command(BaseCommand):
	args = ''
	help = 'Sets the highlight attribute on the specified statement ids'

	def handle(self, *args, **options):
		for statement_id in args:
			utils._highlight_statement(statement_id)

		self.stdout.write("Done - Highlighted\n")