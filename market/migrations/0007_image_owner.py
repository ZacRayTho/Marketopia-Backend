# Generated by Django 4.2 on 2023-04-14 15:04

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('market', '0006_listing'),
    ]

    operations = [
        migrations.CreateModel(
            name='Image',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pic', models.URLField()),
                ('owner', models.ForeignKey( on_delete=django.db.models.deletion.CASCADE, related_name='Image', to='market.listing'))
            ],
        ),
        # migrations.AddField(
        #     model_name='image',
        #     name='owner',
        #     field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='Image', to='market.listing'),
        # ),
    ]