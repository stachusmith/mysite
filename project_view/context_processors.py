from project_view.models import My_part

def my_parts(request):
    return {'my_parts': My_part.objects.all()}