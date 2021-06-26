from django.shortcuts import redirect


def login_required(view):
    
    def view_envuelta(request, *args, **kwargs):
        if 'id' in request.session:
            return view(request, *args, **kwargs)
        else:
            return redirect('/')

    return view_envuelta

def login_admin(view):
    
    def view_envuelta(request, *args, **kwargs):
        if 'user_level'==9 and 'id' in request.session:
            return view(request, *args, **kwargs)
        else:
            return redirect('/')

    return view_envuelta