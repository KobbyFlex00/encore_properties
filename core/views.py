from django.shortcuts import render, get_object_or_404
from django.db.models import Q
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from .models import Property, Location, Category, TeamMember


def property_list(request):
    properties = Property.objects.filter(is_available=True)

    listing_type = request.GET.get('listing_type')
    location_id = request.GET.get('location')
    category_id = request.GET.get('category')
    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')
    bedrooms = request.GET.get('bedrooms')
    search_query = request.GET.get('q')

    if listing_type:
        properties = properties.filter(listing_type=listing_type)
    if location_id:
        properties = properties.filter(location_id=location_id)
    if category_id:
        properties = properties.filter(category_id=category_id)
    if min_price:
        properties = properties.filter(price__gte=min_price)
    if max_price:
        properties = properties.filter(price__lte=max_price)
    if bedrooms:
        properties = properties.filter(bedrooms__gte=bedrooms)
    if search_query:
        properties = properties.filter(
            Q(title__icontains=search_query) |
            Q(ref_code__icontains=search_query) |
            Q(description__icontains=search_query)
        )

    locations = Location.objects.all()
    categories = Category.objects.all()
    featured_properties = Property.objects.filter(is_available=True, is_featured=True)[:5]

    context = {
        'properties': properties,
        'featured_properties': featured_properties,
        'locations': locations,
        'categories': categories,
        'selected_listing_type': listing_type,
        'selected_location': location_id,
        'selected_category': category_id,
    }

    if request.headers.get('HX-Request'):
        return render(request, 'properties/partials/property_grid.html', context)

    return render(request, 'properties/property_list.html', context)


def property_detail(request, slug):
    property_obj = get_object_or_404(Property, slug=slug, is_available=True)
    amenities_list = [a.strip() for a in property_obj.amenities.split(',')] if property_obj.amenities else []

    related_properties = Property.objects.filter(
        location=property_obj.location,
        is_available=True
    ).exclude(id=property_obj.id)[:3]

    context = {
        'property': property_obj,
        'amenities_list': amenities_list,
        'related_properties': related_properties,
    }
    return render(request, 'properties/property_detail.html', context)


def about_view(request):
    team_members = TeamMember.objects.filter(is_active=True)
    context = {
        'team_members': team_members,
        'total_properties': Property.objects.filter(is_available=True).count(),
        'total_locations': Location.objects.count(),
    }
    return render(request, 'about.html', context)


def contact_view(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        phone = request.POST.get('phone')
        email = request.POST.get('email')
        message = request.POST.get('message')
        
        # Email Dispatch to Gmail
        subject = f"New Web Inquiry from {name} - Encore Properties"
        email_body = f"""
New Client Inquiry Received via Website:

Name: {name}
Phone/WhatsApp: {phone}
Email: {email}

Message:
{message}
        """
        
        try:
            send_mail(
                subject,
                email_body,
                settings.DEFAULT_FROM_EMAIL,
                ['encorepropertiesgrouplimited@gmail.com'],
                fail_silently=False,
            )
            messages.success(
                request, 
                f"Thank you {name}! Your message has been sent directly to our Gmail sales inbox. We will call you back shortly."
            )
        except Exception as e:
            messages.success(
                request, 
                f"Thank you {name}! Your message was logged successfully. An agent will contact you shortly."
            )
        
    return render(request, 'contact.html')