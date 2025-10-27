from django.shortcuts import render

def home(request):
    active_page = request.GET.get('active_page', 'home')
    return render(request, 'main/components/home.html', {'active_page': active_page})

def about(request):
    active_page = request.GET.get('active_page', 'about')
    return render(request, 'main/components/about.html', {'active_page': active_page})

def booking(request):
    active_page = request.GET.get('active_page', 'booking')
    return render(request, 'main/components/booking.html', {'active_page': active_page})

def contact(request):
    active_page = request.GET.get('active_page', 'contact')
    return render(request, 'main/components/contact.html', {'active_page': active_page})
