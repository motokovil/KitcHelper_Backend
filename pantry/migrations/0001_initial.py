# Generated by Django 2.2.14 on 2021-03-30 20:21

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Pantry',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=200)),
                ('precio', models.IntegerField()),
                ('init', models.IntegerField()),
                ('current', models.IntegerField()),
                ('medida', models.CharField(choices=[('lt', 'Litro'), ('gr', 'Gramo'), ('ml', 'Mililitro'), ('un', 'Unidad'), ('kg', 'Kilogramo')], default='gr', max_length=2)),
                ('pantry', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='pantry.Pantry')),
            ],
        ),
        migrations.CreateModel(
            name='ShoppingList',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('titulo', models.CharField(max_length=200)),
                ('descripcion', models.TextField(max_length=400)),
                ('activa', models.BooleanField(default=True)),
                ('pantry', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='pantry.Pantry')),
            ],
        ),
        migrations.CreateModel(
            name='ShoppingItem',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('titulo', models.CharField(max_length=200)),
                ('cantidad', models.IntegerField()),
                ('precio', models.IntegerField(blank=True, null=True)),
                ('lista', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='pantry.ShoppingList')),
                ('producto', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='pantry.Product')),
            ],
        ),
    ]
