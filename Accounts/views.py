from django.shortcuts import render, redirect
from Posts import views
from Forum import urls
from .forms import UserUpdateForm
# Create your views here.
def login_excluded(redirect_to):
    """ This decorator kicks authenticated users out of a view """
    def _method_wrapper(view_method):
        def _arguments_wrapper(request, *args, **kwargs):
            if request.user.is_authenticated:
                return redirect(redirect_to)
            return view_method(request, *args, **kwargs)
        return _arguments_wrapper
    return _method_wrapper

def profile(request):
    if request.method == 'POST':
        a_form = UserUpdateForm(request.POST, instance=request.user)

        if a_form.is_valid():
            a_form.save()
            return redirect('profile')
    else:
        a_form = UserUpdateForm(instance=request.user)
        context = {'a_form': a_form}
    return render(request, 'profile.html', context)