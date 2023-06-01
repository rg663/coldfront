# Generated by Django 3.2.17 on 2023-06-01 17:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('grant', '0002_auto_20230406_1310'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='historicalgrant',
            options={'get_latest_by': ('history_date', 'history_id'), 'ordering': ('-history_date', '-history_id'), 'verbose_name': 'historical grant', 'verbose_name_plural': 'historical Grants'},
        ),
        migrations.AlterField(
            model_name='historicalgrant',
            name='history_date',
            field=models.DateTimeField(db_index=True),
        ),
    ]
