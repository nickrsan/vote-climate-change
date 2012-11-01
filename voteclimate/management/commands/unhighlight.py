__author__ = 'Nick Santos'

from django.core.management.base import BaseCommand, CommandError
from voteclimate import utils

class Command(BaseCommand):
	args = ''
	help = 'Unsets the highlight attribute on the specified statement ids'

	def handle(self, *args, **options):
		for statement_id in args:
			status = utils._unhighlight_statement(statement_id)
			if status is False:
				print "Statement was not highlighted"

		self.stdout.write("Done - Highlight removed\n")