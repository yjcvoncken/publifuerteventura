from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.text import slugify

from .models import BlogPost, CommunityApplication


@receiver(post_save, sender=CommunityApplication)
def create_business_story_draft(sender, instance, created, **kwargs):
    """Prepare an editor-reviewed story whenever a business applies."""
    if not created:
        return
    BlogPost.objects.create(
        title=f"Meet {instance.business_name}",
        slug=f"meet-{slugify(instance.business_name)}-{instance.pk}",
        excerpt=f"Introducing {instance.business_name}, a {instance.category.lower()} business based in {instance.location}.",
        content=(
            f"{instance.business_name} has applied to join the Publifuerteventura business community.\n\n"
            f"Based in {instance.location}, the business works in {instance.category}.\n\n"
            f"Their story\n\n{instance.message}\n\n"
            "Editor’s note: Review this draft with the business, add a cover image and refine the story before publishing."
        ),
        post_type=BlogPost.PostType.BUSINESS,
        status=BlogPost.Status.DRAFT,
    )
