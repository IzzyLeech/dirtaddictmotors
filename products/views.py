from django.shortcuts import render


def products_display(request):
    """View to display products with filter option for certain option"""

    context = {}
    return render(request, 'products/products.html', context)
