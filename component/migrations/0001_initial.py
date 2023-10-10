# Generated by Django 3.1.5 on 2023-07-05 09:17

import component.models
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Component',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=128)),
                ('detail', models.TextField(blank=True)),
                ('image', models.ImageField(blank=True, upload_to=component.models.get_path)),
                ('type', models.IntegerField(choices=[(0, 'Development Boards'), (1, 'Sensors and Electronic Components'), (2, 'Motors and Motor Drivers'), (3, 'Tools'), (4, 'Power and Battery'), (5, 'Transmitter and Receiver'), (6, 'Miscellaneous')], default=6)),
                ('max_num', models.IntegerField(default=0)),
                ('issued_num', models.IntegerField(default=0)),
                ('issued_members', models.ManyToManyField(blank=True, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Request',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.IntegerField(choices=[(0, 'Pending'), (1, 'Accepted'), (2, 'Rejected')], default=0)),
                ('request_num', models.IntegerField(default=0)),
                ('user_confirmation', models.BooleanField(default=False)),
                ('time_confirmation', models.DateTimeField(blank=True, null=True)),
                ('reason', models.TextField(blank=True, default='', max_length=128, null=True)),
                ('component', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='component.component')),
                ('request_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]