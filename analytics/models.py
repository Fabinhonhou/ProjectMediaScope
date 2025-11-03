# Em analytics/models.py
from django.db import models
from django.contrib.auth.models import User # Importa o usuário padrão do Django

class Profile(models.Model):
    # Cria um link direto e obrigatório com um usuário
    # Se o usuário for deletado, o perfil também será (models.CASCADE)
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    # O campo que vai guardar o ID do canal do YouTube
    youtube_channel_id = models.CharField(max_length=100, blank=True, null=True)

    # Vamos também guardar o ID do vídeo que queremos no gráfico
    default_video_id = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return f"Perfil de {self.user.username}"