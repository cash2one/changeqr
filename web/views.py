
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext

from qrcode.models import Qrcode, CodeContent, CodeMedia

# Create your views here.


def index(request):
    return render_to_response('home/index.html', {
    },  context_instance=RequestContext(request))


def wap_media(request, code):

    imgs = []
    text = None
    audio = None
    video = None
    use_time = None

    qrcode = get_object_or_404(Qrcode, full=code)
    try:
        qrcodeContent = CodeContent.objects.get(qrcode=qrcode)
        text = qrcodeContent.text
        use_time = qrcodeContent.last_update
        medias = CodeMedia.objects.filter(relate_to=qrcodeContent)
        for m in medias:
            if m.media_type == 1:
                audio = m
            elif m.media_type == 2:
                imgs.append(m)
            elif m.media_type == 3:
                video = m
    except:
        pass
    return render_to_response('wap/media.html', {
        'text': text,
        'imgs': imgs,
        'audio': audio,
        'video': video,
        'use_time': use_time,
    },  context_instance=RequestContext(request))
