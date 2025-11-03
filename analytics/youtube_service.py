# Em dashboard/youtube_service.py
import os
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import logging # Para registrar erros

# Configura o logger
logger = logging.getLogger(__name__)

# Pega a API Key do ambiente
API_KEY = os.environ.get('YOUTUBE_API_KEY')

# 1. Função para criar o "serviço" de conexão
def get_youtube_service():
    if not API_KEY:
        logger.error("A YOUTUBE_API_KEY não foi encontrada no ambiente.")
        return None
    try:
        # Constrói o objeto de serviço da API
        service = build('youtube', 'v3', developerKey=API_KEY)
        return service
    except Exception as e:
        logger.error(f"Erro ao construir o serviço do YouTube: {e}")
        return None

# 2. Função para buscar estatísticas do CANAL
def get_channel_stats(service, channel_id):
    if not service:
        return None
    try:
        request = service.channels().list(
            part="snippet,statistics", # Pedimos o 'snippet' (título, thumb) e 'statistics'
            id=channel_id
        )
        response = request.execute()

        if not response.get('items'):
            logger.warning(f"Nenhum canal encontrado com o ID: {channel_id}")
            return None

        # Pega o primeiro (e único) item da resposta
        item = response['items'][0]
        
        stats = {
            'title': item['snippet']['title'],
            'thumbnail_url': item['snippet']['thumbnails']['default']['url'],
            'subscriber_count': int(item['statistics']['subscriberCount']),
            'view_count': int(item['statistics']['viewCount']),
            'video_count': int(item['statistics']['videoCount']),
        }
        return stats
        
    except HttpError as e:
        logger.error(f"Erro HTTP na API do YouTube: {e}")
        return None
    except Exception as e:
        logger.error(f"Erro ao buscar dados do canal: {e}")
        return None

# 3. Função para buscar estatísticas de um VÍDEO (para o gráfico)
def get_video_stats(service, video_id):
    if not service:
        return None
    try:
        request = service.videos().list(
            part="snippet,statistics",
            id=video_id
        )
        response = request.execute()
        
        if not response.get('items'):
            logger.warning(f"Nenhum vídeo encontrado com o ID: {video_id}")
            return None
            
        item = response['items'][0]
        
        stats = {
            'title': item['snippet']['title'],
            'view_count': int(item['statistics']['viewCount']),
            'like_count': int(item['statistics']['likeCount']),
            'comment_count': int(item['statistics']['commentCount']),
        }
        return stats

    except HttpError as e:
        logger.error(f"Erro HTTP na API do YouTube: {e}")
        return None
    except Exception as e:
        logger.error(f"Erro ao buscar dados do vídeo: {e}")
        return None