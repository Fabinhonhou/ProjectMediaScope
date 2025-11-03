# Em analytics/views.py
from django.shortcuts import render, redirect
# from django.contrib.auth.decorators import login_required # <-- COMENTE ISSO
from .models import Profile
from .forms import ProfileForm
from . import youtube_service
import json
from django.contrib.auth.models import User # <-- IMPORTE O User

# Função "helper" para pegar nosso usuário de teste
def get_teste_profile():
    try:
        # Vamos assumir que seu superusuário (ID=1) é o usuário de teste
        teste_user = User.objects.get(id=1) 
        profile, created = Profile.objects.get_or_create(user=teste_user)
        return profile
    except User.DoesNotExist:
        return None # (Crie um superusuário se isso acontecer)

# @login_required # <-- COMENTADO
def dashboard_view(request):

    profile = get_teste_profile() # 1. Pega o perfil de teste

    if not profile:
        # Se nem o usuário de teste existir, algo está muito errado
        return render(request, 'analytics/index.html', {
            'error_message': 'Usuário de teste (ID=1) não encontrado. Crie um superusuário.'
        })

    # 2. Pega os IDs do perfil de teste
    CHANNEL_ID = profile.youtube_channel_id
    VIDEO_ID_FOR_CHART = profile.default_video_id

    # ... (O resto da sua view continua IDÊNTICO) ...

    # 5. Se os IDs estiverem vazios, manda ele preencher
    if not CHANNEL_ID or not VIDEO_ID_FOR_CHART:
        # (Idealmente, envie uma mensagem "Por favor, preencha seus IDs")
        return redirect('settings')

    context = {
        'channel_stats': None,
        'video_chart_data': None,
        'error_message': None
    }

# @login_required # <-- COMENTADO
def settings_view(request):

    profile = get_teste_profile() # 1. Pega o perfil de teste
    if not profile:
         return redirect('dashboard_home') # Deixa a dashboard lidar com o erro

    if request.method == 'POST':
        form = ProfileForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('dashboard_home')
    else:
        form = ProfileForm(instance=profile)

    return render(request, 'analytics/settings.html', {'form': form})

    # O resto da view é IDÊNTICO, pois agora as variáveis
    # CHANNEL_ID e VIDEO_ID_FOR_CHART são dinâmicas!
    
    service = youtube_service.get_youtube_service()
    
    if not service:
        context['error_message'] = "Erro ao conectar com a API do YouTube. Verifique sua API Key."
        return render(request, 'analytics/index.html', context)

    try:
        channel_stats = youtube_service.get_channel_stats(service, CHANNEL_ID)
        context['channel_stats'] = channel_stats

        video_stats = youtube_service.get_video_stats(service, VIDEO_ID_FOR_CHART)
        
        if video_stats:
            chart_data = {
                'labels': ['Visualizações', 'Likes', 'Comentários'],
                'data': [
                    video_stats['view_count'],
                    video_stats['like_count'],
                    video_stats['comment_count']
                ],
                'video_title': video_stats['title']
            }
            context['video_chart_data'] = json.dumps(chart_data)

    except Exception as e:
        context['error_message'] = f"Erro ao buscar dados: {e}"

    # O template é o mesmo!
    return render(request, 'analytics/index.html', context)