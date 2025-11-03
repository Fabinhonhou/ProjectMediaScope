# Em analytics/forms.py (CRIE ESTE ARQUIVO)
from django import forms
from .models import Profile

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        # Quais campos do modelo devem aparecer no formulário
        fields = ['youtube_channel_id', 'default_video_id']
        # Nomes "amigáveis" para os campos
        labels = {
            'youtube_channel_id': 'ID do seu Canal no YouTube',
            'default_video_id': 'ID do Vídeo para o Gráfico',
        }