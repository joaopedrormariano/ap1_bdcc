# Catálogo de Produtos — Big Data e Cloud Computing (2026.1)

API REST desenvolvida em Django + Django REST Framework para gerenciamento de um catálogo de produtos e suas categorias, com deploy na AWS Elastic Beanstalk.

## 🔗 Link do projeto publicado

**API:** http://catalogo-produtos-env.eba-fsihtxex.us-east-1.elasticbeanstalk.com

- **Health check:** `/`
- **Produtos:** `/api/produtos/`
- **Categorias:** `/api/categorias/`
- **Admin:** `/admin/` (usuário: `admin`)

## 👥 Integrantes do grupo

- João Pedro Mariano
- Rafael Viana
- Hannah Martins
- Kauan Pessanha
- Guilherme Valim

## 🆕 Alterações realizadas nesta entrega

### Nova classe `Categoria`
Criada em `produtos/models.py` com os campos:
- `nome` (CharField, único)
- `descricao` (TextField)
- `data_criacao` (DateTimeField)

### Relacionamento com `Produto`
Adicionado um `ForeignKey` de `Produto` para `Categoria`:
- `on_delete=PROTECT` — impede apagar categoria com produtos vinculados
- `related_name='produtos'` — permite acessar `categoria.produtos.all()`

### Novos endpoints
- `GET/POST /api/categorias/` — lista/cria categorias
- `GET/PUT/DELETE /api/categorias/<id>/` — detalhe/edita/deleta
- `GET /api/produtos/` — agora retorna também `categoria` (id) e `categoria_nome`

### Outras mudanças
- `produtos/admin.py` registra `Produto` e `Categoria` no Django admin.
- `.ebextensions/01_django.config` executa migrate, collectstatic e criação de superuser automática no deploy.

## 💻 Executando localmente

### 1. Pré-requisitos
- Python 3.12
- Git

### 2. Clone e configure o ambiente

```bash
git clone https://github.com/joaopedrormariano/ap1_bdcc.git
cd app.zip

python -m venv venv
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

pip install -r requirements.txt
```

### 3. Banco e superuser

```bash
python manage.py migrate
python manage.py createsuperuser
```

### 4. Servidor

```bash
python manage.py runserver
```

Acesse:
- http://127.0.0.1:8000/api/produtos/
- http://127.0.0.1:8000/api/categorias/
- http://127.0.0.1:8000/admin/

## 🚀 Deploy na AWS Elastic Beanstalk

### Pré-requisitos
- Conta AWS com policy `AdministratorAccess-AWSElasticBeanstalk` no usuário.
- Roles criadas: `aws-elasticbeanstalk-service-role` (uso: Environment) e `aws-elasticbeanstalk-ec2-role` (uso: Compute).

### Etapas executadas

1. **Criação das roles IAM** (IAM → Roles → Create role → AWS service → Elastic Beanstalk → escolher Environment ou Compute).
2. **Geração do zip compatível com Linux** usando Python (pois `Compress-Archive` do PowerShell gera zip com backslashes que o `unzip` do Linux rejeita):
   ```bash
   python -c "import zipfile, os; from pathlib import Path; \
   zf=zipfile.ZipFile('app-linux.zip','w',zipfile.ZIP_DEFLATED); \
   [zf.write(os.path.join(d,f), os.path.relpath(os.path.join(d,f),'.').replace(os.sep,'/')) \
   for item in ['.ebextensions','catalogo','produtos','manage.py','Procfile','requirements.txt'] \
   for d,_,fs in os.walk(item) if os.path.isdir(item) for f in fs if '__pycache__' not in d and not f.endswith('.pyc')]; \
   [zf.write(f, f) for f in ['manage.py','Procfile','requirements.txt']]; zf.close()"
   ```
3. **Criação da aplicação no EB Console:**
   - Application name: `catalogo-produtos`
   - Platform: Python 3.12 (Amazon Linux 2023)
   - Upload do `app-linux.zip`
4. **Configuração do ambiente:**
   - VPC padrão, IP público habilitado
   - Tipo: Instância única, `t2.micro`, sob demanda, x86_64
   - Environment properties:
     - `DJANGO_SETTINGS_MODULE=catalogo.settings`
     - `DJANGO_DEBUG=False`
     - `DJANGO_ALLOWED_HOSTS=.elasticbeanstalk.com`
     - `DJANGO_SUPERUSER_USERNAME=admin`
     - `DJANGO_SUPERUSER_EMAIL=admin@admin.com`
     - `DJANGO_SUPERUSER_PASSWORD=[senha]`
5. **Container commands** (em `.ebextensions/01_django.config`):
   - `migrate --noinput`
   - `collectstatic --noinput`
   - `createsuperuser --noinput`