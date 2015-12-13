from django.http import HttpResponse, Http404, HttpResponseServerError
from django.template.context_processors import csrf
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from django.shortcuts import render_to_response

def index(request):
    return HttpResponse("Well this is good news")

@csrf_exempt
def get_media(request):
    if request.method == 'POST':
        c = {}
        c.update(csrf(request))
        requestParams = request.POST
        try:
            level = requestParams['level']
            image_id = requestParams['image_id']
            print('Got a request for {}/{}'.format(level, image_id))
            # response = HttpResponse()
            # response['Content-Type'] = 'image/png'
            # response['Content-Disposition'] = 'attachment;filename=' +image_id
            with open('{}/images/Level{}/{}.jpg'.format(settings.BASE_DIR, level,image_id), 'rb') as f:
                return HttpResponse(f.read(), content_type="image/jpeg")
        except IOError:
            raise HttpResponseServerError
        except Exception as e:
            print(e)
            raise Http404
    else:
        raise Http404