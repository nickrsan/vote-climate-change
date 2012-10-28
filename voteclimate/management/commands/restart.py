__author__ = 'Nick Santos'

from django.core.management.base import BaseCommand, CommandError
import subprocess


class Command(BaseCommand):
	args = ''
	help = '''runs the shell script that touches the restart.txt file to tell passenger to restart
		   the application'''

	def handle(self, *args, **options):
		subprocess.call('/home/voteclimatechange/voteclimatechange.com/restart.sh')
		self.stdout.write("Ran shell script - passenger set to restart\nThis command does not check that the file was successfully touched, so if you must be sure, check ./tmp/restart.txt")