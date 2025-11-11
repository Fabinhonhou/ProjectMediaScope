# Em core/views.py
from django.shortcuts import render, redirect # (O 'redirect' já deve estar lá)
from django.contrib.auth.decorators import login_required, user_passes_test
from django.db.models import Sum, Count
from django.contrib.auth import get_user_model

from subscriptions.models import Subscription, Payment

# Isso checa se o usuário é um 'superuser'. Se não, ele dá erro.
def is_admin(user):
    return user.is_superuser

def home_view(request):
    """
    Futura página de login/home.
    """
    # Se o usuário já estiver logado, manda ele pro dashboard
    if request.user.is_authenticated:
        return redirect('dashboard_home')
        
    # Se não, mostra a página de login
    return render(request, 'accounts/auth.html')


def planos_view(request):
    """
    Mostra a página de preços (baseado no seu design).
    """
    context = {}
    return render(request, 'core/planos.html', context)


@login_required
@user_passes_test(is_admin, login_url='dashboard_home') # Tranca a porta
def admin_dashboard_view(request):
    """
    Mostra o dashboard de admin com Renda, Clientes, etc.
    """

    # 1. Pega o total de usuários cadastrados
    total_users = get_user_model().objects.count()

    # 2. Pega o total de clientes (assinaturas 'ativas')
    total_clients = Subscription.objects.filter(status=Subscription.StatusChoices.ACTIVE).count()

    # 3. Pega a Renda Total (soma de todos os pagamentos)
    total_revenue_data = Payment.objects.aggregate(total=Sum('amount'))
    total_revenue = total_revenue_data['total'] or 0 # Se for 'None', vira 0

    # (Por enquanto, vamos simular os dados de gráfico)
    fake_chart_data = {
        'labels': ['Jan', 'Fev', 'Mar', 'Abr'],
        'data': [5, 10, 8, 15]
    }

    context = {
        'total_users': total_users,
        'total_clients': total_clients,
        'total_revenue': total_revenue,
        'fake_chart_data': fake_chart_data, # (Depois a gente faz isso de verdade)
    }

    return render(request, 'core/admin_dashboard.html', context)