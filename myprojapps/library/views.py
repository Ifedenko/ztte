from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.contrib.auth.forms import UserCreationForm
from django.views.generic.edit import CreateView
from django.views.generic.base import View
from django.contrib import messages
from django.urls import reverse_lazy
from .models import *
from datetime import datetime, date, timedelta
from django.utils import timezone
from calendar import month_name
from django.contrib.auth import login as auth_login
from django.contrib.auth.views import LoginView
from django.contrib.auth.decorators import login_required
from .forms import *
from django.core.paginator import Paginator
# Create your views here.
def home(request):
    recent_events = RecentEvent.objects.all()[:6]   
    if request.method == 'POST':
        form = ExcursionBookingForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Заявка отправлена!')
            return redirect('home')
    else:
        form = ExcursionBookingForm()

    context = {
        'recent_events': recent_events,  
        'form': form,
    }
    return render(request, "main/home.html", context)

@login_required
def excursion(request):
    collage_images = CollageImage.objects.all()[:5]
    
    if request.method == 'POST':
        form = ExcursionBookingForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Заявка отправлена!')
            return redirect('excursion')  
    else:
        form = ExcursionBookingForm()
    
    context = {
        'collage_images': collage_images,
        'form': form,
    }
    
    return render(request, 'main/excursion.html', context)
def fotogallery(request):
    photos = Photo.objects.all()  
    filter_type = request.GET.get('filter', 'recent')
    selected_year = request.GET.get('year', None)
    selected_month = request.GET.get('month', None)

    today = date.today()
    
    if filter_type == 'recent':
        start_date = today - timedelta(days=30)
        photos = photos.filter(date__gte=start_date)
    
    elif filter_type == 'this_month':
        photos = photos.filter(date__year=today.year, date__month=today.month)
    
    elif filter_type == 'this_year':
        photos = photos.filter(date__year=today.year)
    
    elif filter_type == 'year' and selected_year:
        photos = photos.filter(date__year=selected_year)
        
    elif filter_type == 'month' and selected_year and selected_month:
        photos = photos.filter(date__year=selected_year, date__month=selected_month)
    
    elif filter_type == 'old':
        two_years_ago = today.year - 2
        photos = photos.filter(date__year__lte=two_years_ago)
    years = Photo.objects.dates('date', 'year').values_list('date__year', flat=True).distinct()
    
    months = [(i, month_name[i]) for i in range(1, 13)]
    
    context = {
        'photos': photos,
        'current_filter': filter_type,
        'years': sorted(set(years), reverse=True),
        'months': months,
        'selected_year': selected_year,
        'selected_month': selected_month,
    }
    
    return render(request, "main/fotogallery.html", context)
def photo_detail(request, photo_id):
    photo = get_object_or_404(Photo, id=photo_id)
    data = {
        'id': photo.id,
        'title': photo.title,
        'description': photo.description,
        'date': photo.date.strftime('%d.%m.%Y'),
        'image_url': photo.image.url,
        'created_at': photo.created_at.strftime('%d.%m.%Y'),
    }
    return JsonResponse(data)
def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            auth_login(request, user)
            return redirect('home')  
    else:
        form = CustomUserCreationForm()
    return render(request, 'registration/signup.html', {'form': form})


class CustomLoginView(LoginView):
    authentication_form = CustomAuthenticationForm
    template_name = 'registration/login.html'
    redirect_authenticated_user = True  


@login_required
def profile_view(request):
    profile, created = Profile.objects.get_or_create(user=request.user)
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile, user=request.user)
        if form.is_valid():
            form.save(user=request.user)
            messages.success(request, 'Профиль обновлён!')
            return redirect('profile')
    else:
        form = ProfileForm(instance=profile, user=request.user)

    context = {
        'form': form,
        'profile': profile,
        'user': request.user,
    }
    return render(request, 'profile/profile.html', context)

def history(request):
    events = HistoricalEvent.objects.all()
    selected_category = request.GET.get('category', '')
    if selected_category:
        events = events.filter(category=selected_category)
    categories = HistoricalEvent.CATEGORY_CHOICES
    context = {
        'events': events,
        'categories': categories,
        'selected_category': selected_category,
    }
    return render(request, 'main/history.html', context)
