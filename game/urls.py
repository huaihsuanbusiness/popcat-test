from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('tap/', views.tap, name='tap'),
    path('send-score/', views.send_score, name='send_score'),
    path('leaderboard-proxy/', views.leaderboard_proxy, name='leaderboard_proxy'),
    path('telegram-webhook/', views.telegram_webhook, name='telegram_webhook'),
]