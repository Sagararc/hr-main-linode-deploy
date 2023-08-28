from django.contrib.auth.models import User

def username_context(request):
    username = None
    if request.user.is_authenticated:
        username = request.user.username
    return {'username': username}
