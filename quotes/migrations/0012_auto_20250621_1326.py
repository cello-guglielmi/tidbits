# Generated by Django 5.1.7 on 2025-06-21 16:26

from django.db import migrations, models
from django.utils.text import slugify


def generate_slugs(apps, schema_editor):
    Author = apps.get_model('quotes', 'Author')
    for author in Author.objects.all():
        author.slug = slugify(author.name)
        author.save(update_fields=['slug'])

class Migration(migrations.Migration):

    dependencies = [
        ('quotes', '0011_author_slug_alter_author_name_alter_quote_author'),
    ]

    operations = [
        migrations.RunPython(generate_slugs, migrations.RunPython.noop)
    ]
