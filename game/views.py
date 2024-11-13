from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Player
import requests
from django.core.cache import cache
import json

def index(request):
    return render(request, 'index.html')

def tap_handler(user_id, username):
    player, created = Player.objects.get_or_create(user_id=user_id, defaults={'username': username})
    
    player.tap_count += 1
    player.score += 1 
    player.save()

    return player.score

@csrf_exempt
def tap(request):
    if request.method == 'POST':
        user_id = request.META.get('REMOTE_ADDR') 
        username = None  
        score = tap_handler(user_id, username)

        return JsonResponse({'status': 'success', 'score': score})
    return JsonResponse({'status': 'fail'}, status=400)

@csrf_exempt
def send_score(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        score = data.get('score', 0)
        user_ip = request.META.get('REMOTE_ADDR')
        try:
            response = requests.post(
                f'https://stats.popcat.click/pop?pop_count={score}',
                headers={
                    'Accept': 'application/json',
                    'Content-Type': 'application/json',
                    'User-Agent': 'Mozilla/5.0'
                }
            )
            response.raise_for_status()
            return JsonResponse({'status': 'success', 'data': response.json()})
        except requests.RequestException as e:
            return JsonResponse({'status': 'fail', 'error': str(e)}, status=500)

    return JsonResponse({'status': 'fail'}, status=400)

def telegram_webhook(request):
    return JsonResponse({'status': 'webhook_received'})

def leaderboard_proxy(request):
    cache_key = "leaderboard_data"
    api_url = "https://leaderboard.popcat.click/"

    try:
        headers = {
            'Accept': 'application/json',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36',
            'Origin': 'https://popcat.click', 
            'Referer': 'https://popcat.click/',
        }
        response = requests.get(api_url, headers=headers)
        response.raise_for_status()
        leaderboard_data = response.json()

        user_ip = request.META.get('REMOTE_ADDR')
        country_response = requests.get(f'https://ipinfo.io/{user_ip}/json')
        country_response.raise_for_status()
        user_country_code = country_response.json().get('country', 'Unknown')

        if user_country_code in leaderboard_data:
            user_country_data = {user_country_code: leaderboard_data[user_country_code]}
            leaderboard_data.pop(user_country_code, None)
            leaderboard_data = {**user_country_data, **leaderboard_data}

        cache.set(cache_key, leaderboard_data, timeout=60 * 10)  
        return JsonResponse(leaderboard_data, safe=False)

    except requests.RequestException as e:
        print(f"RequestException: {e}")
        cached_data = cache.get(cache_key)
        if cached_data:
            return JsonResponse(cached_data, safe=False)
        else:
            return JsonResponse({"error": "No data available"}, status=500)