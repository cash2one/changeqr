
from django.shortcuts import render_to_response
from django.template import RequestContext

from qrcode.models import Qrcode, CodeContent, CodeMedia

# Create your views here.

def index(request):
	return render_to_response('home/index.html', {
		},  context_instance=RequestContext(request))


def wap_media (request):

	imgs = []
	audio = None
	video = None
	use_time = None
	
	if 'cid' in request.GET:
		code = request.GET['cid']
		
		try:
			qrcode = Qrcode.objects.get(full=code)
			qrcodeContent = CodeContent.objects.get(qrcode=qrcode)
			use_time = qrcodeContent.last_update
			medias = CodeMedia.objects.filter(relate_to=qrcodeContent)
			# print medias
			# print 'aaaaaa'
			for m in medias:
				if m.media_type == 1:
					audio = m
				elif m.media_type == 2:
					imgs.append(m)
				elif m.media_type == 3:
					video = m
		except:
			pass
	# print imgs
	# print audio
	# print video
	return render_to_response('wap/media.html', {
			'imgs': imgs,
			'audio': audio,
			'video': video,
			'use_time': use_time,
		},  context_instance=RequestContext(request))