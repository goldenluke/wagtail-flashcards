from django.contrib.auth.models import Group
from django.db.models.signals import post_save
from django.dispatch import receiver
from wagtail.models import GroupPagePermission, Page
from flashcards.models import Box, RootPage
from django.contrib.auth.models import User

import logging

logger = logging.getLogger(__name__)

@receiver(post_save, sender=User)
def create_user_box_and_permissions(sender, instance, created, **kwargs):
    """
    Cria um Box automaticamente para o novo usuário, associa o usuário ao grupo "Player"
    e configura permissões de página.
    """
    if created:  # Apenas quando o usuário é criado
        logger.info(f"Criando Box para o usuário {instance.username}")

        # Verificar RootPage
        root_page = RootPage.objects.first()
        if not root_page:
            logger.error("Nenhuma RootPage encontrada. Certifique-se de que uma RootPage está configurada corretamente.")
            return

        # Criar o Box e associá-lo ao usuário
        try:
            user_box = Box(title=f"{instance.username} Folders", owner=instance)
            root_page.add_child(instance=user_box)  # Adiciona o Box como filho da RootPage
            user_box.save_revision().publish()  # Publica o Box
            logger.info(f"Box criado com sucesso para {instance.username}: ID {user_box.id}")
        except Exception as e:
            logger.error(f"Erro ao criar Box para {instance.username}: {e}")
            return

        # Adicionar o usuário ao grupo "Player"
        try:
            player_group, group_created = Group.objects.get_or_create(name="Player")
            instance.groups.add(player_group)
            instance.save()
            logger.info(f"Usuário {instance.username} adicionado ao grupo 'Player'")
        except Exception as e:
            logger.error(f"Erro ao adicionar {instance.username} ao grupo 'Player': {e}")
