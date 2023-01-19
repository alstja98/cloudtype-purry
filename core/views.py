from django.shortcuts import render, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import redirect
from django.core.files.storage import default_storage #aws에 이미지 저장하기 위해 필요한거임
from django.conf import settings
from .models import User, Images, Prompt; #db 테이블들 가져옴
import random

def index(request):
	return render(request, 'index.html')

# 신청자 정보 받으면 sql에 저장, 이미지 aws에 저장
@csrf_exempt
def openbeta(request):
    user_name = request.POST['name']
    user_email = request.POST['email']
    user = User.objects.create(name=user_name, email=user_email)
    prompt_id = Prompt.objects.get(pk=1).id  # Assume the prompt with id 1 exists in the database
    image_type = ['front', 'up', 'down', 'right', 'left']  # array of image types
    index = 0  # to keep track of the current image type

    for i in range(1, 6):
        myfile = request.FILES.get(f'myfile{i}')
        if myfile:
            filename = default_storage.save(myfile.name, myfile)
            file_url = default_storage.url(filename)
            if index < len(image_type):
                Images.objects.create(user=user, path=file_url, prompt_id=prompt_id, type=image_type[index])
                index += 1
    return HttpResponse("<script>alert('신청이 완료되었습니다.');window.location.href = '/app1'</script>")