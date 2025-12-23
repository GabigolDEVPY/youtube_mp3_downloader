from django.http import FileResponse
from django.views.decorators.csrf import csrf_exempt
from core import settings
from .utils import Yt, clear_folder
import os
from django.views.generic import TemplateView
# Create your views here.

class IndexView(TemplateView):
    template_name = "index.html"

class DetailMusic(TemplateView):
    template_name = "detail.html"
    
    def get_context_data(self, **kwargs):
        url = url= self.request.GET.get("url")
        yt = Yt(url=url)
        context = super().get_context_data(**kwargs)
        context["music"] = yt.get_info()
        context["url"] = url
        print(context["music"])
        return context

@csrf_exempt
def DownloadMusic(request):
    clear_folder()
    url = request.POST.get("url")
    yt = Yt(url=url)
    info = yt.get_info()
    yt.download()
    name_music = f"{info["title"]}.mp3"
    file_path = os.path.join(settings.BASE_DIR, 'media', name_music)
    return FileResponse(open(file_path, 'rb'), as_attachment=True, filename=name_music)
