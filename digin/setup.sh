# cat create_db.sql | python manage.py dbshell
cat create_user.sql | python manage.py dbshell
cat create_token.sql | python manage.py dbshell
cat create_polls.sql | python manage.py dbshell

python manage.py makemigrations
python manage.py migrate sessions