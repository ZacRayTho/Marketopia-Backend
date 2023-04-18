# Generated by Django 4.2 on 2023-04-18 22:13

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('market', '0009_alter_customuser_options_remove_customuser_username_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='location',
            name='name',
        ),
        migrations.AddField(
            model_name='location',
            name='city',
            field=models.CharField(default='Something', max_length=100),
        ),
        migrations.AddField(
            model_name='location',
            name='state',
            field=models.CharField(default='Went Wrong', max_length=100),
        ),
        migrations.AddField(
            model_name='location',
            name='zip',
            field=models.IntegerField(default='0'),
        ),
        migrations.AlterField(
            model_name='listing',
            name='location',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='listing', to='market.location'),
        ),
    ]
