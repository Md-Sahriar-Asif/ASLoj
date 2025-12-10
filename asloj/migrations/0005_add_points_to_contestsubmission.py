from django.db import migrations, models

class Migration(migrations.Migration):

    dependencies = [
        ('asloj', '0004_auto_20251208_1923'),
    ]

    operations = [
        migrations.AddField(
            model_name='contestsubmission',
            name='points',
            field=models.IntegerField(default=0),
        ),
    ]
