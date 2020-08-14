# Generated by Django 3.0.8 on 2020-07-22 15:32

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('network', '0003_fpost'),
    ]

    operations = [
        migrations.RenameField(
            model_name='post',
            old_name='likes',
            new_name='num_likes',
        ),
        migrations.CreateModel(
            name='Like',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('post', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='likes', to='network.Post')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='liked', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]