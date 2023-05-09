from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

from django.conf import settings

import random

# Create your views here.


@login_required
def home(request):
    liargame_joined = settings.LIARGAME_USER_VARS.get("liargame_joined", default=[])
    
    return render(
        request, 
        "liargame/home.html", 
        {
            "user": request.user,
            "joined": liargame_joined, 
            "joined_len": len(liargame_joined), # ", ".join(liargame_joined), 
            "ready": settings.LIARGAME_USER_VARS.get('word_confirm', False), 
            "liars": settings.LIARGAME_USER_VARS.get('liars')
        }
    )

@login_required
def join(request):
    liargame_joined = settings.LIARGAME_USER_VARS.get("liargame_joined", default=[])
    request_username = request.user.get_username()
    
    if request_username not in liargame_joined:
        liargame_joined.append( request_username )
        settings.LIARGAME_USER_VARS.set(liargame_joined=liargame_joined)
    
    return redirect('liargame_home')    

@login_required
def unjoin(request):
    liargame_joined = settings.LIARGAME_USER_VARS.get("liargame_joined", default=[])
    request_username = request.user.get_username()
    
    if request_username in liargame_joined:
        liargame_joined.remove( request_username )
        settings.LIARGAME_USER_VARS.set(liargame_joined=liargame_joined)
    
    return redirect('liargame_home')

@login_required
def set_word_setter(request):
    return render(request, "liargame/set_word.html", {})
    
@login_required
def set_word_result(request):
    realword = request.POST.get('realword')
    fakeword = request.POST.get('fakeword')
    settings.LIARGAME_USER_VARS.set(realword=realword, fakeword=fakeword, word_confirm=False)
    return render(request, "liargame/set_word_result.html", {"realword": realword, "fakeword": fakeword, })
    
@login_required
def set_word_result_confirm(request):
    settings.LIARGAME_USER_VARS.set(word_confirm=True)
    return redirect('liargame_home')

SEQ_SIZE = 100
LIAR_CNT = 1
@login_required
def choose_liar(request):
    liargame_joined = settings.LIARGAME_USER_VARS.get('liargame_joined')
    liargame_joined = liargame_joined.copy() * (SEQ_SIZE // len(liargame_joined))
    liars = set()
    while len(liars) < LIAR_CNT:
        liars.add( random.choice( liargame_joined ) )
    settings.LIARGAME_USER_VARS.set(liars=liars)
    
    return redirect('liargame_home')
    
@login_required
def check_my_word(request):
    liars = settings.LIARGAME_USER_VARS.get('liars', False)
    
    if not liars:
        return redirect('liargame_home')
    
    is_liar = request.user.get_username() in liars
    
    if is_liar:
        my_word = settings.LIARGAME_USER_VARS.get('fakeword')
    else:
        my_word = settings.LIARGAME_USER_VARS.get('realword')
    
    return render(request, "liargame/check_my_word.html", {"is_liar": is_liar, "my_word": my_word, })
    
@login_required
def reset(request):
    if request.user.is_leadership:
        settings.LIARGAME_USER_VARS.remove('liars', error_proof=True)
        settings.LIARGAME_USER_VARS.remove('word_confirm', error_proof=True)
        settings.LIARGAME_USER_VARS.remove('realword', error_proof=True)
        settings.LIARGAME_USER_VARS.remove('fakeword', error_proof=True)
    return redirect('liargame_home')
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    