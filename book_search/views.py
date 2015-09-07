from django.shortcuts import render, redirect
from .tasks import process_query_and_email
from datetime import datetime as dt


def home_page(request):
    if request.method == 'POST':
        query, email = request.POST.get('query'), request.POST.get('email')
        process_query_and_email.delay(query, email, dt.now())
        request.session['query'] = query
        request.session['email'] = email
        return redirect('/?success')
    if 'success' in request.GET:
        query = request.session.pop('query', None)
        email = request.session.pop('email', None)
        success = query and email
        if not success:
            return redirect('/')
        return render(request, 'home.html',
                      {
                          'success': success,
                          'query': query,
                          'email': email
                      }
                      )
    return render(request, 'home.html')
