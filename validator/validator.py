def is_http(request):
    return 'X-Forwarded-Proto' in request.headers and 'http' == request.headers['X-Forwarded-Proto']
