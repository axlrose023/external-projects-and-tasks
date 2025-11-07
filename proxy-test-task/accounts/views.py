from django.contrib import messages
from django.contrib.auth import authenticate, update_session_auth_hash, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserChangeForm
from django.db.models import Sum
from django.shortcuts import render, redirect

from accounts.models import CustomUser
from proxy.models import UserSite, UserStatistics


@login_required(login_url='login')
def home(request):
    user = request.user
    created_sites = UserSite.objects.filter(user=user)

    site_statistics = []
    for site in created_sites:
        statistics = UserStatistics.objects.filter(user=user, site=site).first()
        site_statistics.append({'site': site, 'statistics': statistics})

    total_statistics = UserStatistics.objects.filter(user=user, site__in=created_sites).aggregate(
        total_page_transitions=Sum('page_transitions'),
        total_data_sent=Sum('data_sent'),
        total_data_received=Sum('data_received'),
    )

    context = {
        'user': user,
        'site_statistics': site_statistics,
        'total_statistics': total_statistics,
    }

    return render(request, 'index.html', context)


def login(request):
    try:
        if request.method == 'POST':
            username = request.POST.get('username')
            password = request.POST.get('password')
            user = authenticate(request, username=username, password=password)

            if user is not None:
                from django.contrib.auth import login
                login(request, user)
                return redirect('home')
            else:
                messages.error(request, 'Invalid login credentials. Please try again.')

        return render(request, 'accounts/login.html')
    except ValueError as e:
        messages.error(request, f'An error occurred: {e}')
        return render(request, 'accounts/login.html')


def user_logout(request):
    logout(request)
    return redirect('home')


def register(request):
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')

        user = CustomUser.objects.create_user(username=username, email=email, password=password, first_name=first_name,
                                              last_name=last_name)
        if user:
            messages.success(request, 'Now please log in')
        return redirect('login')
    return render(request, 'accounts/register.html')


@login_required(login_url='login')
def change_password(request):
    if request.method == 'POST':
        old_password = request.POST.get('old_password')
        new_password = request.POST.get('new_password')
        confirm_password = request.POST.get('confirm_password')

        user = request.user

        if user.check_password(old_password) and new_password == confirm_password:
            user.set_password(new_password)
            user.save()
            update_session_auth_hash(request, user)
            messages.success(request, 'Password changed successfully.')
            logout(request)
            return redirect('login')
        else:
            messages.error(request, 'Invalid old password or new passwords do not match.')

    return render(request, 'accounts/change_password.html')

