# Generated by Django 4.2.2 on 2023-06-27 20:24

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('compraventa', '0004_alter_producto_modelo'),
    ]

    operations = [
        migrations.AddField(
            model_name='pedido',
            name='fecha_pedido',
            field=models.DateTimeField(default='2023-1-1'),
        ),
        migrations.RemoveField(
            model_name='pedido',
            name='productos',
        ),
        migrations.AddField(
            model_name='pedido',
            name='productos',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.DO_NOTHING, to='compraventa.producto'),
        ),
    ]
