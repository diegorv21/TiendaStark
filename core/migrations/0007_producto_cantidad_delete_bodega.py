# Generated by Django 4.0.5 on 2022-07-07 18:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0006_producto_imagen'),
    ]

    operations = [
        migrations.AddField(
            model_name='producto',
            name='cantidad',
            field=models.CharField(max_length=80, null=True, verbose_name='Cantidad'),
        ),
        migrations.DeleteModel(
            name='Bodega',
        ),
    ]
