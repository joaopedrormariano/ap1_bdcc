# Documentação da AP2

Projeto: **Catálogo / E-commerce** — Django REST evoluído do RestEB para
arquitetura em nuvem (AWS RDS PostgreSQL + S3 + Elastic Beanstalk).

---

## 1. Etapas realizadas

1. **Ponto de partida — RestEB.** Projeto Django REST com um único modelo
   `Produto` (SQLite, mídia local) e deploy no Elastic Beanstalk.

2. **Evolução para e-commerce com carrinho.**
   - Novo modelo `Categoria` e enriquecimento de `Produto` (FK de categoria,
     `estoque`, `ativo`, `atributos` em JSON, `data_atualizacao`).
   - Novo app `pedidos` com `Pedido` (carrinho) e `ItemPedido`.
   - `ViewSets`, `Serializers` e rotas para os novos recursos.
   - Ações de carrinho: `adicionar_item`, `remover_item`, `finalizar`.
   - Registro de todos os modelos no Django Admin.

3. **Migração do banco para PostgreSQL (RDS).**
   - `settings.py` reescrito para usar `django.db.backends.postgresql`.
   - Configuração lida de variáveis de ambiente, com suporte tanto às variáveis
     `RDS_*` (injetadas pelo Elastic Beanstalk) quanto a `POSTGRES_*` (dev local).
   - Adição do driver `psycopg[binary]` ao `requirements.txt`.

4. **Mídia no S3.**
   - Integração com `django-storages` + `boto3`.
   - `STORAGES['default']` apontando para `S3Storage` quando `USE_S3=True`.
   - Pasta lógica `media/` no bucket e URL pública/assinada conforme configuração.

5. **Boas práticas de configuração.**
   - Todos os segredos (chave secreta, banco, credenciais AWS) em variáveis de
     ambiente; nada sensível versionado (`.gitignore` + `.env.example`).
   - `CSRF_TRUSTED_ORIGINS` configurável para o login do Admin em produção.

6. **Deploy e automação.**
   - `.ebextensions/django.config` executa `migrate`, `collectstatic` e
     `criar_admin` no deploy.
   - Comando `criar_admin` (superusuário root não interativo) e `seed_demo`
     (dados de exemplo).
   - Scripts `bootstrap_local.sh` e `build_zip.sh`.

7. **Extensão opcional (JSONB).** Filtros relacionais e dentro do JSON na API,
   incluindo um caso combinado (categoria + atributo do JSON).

8. **Testes.** Suíte com 7 testes cobrindo os filtros JSON e o fluxo de carrinho.

---

## 2. Principais decisões técnicas

- **`RDS_*` como nomes das variáveis do banco.** É o padrão que o Elastic
  Beanstalk injeta quando o RDS é criado junto do ambiente, eliminando
  configuração manual. Mantive `POSTGRES_*` como _fallback_ para o
  desenvolvimento local, e um atalho `USE_SQLITE=True` para rodar/testar sem
  instalar PostgreSQL.

- **`django-storages` em vez de chamar `boto3` na mão.** Integra o upload de
  mídia ao próprio `ImageField`: o código de upload/serving não muda entre
  ambientes — só a configuração (`USE_S3`). Isso mantém as views e serializers
  agnósticos ao destino do arquivo.

- **`STORAGES` (API nova do Django 5.1+/6.0)** em vez do antigo
  `DEFAULT_FILE_STORAGE`, por estar na versão do framework usada (Django 6.0.4).

- **`preco_unitario` como snapshot no `ItemPedido`.** O preço do item é
  congelado no momento em que entra no carrinho, para o histórico do pedido não
  mudar se o preço do produto for alterado depois.

- **Carrinho = `Pedido` com status `ABERTO`.** Evita um modelo separado de
  "carrinho"; finalizar a compra apenas transiciona o status para `PAGO`.

- **`JSONField` para atributos variáveis.** Especificações que mudam por tipo de
  produto (marca, RAM, CPU, cor) ficam em JSON (JSONB no PostgreSQL), enquanto
  dados estruturados e com integridade (preço, estoque, categoria) seguem em
  colunas relacionais.

- **Superusuário via comando idempotente.** `criar_admin` lê
  `DJANGO_SUPERUSER_*` e pode rodar a cada deploy sem duplicar o usuário,
  garantindo o Admin disponível em produção sem passo manual.

---

## 3. Dificuldades e soluções

- **Resposta do carrinho desatualizada em uma etapa.** Como o `ViewSet` usa
  `prefetch_related('itens__produto')`, ao adicionar um item e serializar o
  mesmo objeto, o cache do _prefetch_ ainda refletia o estado anterior (lista
  vazia). **Solução:** após cada alteração, o objeto é relido do banco
  (`get_queryset().get(pk=...)`) antes de serializar, garantindo `itens` e
  `total` corretos na resposta. Coberto por teste.

- **Filtros numéricos dentro do JSON.** Comparar `ram_gb >= 16` exige o lookup
  correto sobre a chave do JSON. **Solução:** `atributos__ram_gb__gte=int(valor)`,
  validando que o parâmetro é numérico antes de aplicar.

- **CSRF no Django Admin atrás de domínio/HTTPS.** Em produção, o login do Admin
  pode falhar com _CSRF verification failed_. **Solução:**
  `CSRF_TRUSTED_ORIGINS` configurável por variável de ambiente
  (`DJANGO_CSRF_TRUSTED_ORIGINS`, com esquema `https://`).

- **Acesso às imagens no S3 (público × privado).** Dependendo da política do
  bucket, as URLs podem retornar 403. **Solução:** chave `AWS_QUERYSTRING_AUTH`
  por variável de ambiente — `False` para URLs públicas (com bucket policy de
  leitura em `media/*`) ou `True` para URLs assinadas em bucket privado.

- **Pacote de deploy limpo.** Evitar enviar `venv`, `db.sqlite3`, `.env` e
  `__pycache__` no `app.zip`. **Solução:** script `build_zip.sh` com exclusões
  explícitas e `.ebignore`.

---

## 4. Como reproduzir rapidamente

```bash
# Local (SQLite, sem AWS):
bash scripts/bootstrap_local.sh
source .venv/bin/activate
python manage.py runserver

# Testes:
USE_SQLITE=True python manage.py test

# Pacote de deploy:
bash scripts/build_zip.sh
```

Detalhes completos de deploy (RDS, S3, EB) e variáveis de ambiente estão no
`README.md`.
