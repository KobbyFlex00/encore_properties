from django.shortcuts import render, get_object_or_404
from django.db.models import Q
from django.contrib import messages
from .models import Property, Location, Category


def property_list(request):
    properties = Property.objects.filter(is_available=True)

    # Filter Query Parameters
    listing_type = request.GET.get('listing_type')
    location_id = request.GET.get('location')
    category_id = request.GET.get('category')
    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')
    bedrooms = request.GET.get('bedrooms')
    search_query = request.GET.get('q')

    # Apply Filters
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

    context = {
        'properties': properties,
        'locations': locations,
        'categories': categories,
        'selected_listing_type': listing_type,
        'selected_location': location_id,
        'selected_category': category_id,
    }

    # HTMX Check: Return partial grid if request comes from HTMX AJAX filter
    if request.headers.get('HX-Request'):
        return render(request, 'properties/partials/property_grid.html', context)

    return render(request, 'properties/property_list.html', context)


def property_detail(request, slug):
    property_obj = get_object_or_404(Property, slug=slug, is_available=True)
    
    # Process amenities string into a clean list for template display
    amenities_list = [a.strip() for a in property_obj.amenities.split(',')] if property_obj.amenities else []

    # Fetch similar properties in the same location
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
    """Renders the About Us page."""
    context = {
        'total_properties': Property.objects.filter(is_available=True).count(),
        'total_locations': Location.objects.count(),
    }
    return render(request, 'about.html', context)


def contact_view(request):
    """Renders the Contact Us page & processes inquiries."""
    if request.method == 'POST':
        name = request.POST.get('name')
        phone = request.POST.get('phone')
        email = request.POST.get('email')
        message = request.POST.get('message')
        
        # Trigger success feedback message
        messages.success(
            request, 
            f"Thank you {name}! Your message has been received. Our sales desk will call you back shortly."
        )
        
    return render(request, 'contact.html')