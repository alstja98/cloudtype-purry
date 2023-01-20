from http.client import HTTPResponse
from django.db import connection
from django.shortcuts import render, HttpResponse, redirect
from django.views.decorators.csrf import csrf_exempt
from django.views import views
from django.core.files.storage import default_storage  # aws에 이미지 저장하기 위해 필요한거임
from django.conf import settings
from django.http import FileResponse, HttpResponseBadRequest, HttpResponse, JsonResponse
from .models import User, Images, Prompt, Admin;  # db 테이블들 가져옴
from datetime import datetime
import boto3
import bcrypt, jwt, json 

def index(request):
	return render(request, 'index.html')

# 신청자 정보 받으면 sql에 저장, 이미지 aws에 저장

@csrf_exempt
def openbeta(request):
    user_name = request.POST['name']
    user_email = request.POST['email']
    user = User.objects.create(name=user_name, email=user_email)
    # Assume the prompt with id 1 exists in the database
    prompt_id = Prompt.objects.get(pk=1).id
    image_type = ['front', 'up', 'down',
        'right', 'left']  # array of image types
    index = 0  # to keep track of the current image type

    for i in range(1, 6):
        myfile = request.FILES.get(f'myfile{i}')
        if myfile:
            extension = myfile.name.split(".")[-1]
            date = datetime.now().strftime("%Y%m%d")
            time = datetime.now().strftime("%H:%M:%S")
            filename = user_name + str(i) + "_" + \
                                       date + "_" + time + "." + extension
            filename = default_storage.save(filename, myfile)
            file_url = default_storage.url(filename)
            if index < len(image_type):
                Images.objects.create(
                    user=user, path=file_url, prompt_id=prompt_id, type=image_type[index])
                index += 1

    return HttpResponse("<script>alert('신청이 완료되었습니다.');window.location.href = '/app1'</script>")

'''
def manage(request):
    id = request.GET.get('id')
    password = request.GET.get('password')
    if id != 'furrywithprobee123@gmail.com' and password != 'probee123!':
        return HttpResponseBadRequest
    with connection.cursor() as cursor:
        cursor.execute(
            "SELECT u.id, u.name, u.email, i.type, i.path FROM user u, images i WHERE u.id=i.user_id")
        # cursor.execute(
        #     "SELECT u.id, u.name, u.email, i.type, i.path FROM user u, images i WHERE u.id=i.user_id and i.type in ('front','up','down','right','left') group by u.id")
        rows = cursor.fetchall()
        response = []
        s3 = boto3.client('s3')
        for row in rows:
            path = row[4].split('?')[0]
            response.append(
                {'id': row[0], 'name': row[1], 'email': row[2], 'type': row[3], 'path': path})
    return render(request, 'manage.html', {'rows': response})


def login(request):
    if request.method == "GET":
        return render(request, 'login.html')

    elif request.method == "POST":
        username = request.POST.get('username', None)
        password = request.POST.get('password', None)

        res_data = {}
        if not (username and password):
            res_data['error'] = '모든 값을 입력하세요!'

        else:
            if username == 'probee' and password == 'probee123!':
                pass
            else:
                res_data['error'] = '비밀번호가 다릅니다!'

        return render(request, 'login.html', res_data)
'''

def download_image(request):
    path = request.GET.get('path')
    # Connect to S3 using the boto3 library
    s3 = boto3.client('s3')

    # Download the image
    response = s3.get_object(Bucket='purry0', Key=path)
    # Return the image as a FileResponse so that it can be downloaded
    return FileResponse(response['Body'], as_attachment=True, filename='image.jpg')

@csrf_exempt
def login(request):

    if request.method == "GET":
        return render(request, 'login.html')
    elif request.method == "POST":
        username = request.POST.get('id', None)
        password = request.POST.get('pw', None)
        session_username = request.session.get('username', None)
        session_password = request.session.get('password', None)
        if username == session_username and password == session_password:
            with connection.cursor() as cursor:
                cursor.execute(
                    "SELECT u.id, u.name, u.email, i.type, i.path FROM user u, images i WHERE u.id=i.user_id")
                rows = cursor.fetchall()
                response = []
                s3 = boto3.client('s3')
                for row in rows:
                    path = row[4].split('?')[0]
                    response.append(
                        {'id': row[0], 'name': row[1], 'email': row[2], 'type': row[3], 'path': path})
            return render(request, 'manage.html', {'rows': response})
        else:
            if Admin.objects.filter(id=username).exists() :
                decode_hash_pw = Admin.objects.get(id=username).pw
                bytes_input_pw = password.encode('utf-8')
                bytes_db_pw = decode_hash_pw.encode('utf-8')
                user = bcrypt.checkpw(bytes_input_pw, bytes_db_pw)
            #user = Admin.objects.filter(id=username, pw=password).first()
            if user:
                request.session['username'] = username
                request.session['password'] = password
                with connection.cursor() as cursor:
                    cursor.execute(
                        "SELECT u.id, u.name, u.email, i.type, i.path FROM user u, images i WHERE u.id=i.user_id")
                    rows = cursor.fetchall()
                    response = []
                    s3 = boto3.client('s3')
                    for row in rows:
                        path = row[4].split('?')[0]
                        response.append(
                            {'id': row[0], 'name': row[1], 'email': row[2], 'type': row[3], 'path': path})
                return render(request, 'manage.html', {'rows': response})
            else:
                res_data = {'error': '로그인 정보가 틀렸습니다.'}
                return render(request, 'login.html', res_data)
    return render(request, 'login.html')
