# Generated by Django 4.2.11 on 2024-05-23 19:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('allocation', '0005_auto_20211117_1413'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='historicalallocation',
            options={'get_latest_by': ('history_date', 'history_id'), 'ordering': ('-history_date', '-history_id'), 'verbose_name': 'historical allocation', 'verbose_name_plural': 'historical allocations'},
        ),
        migrations.AlterModelOptions(
            name='historicalallocationattribute',
            options={'get_latest_by': ('history_date', 'history_id'), 'ordering': ('-history_date', '-history_id'), 'verbose_name': 'historical allocation attribute', 'verbose_name_plural': 'historical allocation attributes'},
        ),
        migrations.AlterModelOptions(
            name='historicalallocationattributechangerequest',
            options={'get_latest_by': ('history_date', 'history_id'), 'ordering': ('-history_date', '-history_id'), 'verbose_name': 'historical allocation attribute change request', 'verbose_name_plural': 'historical allocation attribute change requests'},
        ),
        migrations.AlterModelOptions(
            name='historicalallocationattributetype',
            options={'get_latest_by': ('history_date', 'history_id'), 'ordering': ('-history_date', '-history_id'), 'verbose_name': 'historical allocation attribute type', 'verbose_name_plural': 'historical allocation attribute types'},
        ),
        migrations.AlterModelOptions(
            name='historicalallocationattributeusage',
            options={'get_latest_by': ('history_date', 'history_id'), 'ordering': ('-history_date', '-history_id'), 'verbose_name': 'historical allocation attribute usage', 'verbose_name_plural': 'historical allocation attribute usages'},
        ),
        migrations.AlterModelOptions(
            name='historicalallocationchangerequest',
            options={'get_latest_by': ('history_date', 'history_id'), 'ordering': ('-history_date', '-history_id'), 'verbose_name': 'historical allocation change request', 'verbose_name_plural': 'historical allocation change requests'},
        ),
        migrations.AlterModelOptions(
            name='historicalallocationuser',
            options={'get_latest_by': ('history_date', 'history_id'), 'ordering': ('-history_date', '-history_id'), 'verbose_name': 'historical allocation user', 'verbose_name_plural': 'historical Allocation User Status'},
        ),
        migrations.AlterField(
            model_name='historicalallocation',
            name='history_date',
            field=models.DateTimeField(db_index=True),
        ),
        migrations.AlterField(
            model_name='historicalallocationattribute',
            name='history_date',
            field=models.DateTimeField(db_index=True),
        ),
        migrations.AlterField(
            model_name='historicalallocationattributechangerequest',
            name='history_date',
            field=models.DateTimeField(db_index=True),
        ),
        migrations.AlterField(
            model_name='historicalallocationattributetype',
            name='history_date',
            field=models.DateTimeField(db_index=True),
        ),
        migrations.AlterField(
            model_name='historicalallocationattributeusage',
            name='history_date',
            field=models.DateTimeField(db_index=True),
        ),
        migrations.AlterField(
            model_name='historicalallocationchangerequest',
            name='history_date',
            field=models.DateTimeField(db_index=True),
        ),
        migrations.AlterField(
            model_name='historicalallocationuser',
            name='history_date',
            field=models.DateTimeField(db_index=True),
        ),
    ]
