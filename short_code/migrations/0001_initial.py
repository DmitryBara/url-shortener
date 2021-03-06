# Generated by Django 3.1.3 on 2021-09-27 14:45

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='DynamicConfig',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(choices=[('current_initial_parameters_id', 'Current Initial Parameters Id')], max_length=30, unique=True)),
                ('value', models.CharField(max_length=30)),
            ],
        ),
        migrations.CreateModel(
            name='ShortCode',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('short_code', models.CharField(max_length=30, unique=True)),
                ('full_url', models.URLField(max_length=300)),
                ('redirect_count', models.IntegerField()),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('last_redirect_at', models.DateTimeField(blank=True, null=True)),
            ],
            options={
                'ordering': ('-created_at',),
            },
        ),
        migrations.CreateModel(
            name='InitialParametersState',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('alphabet_sorted', models.CharField(max_length=300)),
                ('requested_short_code_length', models.IntegerField()),
                ('min_number_from_range', models.BigIntegerField()),
                ('max_number_from_range', models.BigIntegerField()),
                ('last_number_converted_to_short_code', models.BigIntegerField()),
            ],
            options={
                'unique_together': {('alphabet_sorted', 'requested_short_code_length')},
            },
        ),
    ]
