# Generated by Django 4.2.2 on 2023-07-07 15:12

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('compraventa', '0003_producto_descripcion_alter_itempedido_cantidad'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pedido',
            name='cliente_solicitante',
            field=models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='compraventa.cliente'),
        ),
    ]
