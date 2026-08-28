from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [("directory", "0028_business_homepage_size")]

    operations = [
        migrations.RemoveField(model_name="business", name="rating"),
        migrations.RemoveField(model_name="business", name="review_count"),
        migrations.AlterField(
            model_name="business",
            name="price_label",
            field=models.CharField(
                blank=True,
                help_text="Optional short price note, such as 'From €25' or 'Free'. It is not currently displayed on the website.",
                max_length=40,
            ),
        ),
    ]
