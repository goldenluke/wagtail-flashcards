from django.contrib.auth.models import Group, Permission
from django.db.models.signals import post_save
from django.dispatch import receiver
from wagtail.models import GroupPagePermission
from flashcards.models import Box, RootPage
from django.contrib.auth.models import User

import logging

logger = logging.getLogger(__name__)

@receiver(post_save, sender=User)
def create_user_box_and_permissions(sender, instance, created, **kwargs):
    """
    Automatically creates a Box for new users, adds them to the Player group,
    and grants them "add" permission to their Box.
    """
    if created:  # Only execute when the user is created
        logger.info(f"Creating Box for user: {instance.username}")

        # Step 1: Retrieve the RootPage
        root_page = RootPage.objects.first()
        if not root_page:
            logger.error("No RootPage found. Ensure that a RootPage is configured.")
            return

        # Step 2: Create a Box for the user
        try:
            user_box = Box(title=f"{instance.username} Folders", owner=instance)
            root_page.add_child(instance=user_box)  # Add Box as a child of RootPage
            user_box.save_revision().publish()  # Publish the Box
            logger.info(f"Box successfully created for {instance.username}: ID {user_box.id}")
        except Exception as e:
            logger.error(f"Error creating Box for {instance.username}: {e}")
            return

        # Step 3: Add the user to the Player group
        try:
            player_group, created = Group.objects.get_or_create(name="Player")
            instance.groups.add(player_group)
            instance.save()
            logger.info(f"User {instance.username} added to group 'Player'")
        except Exception as e:
            logger.error(f"Error adding {instance.username} to group 'Player': {e}")

        # Step 4: Grant "add" permission to the user's Box
        try:
            # Fetch the Wagtail permission for "add"
            add_permission = Permission.objects.get(codename="add_page")

            # Assign the permission to the group on the Box
            GroupPagePermission.objects.get_or_create(
                group=player_group,
                page=user_box,
                permission=add_permission,
            )
            logger.info(f"Granted 'add' permission to the Player group for Box {user_box.title}")
        except Exception as e:
            logger.error(f"Error granting permissions to Box {user_box.title}: {e}")
