# Generated by Django 3.1.3 on 2020-12-01 12:10

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0003_bucketlist_bucketlistitem'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='bucketlistitem',
            unique_together=None,
        ),
        migrations.RemoveField(
            model_name='bucketlistitem',
            name='bucketlist',
        ),
        migrations.DeleteModel(
            name='Bucketlist',
        ),
        migrations.DeleteModel(
            name='BucketlistItem',
        ),
    ]
