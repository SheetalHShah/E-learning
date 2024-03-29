# Generated by Django 3.2.5 on 2022-01-17 09:26

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0010_alter_transaction_checksum'),
    ]

    operations = [
        migrations.CreateModel(
            name='review',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('r_name', models.CharField(max_length=50)),
                ('r_email', models.EmailField(max_length=50)),
                ('r_content', models.CharField(max_length=1000)),
                ('course_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.course1')),
                ('student_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.student1')),
            ],
        ),
    ]
