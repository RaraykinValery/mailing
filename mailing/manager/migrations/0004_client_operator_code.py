# Generated by Django 4.1.4 on 2023-01-20 14:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('manager', '0003_remove_client_operator_code'),
    ]

    operations = [
        migrations.AddField(
            model_name='client',
            name='operator_code',
            field=models.CharField(default='000', editable=False, max_length=3, verbose_name='Код оператора'),
            preserve_default=False,
        ),
    ]
