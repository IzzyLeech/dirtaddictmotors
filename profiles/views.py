from django.shortcuts import render


def profile(request):
    context = {
        'user': request.user,
    }
    return render(request, 'profiles/profile.html', context)
