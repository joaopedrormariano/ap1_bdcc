import django.db.models.deletion
from django.db import migrations, models

class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('produtos', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Pedido',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cliente_nome', models.CharField(max_length=200)),
                ('cliente_email', models.EmailField(blank=True, max_length=254)),
                ('status', models.CharField(choices=[('ABERTO', 'Aberto (carrinho)'), ('PAGO', 'Pago'), ('ENVIADO', 'Enviado'), ('CANCELADO', 'Cancelado')], default='ABERTO', max_length=10)),
                ('criado_em', models.DateTimeField(auto_now_add=True)),
                ('atualizado_em', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name': 'Pedido',
                'verbose_name_plural': 'Pedidos',
                'ordering': ['-criado_em'],
            },
        ),
        migrations.CreateModel(
            name='ItemPedido',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantidade', models.PositiveIntegerField(default=1)),
                ('preco_unitario', models.DecimalField(decimal_places=2, max_digits=10)),
                ('produto', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='itens_pedido', to='produtos.produto')),
                ('pedido', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='itens', to='pedidos.pedido')),
            ],
            options={
                'verbose_name': 'Item do Pedido',
                'verbose_name_plural': 'Itens do Pedido',
                'unique_together': {('pedido', 'produto')},
            },
        ),
    ]
