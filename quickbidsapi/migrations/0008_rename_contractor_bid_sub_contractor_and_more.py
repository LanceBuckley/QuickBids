# Generated by Django 4.2.5 on 2023-09-15 14:31

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('quickbidsapi', '0007_rename_request_bid_is_request'),
    ]

    operations = [
        migrations.RenameField(
            model_name='bid',
            old_name='contractor',
            new_name='sub_contractor',
        ),
        migrations.AddField(
            model_name='bid',
            name='primary_contractor',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='my_requests', to='quickbidsapi.contractor'),
            preserve_default=False,
        ),
    ]
