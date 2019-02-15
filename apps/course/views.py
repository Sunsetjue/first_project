from django.shortcuts import render
from apps.cms.models import Course
from django.shortcuts import Http404
from django.conf import settings
from utils import restful
import time, hmac, hashlib, os

# Create your views here.
def course_index(request):
    courses = Course.objects.all()
    context = {"courses": courses}
    return render(request, "course/course_index.html", context=context)

def course_detail(request,course_id):
    try:
        course = Course.objects.get(id=course_id)
        context = {"course": course}
        return render(request, 'course/course_detail.html', context=context)
    except:
        raise Http404

def course_token(request):
    # video：是视频文件的完整链接
    file = request.GET.get('video')
    #
    # course_id = request.GET.get('course_id')
    # if not CourseOrder.objects.filter(course_id=course_id,buyer=request.user,status=2).exists():
    #     return restful.params_error(message='请先购买课程！')

    expiration_time = int(time.time()) + 2 * 60 * 60

    USER_ID = settings.BAIDU_CLOUD_USER_ID
    USER_KEY = settings.BAIDU_CLOUD_USER_KEY

    # file=http://hemvpc6ui1kef2g0dd2.exp.bcevod.com/mda-igjsr8g7z7zqwnav/mda-igjsr8g7z7zqwnav.m3u8
    extension = os.path.splitext(file)[1]
    media_id = file.split('/')[-1].replace(extension, '')

    # unicode->bytes=unicode.encode('utf-8')bytes
    key = USER_KEY.encode('utf-8')
    message = '/{0}/{1}'.format(media_id, expiration_time).encode('utf-8')
    signature = hmac.new(key, message, digestmod=hashlib.sha256).hexdigest()
    token = '{0}_{1}_{2}'.format(signature, USER_ID, expiration_time)
    return restful.result(data={'token': token})

def paying_course(request,course_id):
    try:
        course = Course.objects.get(id=course_id)
        context = {"course": course}
        return render(request, 'course/paying_course.html', context=context)
    except:
        raise Http404
