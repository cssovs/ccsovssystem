cmd /c py manage.py makemigrations settings && py manage.py makemigrations election && py manage.py makemigrations post && py manage.py makemigrations party && py manage.py migrate && py manage.py createsuperuser