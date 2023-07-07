from django.shortcuts import render


def profile(request):
    context = {}
    return render(request, 'profiles/profile.html', context)
