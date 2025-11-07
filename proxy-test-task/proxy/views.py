from urllib.parse import urljoin

import requests
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseForbidden
from django.shortcuts import render, redirect, get_object_or_404

from proxy.utils import replace_internal_links


def proxy_view(request, user_site_name, path):
    try:
        user_site = get_object_or_404(UserSite, name=user_site_name)
        full_url = urljoin(user_site.url, path)

        response = requests.get(full_url)
        response.raise_for_status()

        content = response.content.decode('utf-8')
        content = replace_internal_links(user_site.url, user_site_name, content)

        user = request.user
        user_statistics, created = UserStatistics.objects.get_or_create(user=user, site=user_site)

        if not created:
            user_statistics.page_transitions += 1
            content_length = request.META.get('CONTENT_LENGTH', 0)
            user_statistics.data_sent += int(request.META.get('CONTENT_LENGTH', 0)) if content_length else 0
            user_statistics.data_received += int(response.headers.get('content-length', 0))
            user_statistics.save()

        return HttpResponse(content)
    except requests.exceptions.RequestException as e:
        return HttpResponse(f"Error: {str(e)}", status=500)


from proxy.forms import UserSiteForm
from proxy.models import UserStatistics, UserSite


@login_required(login_url='login')
def create_user_site(request):
    if request.method == 'POST':
        form = UserSiteForm(request.POST)
        if form.is_valid():
            user_site = form.save(commit=False)
            user_site.user = request.user
            user_site.save()
            return redirect('home')
    else:
        form = UserSiteForm()

    return render(request, 'proxy/create_user_site.html', {'form': form})


@login_required(login_url='login')
def delete_user_site(request, site_id):
    user_site = get_object_or_404(UserSite, id=site_id)
    if user_site.user != request.user:
        return HttpResponseForbidden("You don't have permission to delete this site.")
    user_site.delete()
    return redirect('home')
