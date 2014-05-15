import os
import logging

from fabric.api import run, local, sudo, prompt, reboot

checkpoint_file = os.path.join(os.getcwd(),".voteclimate_fabric_checkpoint_file.txt")

def log(message):
	print message


def check_result(result, item):
	if result.failed:
		log("%s install FAILED" % item)
	else:
		log("%s install successful" % item)


def _write_checkpoint(number):
	checkpoints = open(checkpoint_file, 'w')
	checkpoints.write(number)
	checkpoints.close()


def linux_setup():
	""" setup is split into checkpoints so that we can resume, but also so that we can reboot the server and then resume.
	Each checkpoint is responsible for initiating the next one
	"""

	checkpoints = open(checkpoint_file, 'r')
	checkpoint = checkpoints.readline()
	checkpoints.close()

	if checkpoint is None:
		log("Starting at the beginning")
		_checkpoint_initial()
	if checkpoint == 1:
		log("Resuming at Checkpoint 1")
		_checkpoint_one()

	branch = prompt("staging or release?", default="release", validate=str)


def _checkpoint_initial():
	log("Updating server OS")
	check_result(sudo("apt-get update"), "apt-get update")
	check_result(sudo("apt-get dist-upgrade"), "apt-get dist-upgrade")
	check_result(sudo("apt-get autoremove"), "apt-get autoremove")
	log("Rebooting")
	reboot()

	_write_checkpoint(1)
	_checkpoint_one()


def _checkpoint_one():
	log("Configuring firewall")
	check_result(sudo("ufw disable"), "disable firewall temporarily")  # disable firewall before remaining config so that if something fails, we don't get locked out
	check_result(local("ufw allow 22"), "firewall port 22")
	check_result(local("ufw allow 80"), "firewall port 80")
	check_result(local("ufw allow 443"), "firewall port 443")
	check_result(sudo("ufw enable"), "enable firewall")

	log("Installing python packages")
	check_result(local("apt-get install python-pip"), "pip")
	check_result(local("pip install django"), "django")
	check_result(local("pip install gunicorn"), "gunicorn")
	# TODO: Later, make sure to read the dependencies file and install anything listed there

	_write_checkpoint(2)