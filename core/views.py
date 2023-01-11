from django.shortcuts import render, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import redirect
from django.core.files.storage import default_storage #aws에 이미지 저장하기 위해 필요한거임
from django.conf import settings
from .models import User, Images; #db 테이블들 가져옴
import random



def index(request):
	return render(request, 'index.html')


# 신청자 정보 받으면 sql에 저장, 이미지 aws에 저장
@csrf_exempt #이거는 장고 csrf 보안 해제 때문에 필요한거임. 나중에 배포할때는 지워야함.
def openbeta(request):
    applicant_name = request.POST['name']
    applicant_email = request.POST['email']
    files = request.FILES.getlist('myfiles')


    for file in files:
        # input에서 받아온 이름과 이메일을 가진 사용자가 이미 User 테이블에 있는지 확인
        user, created = User.objects.get_or_create(name=applicant_name, email=applicant_email)

        # S3에 이미지 저장하고, 저장된 이미지의 url을 가져옴
        filename = default_storage.save(file.name, file)
        file_url = default_storage.url(filename)

        # input에서 받아온 이미지 이름들을 images 테이블에 저장
        Images.objects.create(seq=user, path=file_url)
 

    return redirect('/app1')