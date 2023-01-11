from django.shortcuts import render, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import redirect
from .models import User, Images; #db 테이블들 가져옴
import random
from utils.s3Manager import upload_files_to_S3


def index(request):
	return render(request, 'core/index.html')


# 신청자 정보 받으면 sql에 저장, 이미지 aws에 저장
@csrf_exempt #이거는 장고 csrf 보안 해제 때문에 필요한거임. 나중에 배포할때는 지워야함.
def openbeta(request):
    applicant_name = request.POST['name']
    applicant_email = request.POST['email']
    applicant_imgs = request.POST['myfiles[]']

    print(applicant_name)
    print(applicant_email)
    print(applicant_imgs) #이미지가 하나만 출력되는 문제가 있음. 이건 나중에 해결해야함.

    # input에서 받아온 유저의 이름과 email을 user 테이블에 저장
    User.objects.create(name=applicant_name, email=applicant_email)
    # input에서 받아온 유저의 이미지 이름들 images 테이블에 저장
    # 사실 이미지 이름을 AWS 컴퓨터 내의 경로로 재구성해야하고, 이미지들도 여러개 받을 수 있게 처리해야하는데
    # 우선 테스트로 DB에 이미지 이름만 저장하도록 함.
    user_seq = User.objects.get(name=applicant_name)
    print(user_seq)
    
    image_path = upload_files_to_S3(applicant_imgs)
    Images.objects.create(seq=user_seq, path=image_path)

    return redirect('/app1')