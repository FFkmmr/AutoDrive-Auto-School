from django.shortcuts import render

def home(request):
    return render(request, 'main/components/home.html')

def about(request):
    return render(request, 'main/components/about.html')

def booking(request):
    return render(request, 'main/components/booking.html')

def contact(request):
    return render(request, 'main/components/contact.html')