#!/usr/bin/env bash
echo "[run] install requirements.txt"
pip install -r requirements.txt || exit 1
echo "[run] make migrations"
python3 manage.py makemigrations || exit 1
echo "[run] Migrate DB"
python3 manage.py migrate || exit 1
echo "[run] Create superuser"
echo "from django.contrib.auth import get_user_model
User = get_user_model()
if not User.objects.filter(is_superuser=True).exists():
    user = User()
    user.first_name = 'Admin'
    user.last_name = 'Dev'
    user.is_superuser = True
    user.is_staff = True
    user.set_password('qwerty123')
    user.email = 'omarbustosmenas@gmail.com'
    user.save()

" | python3 manage.py shell || exit 1

echo "[run] runserver with django"
python3 manage.py runserver 0.0.0.0:8000
