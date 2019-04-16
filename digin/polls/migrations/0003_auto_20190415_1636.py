# Generated by Django 2.1.7 on 2019-04-15 16:36

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0002_auto_20190329_2328'),
    ]

    operations = [
        migrations.AddField(
            model_name='choice',
            name='address',
            field=models.CharField(default=django.utils.timezone.now, max_length=200),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='choice',
            name='latitude',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='choice',
            name='longitude',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='choice',
            name='phone',
            field=models.CharField(blank=True, max_length=200),
        ),
        migrations.AddField(
            model_name='choice',
            name='place_id',
            field=models.CharField(default=0, max_length=200),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='choice',
            name='price_level',
            field=models.IntegerField(blank=True, default=2),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='choice',
            name='rating',
            field=models.IntegerField(default=3),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='choice',
            name='reviews',
            field=models.CharField(default='', max_length=2000),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='choice',
            name='website',
            field=models.CharField(blank=True, max_length=200),
        ),
    ]
