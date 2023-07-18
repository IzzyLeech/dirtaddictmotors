from django.shortcuts import render, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from .models import UserProfile
from .forms import UserProfileForm

from checkout.models import Order


@login_required
def profile(request):
    """
    View that will display the user profile
    """
    profile = get_object_or_404(UserProfile, user=request.user)

    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=profile)
        if form.is_valid():
            # Check if the form data has changed
            if (form.cleaned_data['first_name'] != profile.user.first_name or
                    form.cleaned_data['last_name'] != profile.user.last_name or
                    form.has_changed()):
                form.save()

                # Update the first and last name on the related User object
                user = profile.user
                user.first_name = form.cleaned_data['first_name']
                user.last_name = form.cleaned_data['last_name']
                user.save()

                messages.success(request, 'Profile updated successfully')
            else:
                messages.info(request, 'No changes were made to the profile')
        else:
            messages.error(
                        request,
                        'Update failed. Please ensure the form is valid')
    else:
        form = UserProfileForm(instance=profile)

    orders = profile.orders.all()

    context = {
        'form': form,
        'orders': orders,
        'on_profile_page': True
    }
    return render(request, 'profiles/profile.html', context)


@login_required
def order_history(request, order_number):
    order = get_object_or_404(Order, order_number=order_number)

    if not request.user.is_superuser:
        messages.info(request, (
            f'This is a past confirmation for order number {order_number}. '
            'A confirmation email was sent on the order date.'
        ))

    context = {
        'order': order,
    }

    return render(request, 'checkout/checkout_success.html', context)
