del voteclimate.sqlite
echo 'Deleted Database'
python manage.py syncdb --noinput
echo 'Recreated Database - Adding Data'
python manage.py seed_db
python manage.py dumpdata > .\voteclimate\fixtures\dumped.json
