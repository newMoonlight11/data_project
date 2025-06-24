from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.http import HttpResponse
from django.core.management import call_command

def home(request):
    return HttpResponse("Bienvenido al sistema de procesamiento de archivos")

@require_POST
def parse_file(request):
    filepath = request.POST.get('filename')
    if not filepath:
        return JsonResponse({'status': 'error', 'message': 'Filename is required'}, status=400)
    try:
        call_command('generate_exports', filepath)
        call_command('data_prueba', filepath)
        return JsonResponse({'status': 'ok'})
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)}, status=500)
    
