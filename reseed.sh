bash ./reset_db.sh
echo 'Deleted Database'
python manage.py syncdb
echo 'Recreated Database - Adding Data'
python manage.py seed_db
python manage.py dumpdata > .\voteclimate\fixtures\dumped.json
