from django.db import models
from django.utils.text import slugify
from cloudinary.models import CloudinaryField
import urllib.parse
import re


class Location(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True, blank=True)

    class Meta:
        ordering = ['name']

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True, blank=True)

    class Meta:
        verbose_name_plural = "Categories"
        ordering = ['name']

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Property(models.Model):
    LISTING_TYPES = (
        ('sale', 'For Sale'),
        ('rent', 'For Rent'),
        ('short_stay', 'Short Stay'),
        ('land', 'Land / Plot'),
    )

    CURRENCY_CHOICES = (
        ('USD', '$ (USD)'),
        ('GHS', 'GHS (₵)'),
    )

    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True, blank=True)
    
    # Ref Code auto-generated automatically (e.g. EP-001)
    ref_code = models.CharField(max_length=20, unique=True, blank=True, help_text="Auto-generated e.g. EP-001")
    
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='properties')
    location = models.ForeignKey(Location, on_delete=models.CASCADE, related_name='properties')
    listing_type = models.CharField(max_length=20, choices=LISTING_TYPES, default='sale')

    currency = models.CharField(max_length=3, choices=CURRENCY_CHOICES, default='USD')
    price = models.DecimalField(max_digits=12, decimal_places=2)

    bedrooms = models.IntegerField(default=1)
    bathrooms = models.IntegerField(default=1)
    parking_spaces = models.IntegerField(default=1)
    square_meters = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)

    description = models.TextField()
    amenities = models.TextField(help_text="Comma-separated e.g. Pool, Generator, Security")

    # Mandatory Image Upload
    main_image = CloudinaryField('image', help_text="Property primary feature photo (Required)")
    
    # Mandatory Social Media URL
    social_media_url = models.URLField(
        max_length=500, 
        help_text="Direct link to property post on Instagram, TikTok, YouTube, Facebook, X, etc. (Required)"
    )

    is_featured = models.BooleanField(default=False)
    is_available = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = "Properties"
        ordering = ['-created_at']

    def save(self, *args, **kwargs):
        # Auto-generate Ref Code if blank
        if not self.ref_code:
            last_property = Property.objects.all().order_by('id').last()
            next_id = (last_property.id + 1) if last_property else 1
            self.ref_code = f"EP-{next_id:03d}"

        if not self.slug:
            self.slug = slugify(f"{self.title}-{self.ref_code}")
            
        super().save(*args, **kwargs)

    def get_whatsapp_link(self):
        phone = "233598870757"
        msg = f"Hello Encore Properties, I am interested in viewing {self.title} (Ref: #{self.ref_code}) listed at {self.currency} {self.price:,.2f}. Please provide more details."
        return f"https://wa.me/{phone}?text={urllib.parse.quote(msg)}"

    def get_social_platform_info(self):
        """Identifies platform type for button styling."""
        url = self.social_media_url or ""
        if "instagram.com" in url:
            return {"platform": "Instagram", "icon": "fa-brands fa-instagram", "color": "bg-pink-600 hover:bg-pink-700"}
        elif "tiktok.com" in url:
            return {"platform": "TikTok", "icon": "fa-brands fa-tiktok", "color": "bg-black hover:bg-slate-900"}
        elif "youtube.com" in url or "youtu.be" in url:
            return {"platform": "YouTube", "icon": "fa-brands fa-youtube", "color": "bg-red-600 hover:bg-red-700"}
        elif "facebook.com" in url:
            return {"platform": "Facebook", "icon": "fa-brands fa-facebook", "color": "bg-blue-600 hover:bg-blue-700"}
        elif "x.com" in url or "twitter.com" in url:
            return {"platform": "X (Twitter)", "icon": "fa-brands fa-x-twitter", "color": "bg-slate-900 hover:bg-black"}
        elif "snapchat.com" in url:
            return {"platform": "Snapchat", "icon": "fa-brands fa-snapchat", "color": "bg-yellow-400 text-black hover:bg-yellow-500"}
            
        return {"platform": "Social Media", "icon": "fa-solid fa-arrow-up-right-from-square", "color": "bg-brand-green text-black hover:bg-emerald-400"}

    def __str__(self):
        return f"{self.ref_code} - {self.title}"


class PropertyImage(models.Model):
    property = models.ForeignKey(Property, on_delete=models.CASCADE, related_name='gallery')
    image = CloudinaryField('image', blank=True, null=True)
    caption = models.CharField(max_length=150, blank=True)

    def __str__(self):
        return f"Gallery Image for {self.property.title}"


class TeamMember(models.Model):
    name = models.CharField(max_length=150)
    role = models.CharField(max_length=150, help_text="e.g. Chief Executive Officer, Senior Realtor")
    image = CloudinaryField('image', blank=True, null=True)
    bio = models.TextField(help_text="Brief professional background description")
    phone = models.CharField(max_length=50, blank=True, help_text="Direct phone line")
    email = models.EmailField(blank=True)
    order = models.IntegerField(default=0, help_text="Display priority (lowest first)")
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['order', 'name']

    def __str__(self):
        return f"{self.name} - {self.role}"