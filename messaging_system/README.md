For a super user you will have to:

python manage.py createsuperuser

and create one

to load the server it is:

cd messaging_system
python manage.py migrate
python manage.py runserver