from django.db import models
from django.conf import settings # Para pegar o User (AUTH_USER_MODEL)

# Modelo 1: O "Cardápio" de Planos
class Plan(models.Model):
    name = models.CharField(max_length=100, unique=True) # Ex: "Plano Essential"
    price_monthly = models.DecimalField(max_digits=10, decimal_places=2) # Ex: 297.00
    price_annual = models.DecimalField(max_digits=10, decimal_places=2) # Ex: 237.00 (por mês)
    
    # Campo para o seu design (o ícone roxo)
    # Veja: https://fonts.google.com/icons
    icon_name = models.CharField(max_length=50, blank=True, help_text="Nome do ícone do Material Symbols (ex: 'auto_awesome')")

    def __str__(self):
        return self.name

# Modelo 2: O "Contrato" (Quem assinou o quê)
class Subscription(models.Model):
    
    class StatusChoices(models.TextChoices):
        ACTIVE = 'active', 'Ativa'
        CANCELED = 'canceled', 'Cancelada'
        PAST_DUE = 'past_due', 'Vencida' # (Vencida/Aguardando Pagamento)
        FREE_TRIAL = 'free_trial', 'Trial Gratuito'

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE,
        related_name='subscription'
    ) # Um usuário só pode ter UMA assinatura
    
    plan = models.ForeignKey(Plan, on_delete=models.SET_NULL, null=True, related_name='subscriptions')
    status = models.CharField(max_length=20, choices=StatusChoices.choices, default=StatusChoices.FREE_TRIAL)
    
    start_date = models.DateTimeField(auto_now_add=True) # Data que o registro foi criado
    current_period_end = models.DateTimeField(null=True, blank=True) # Data que a assinatura expira

    def __str__(self):
        return f"{self.user.email} - {self.plan.name if self.plan else 'Sem Plano'} ({self.status})"
    
    # Em subscriptions/models.py
# (O 'Plan' e 'Subscription' que já fizemos estão aqui em cima)

...

# Modelo 3: O "Caixa Registadora" (Histórico de Pagamentos)
class Payment(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.SET_NULL, # Se o user for deletado, guardamos o histórico
        null=True,
        related_name='payments'
    )
    subscription = models.ForeignKey(
        Subscription,
        on_delete=models.SET_NULL, # Linka o pagamento à assinatura
        null=True,
        related_name='payments'
    )
    amount = models.DecimalField(max_digits=10, decimal_places=2) # O valor que foi pago
    payment_date = models.DateTimeField(auto_now_add=True) # Quando foi pago

    # No futuro, podemos adicionar 'stripe_payment_id', etc.

    def __str__(self):
        return f"Pagamento de {self.amount} por {self.user.email if self.user else 'Usuário Deletado'}"