from project_view.models import My_part
from project_view.forms import GetInTouchForm

def my_parts(request):
    return {'my_parts': My_part.objects.all()}

def touch_form(request):
    return {'touch_form': GetInTouchForm() }