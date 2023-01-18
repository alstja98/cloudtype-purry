from django.shortcuts import render, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import redirect
from django.core.files.storage import default_storage #aws에 이미지 저장하기 위해 필요한거임
from django.conf import settings
from .models import User, Images; #db 테이블들 가져옴
import random



def index(request):
	return render(request, 'index.html')

@csrf_exempt
def openbeta(request):
    user_name = request.POST['name']
    user_email = request.POST['email']
    user = User.objects.create(name=user_name, email=user_email)
    
    for i in range(1, 6):
        myfile = request.FILES.get(f'myfile{i}')
        if myfile:
            filename = default_storage.save(myfile.name, myfile)
            file_url = default_storage.url(filename)
            Images.objects.create(user_id=user, path=file_url)
    
    return redirect('/app1')