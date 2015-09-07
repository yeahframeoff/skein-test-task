from django.shortcuts import render, redirect
from .tasks import process_query_and_email


def home_page(request):
    if request.method == 'POST':
        query, email = request.POST.get('query'), request.POST.get('email')
        process_query_and_email.delay(query, email)
        return redirect('/?success')
    if 'success' in request.GET:
        return render(request, 'home.html', {'success': True})
    return render(request, 'home.html')
