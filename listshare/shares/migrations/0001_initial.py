# Generated by Django 4.1.7 on 2023-03-23 23:31

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='auth_user',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=50, unique=True)),
                ('email', models.CharField(max_length=50, unique=True)),
                ('password', models.CharField(max_length=50)),
                ('balance', models.DecimalField(decimal_places=2, max_digits=10)),
            ],
            options={
                'db_table': 'userprofle',
            },
        ),
        migrations.CreateModel(
            name='Share',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ticker', models.CharField(max_length=10, unique=True)),
                ('price', models.DecimalField(decimal_places=2, max_digits=10)),
            ],
            options={
                'db_table': 'share',
            },
        ),
        migrations.CreateModel(
            name='Transaction',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('transaction_type', models.CharField(choices=[('BUY', 'Buy'), ('SELL', 'Sell')], max_length=4)),
                ('quantity', models.IntegerField()),
                ('price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('transaction_date', models.DateTimeField(auto_now_add=True)),
                ('share', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='shares.share')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='shares.auth_user')),
            ],
            options={
                'db_table': 'Transaction',
            },
        ),
        migrations.CreateModel(
            name='Portfolio',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.IntegerField()),
                ('purchase_price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('purchase_date', models.DateTimeField(auto_now_add=True)),
                ('share', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='shares.share')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='shares.auth_user')),
            ],
            options={
                'db_table': 'Portfolio',
            },
        ),
    ]
