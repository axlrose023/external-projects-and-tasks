from django.shortcuts import render, get_object_or_404
from django.http import Http404
from .models import Office

def office_detail(request, room_number):
    try:
        office = Office.objects.get(cabinet=room_number)
    except Office.DoesNotExist:
        raise Http404("Кабінет з таким номером не існує")
    return render(request, 'office/office_detail.html', {'office': office})
