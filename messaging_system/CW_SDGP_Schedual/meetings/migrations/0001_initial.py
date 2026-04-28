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
            name='Meeting',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title',        models.CharField(max_length=255)),
                ('meeting_type', models.CharField(
                    choices=[('standup','Stand-up'),('one_on_one','1-on-1'),('review','Review'),
                             ('planning','Planning'),('interview','Interview'),('workshop','Workshop'),('other','Other')],
                    default='other', max_length=20)),
                ('date',        models.DateField()),
                ('start_time',  models.TimeField()),
                ('end_time',    models.TimeField()),
                ('description', models.TextField(blank=True)),
                ('location',    models.CharField(blank=True, max_length=255)),
                ('created_by',  models.ForeignKey(on_delete=django.db.models.deletion.CASCADE,
                                                  related_name='created_meetings', to=settings.AUTH_USER_MODEL)),
                ('attendees',   models.ManyToManyField(blank=True, related_name='attending_meetings', to=settings.AUTH_USER_MODEL)),
            ],
            options={'ordering': ['date', 'start_time']},
        ),
    ]
