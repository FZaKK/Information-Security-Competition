python manage.py makemigrations && ^
python manage.py migrate && ^
python .\manage.py clear_sql &&^
python .\manage.py import_sql &&^
python manage.py runserver 0.0.0.0:8000