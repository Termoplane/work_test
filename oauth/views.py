from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
import requests
import json

# Create your views here.

def startpage(request):
    if request.user.is_authenticated:
        if not request.user.social_auth.filter(provider='vk-oauth2'):
            return render(request, 'login.html')
        else:
            return HttpResponseRedirect('/friends')
    else:
        return HttpResponse('Problem occured')

@login_required
def friends(request):
    social = request.user.social_auth.get(provider='vk-oauth2')
    log_user = requests.get(
        'https://api.vk.com/method/users.get',
        params={'access_token': social.extra_data['access_token'], 'v': '5.103', 'fields': ['photo_100']}
    )
    friends = requests.get(
        'https://api.vk.com/method/friends.get',
        params={'access_token': social.extra_data['access_token'], 'fields': ['photo_100'], 'v': '5.103'}
    )
    friends = friends.json()
    log_user = log_user.json()
    friends = friends['response']['items'][:5]
    log_user = log_user['response']
    logged_user = log_user[0]

    context = {'user': logged_user, 'friend_list': friends}
    return render(request, 'friends.html', context)