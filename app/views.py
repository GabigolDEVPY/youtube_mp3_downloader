from django.http import FileResponse, HttpResponse
from django.shortcuts import redirect
from django.views.decorators.csrf import csrf_exempt
from core import settings
from .utils import VideoNotFoundError, Yt, clear_folder
import os
from django.contrib import messages
from django.views.generic import TemplateView
# Create your views here.

class IndexView(TemplateView):
    template_name = "index.html"

class DetailMusic(TemplateView):
    template_name = "detail.html"
    
    def get(self, request, *args, **kwargs):
        url = self.request.GET.get("url")
        if not url:
            messages.error("URL não informada")
            return redirect("app:index")

        try:
            yt = Yt(url=url)
            context = self.get_context_data()
            context["music"] = yt.get_info()
            context["url"] = url
            return self.render_to_response(context)
            
        except VideoNotFoundError as e:
            messages.error(request, str(e))
            return redirect("app:index")
            
        except Exception:
            messages.error(request, "Um erro inesperado aconteceu")

@csrf_exempt
def DownloadMusic(request):
    try:
        clear_folder()
        url = request.POST.get("url")
        if not url:
            return HttpResponse("URL não informada", status=400)
        
        yt = Yt(url=url)
        info = yt.get_info()
        yt.download()
        
        name_music = f"{info["title"]}.mp3"
        file_path = os.path.join(settings.BASE_DIR, 'media', name_music)
        
        if not os.path.exists(file_path):
            return HttpResponse("Arquivo não encontrado", status=400)
        
        return FileResponse(open(file_path, 'rb'), as_attachment=True, filename=name_music)

    except VideoNotFoundError as e:
        return HttpResponse(str(e), status=404)
    
    except Exception:
        return HttpResponse("Erro ao processar o download", status=500)