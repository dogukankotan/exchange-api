# Generated by Django 3.2.11 on 2022-01-23 00:05

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('shares', '0002_alter_share_symbol'),
        ('exchange', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Market',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.DecimalField(decimal_places=2, max_digits=32)),
                ('rate', models.DecimalField(decimal_places=2, max_digits=32)),
                ('flow', models.PositiveIntegerField(choices=[(1, 'sell'), (2, 'buy')], null=True)),
                ('share', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='shares.share')),
            ],
        ),
        migrations.DeleteModel(
            name='Register',
        ),
        migrations.AddField(
            model_name='transaction',
            name='market',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='exchange.market'),
            preserve_default=False,
        ),
    ]
