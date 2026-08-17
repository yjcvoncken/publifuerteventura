from django.db import migrations, models


def rewrite_posts(apps, schema_editor):
    BlogPost = apps.get_model("directory", "BlogPost")
    posts = list(BlogPost.objects.order_by("id"))
    examples = [
        {
            "title": "How to get more customers for your Fuerteventura business",
            "slug": "get-more-customers-fuerteventura-business",
            "excerpt": "A practical local marketing plan for Fuerteventura businesses that want to be discovered by residents and visitors ready to buy.",
            "content": "Customers already search online for services in Fuerteventura. The opportunity is making sure your business appears when their need is strongest.\n\nStart with a clear description of what you offer and where you work. Use specific phrases such as plumber in Corralejo, yoga classes in Lajares or property maintenance in Fuerteventura. These phrases help search engines connect your business with relevant local searches.\n\nConsistency builds trust. Keep your business name, contact details, opening hours and location accurate everywhere you appear online. Add recent photographs and ask satisfied customers for honest reviews.\n\nA paid Publifuerteventura partner listing puts your company inside a curated local platform designed around service searches. It also gives your business an additional relevant presence online, helping potential customers understand what you do and contact you with confidence.",
            "post_type": "marketing",
            "focus_keyword": "how to get more customers in Fuerteventura",
            "meta_title": "How to Get More Customers in Fuerteventura",
            "meta_description": "Local marketing advice for Fuerteventura businesses that want more online visibility, enquiries and customers.",
        },
        {
            "title": "Local SEO for Fuerteventura businesses: a practical guide",
            "slug": "local-seo-fuerteventura-businesses",
            "excerpt": "Learn how local SEO helps island businesses appear when customers search for services in Corralejo, Lajares, El Cotillo and across Fuerteventura.",
            "content": "Local SEO is the work that helps a business appear in location-based searches. For an island company, that means being visible when someone searches for your service together with Fuerteventura or a town such as Corralejo.\n\nChoose one main service and location for each page on your website. Explain the work in natural language, answer common customer questions and include clear contact information. Avoid repeating keywords unnaturally; useful detail is more valuable than volume.\n\nBuild local relevance through accurate directory listings, genuine reviews and links from trusted Fuerteventura websites. A relevant listing tells search engines that your business is connected to the place and service it claims to serve.\n\nPublifuerteventura is built specifically around finding island services. Paid partners receive a focused business profile and can be included in useful editorial stories created to attract relevant local searches over time.",
            "post_type": "seo",
            "focus_keyword": "local SEO Fuerteventura businesses",
            "meta_title": "Local SEO for Fuerteventura Businesses | Guide",
            "meta_description": "A practical guide to local SEO for businesses in Fuerteventura, including visibility, listings, reviews and location keywords.",
        },
    ]
    for post, data in zip(posts, examples):
        for field, value in data.items():
            setattr(post, field, value)
        post.save()
    BlogPost.objects.filter(post_type__in=["news", "guide"]).update(post_type="marketing")


class Migration(migrations.Migration):
    dependencies = [("directory", "0005_blogpost_post_type")]
    operations = [
        migrations.AddField(model_name="blogpost", name="focus_keyword", field=models.CharField(blank=True, help_text="Main search phrase this article should target.", max_length=160)),
        migrations.AddField(model_name="blogpost", name="meta_description", field=models.CharField(blank=True, help_text="SEO description shown in search results. Leave blank to use the excerpt.", max_length=320)),
        migrations.AddField(model_name="blogpost", name="meta_title", field=models.CharField(blank=True, help_text="SEO page title. Leave blank to use the article title.", max_length=160)),
        migrations.AlterField(model_name="blogpost", name="post_type", field=models.CharField(choices=[("marketing", "Business marketing"), ("seo", "Local SEO"), ("business", "Business spotlight")], default="marketing", max_length=12)),
        migrations.RunPython(rewrite_posts, migrations.RunPython.noop),
    ]
