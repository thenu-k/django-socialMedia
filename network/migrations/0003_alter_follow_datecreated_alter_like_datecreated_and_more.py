# Generated by Django 4.1.7 on 2023-02-25 11:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('network', '0002_alter_post_datecreated'),
    ]

    operations = [
        migrations.AlterField(
            model_name='follow',
            name='dateCreated',
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='like',
            name='dateCreated',
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='post',
            name='dateCreated',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
    ]