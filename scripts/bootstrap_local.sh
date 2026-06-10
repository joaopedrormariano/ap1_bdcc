#!/usr/bin/env bash
set -e

echo ">> Criando ambiente virtual (.venv)"
python3 -m venv .venv
source .venv/bin/activate

echo ">> Instalando dependencias"
pip install --upgrade pip
pip install -r requirements.txt

if [ ! -f .env ]; then
  export USE_SQLITE=True
  export DJANGO_DEBUG=True
  echo ">> .env nao encontrado: rodando em modo SQLite (dev)."
fi

echo ">> Aplicando migracoes"
python manage.py migrate --noinput

echo ">> Populando dados de demonstracao"
python manage.py seed_demo

echo ">> Criando superusuario admin"
DJANGO_SUPERUSER_USERNAME=${DJANGO_SUPERUSER_USERNAME:-root} \
DJANGO_SUPERUSER_EMAIL=${DJANGO_SUPERUSER_EMAIL:-root@example.com} \
DJANGO_SUPERUSER_PASSWORD=${DJANGO_SUPERUSER_PASSWORD:-Senha123Forte} \
python manage.py criar_admin

echo ""
echo ">> Pronto. Inicie o servidor com:"
echo "   source .venv/bin/activate && python manage.py runserver"
echo "   API:   http://127.0.0.1:8000/api/produtos/"
echo "   Admin: http://127.0.0.1:8000/admin/"
