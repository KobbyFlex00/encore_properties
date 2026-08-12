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
    ref_code = models.CharField(max_length=20, unique=True, help_text="e.g. EP-101 or #JJ_001")
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

    main_image = CloudinaryField('image', blank=True, null=True, help_text="Optional. Leave blank if using a social media link.")
    social_media_url = models.URLField(
        max_length=500, 
        blank=True, 
        null=True, 
        help_text="Paste link from Instagram, TikTok, YouTube, Facebook, X, or Snapchat."
    )

    is_featured = models.BooleanField(default=False)
    is_available = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = "Properties"
        ordering = ['-created_at']

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(f"{self.title}-{self.ref_code}")
        super().save(*args, **kwargs)

    def get_whatsapp_link(self):
        phone = "233598870757"
        msg = f"Hello Encore Properties, I am interested in viewing {self.title} (Ref: #{self.ref_code}) listed at {self.currency} {self.price:,.2f}. Please provide more details."
        return f"https://wa.me/{phone}?text={urllib.parse.quote(msg)}"

    def get_thumbnail_url(self):
        """Returns main image URL or auto-generated YouTube thumbnail."""
        if self.main_image:
            return self.main_image.url
        
        url = self.social_media_url or ""
        if "youtube.com" in url or "youtu.be" in url:
            video_id = ""
            if "youtu.be" in url:
                video_id = url.split("/")[-1].split("?")[0]
            elif "v=" in url:
                video_id = url.split("v=")[1].split("&")[0]
            if video_id:
                return f"https://img.youtube.com/vi/{video_id}/hqdefault.jpg"
        return None

    def get_social_platform_info(self):
        """Parses URLs into live embeddable URLs."""
        url = self.social_media_url or ""
        
        # Instagram Embed Handler
        if "instagram.com" in url:
            match = re.search(r'instagram\.com/(?:p|reel|tv)/([^/?#&]+)', url)
            post_id = match.group(1) if match else ""
            embed_url = f"https://www.instagram.com/p/{post_id}/embed" if post_id else ""
            return {
                "platform": "instagram", 
                "embed_url": embed_url, 
                "is_embeddable": bool(embed_url),
                "icon": "fa-brands fa-instagram", 
                "color": "from-purple-600 via-pink-500 to-amber-500"
            }
        
        # YouTube Embed Handler
        elif "youtube.com" in url or "youtu.be" in url:
            video_id = ""
            if "youtu.be" in url:
                video_id = url.split("/")[-1].split("?")[0]
            elif "v=" in url:
                video_id = url.split("v=")[1].split("&")[0]
            embed_url = f"https://www.youtube.com/embed/{video_id}" if video_id else url
            return {
                "platform": "youtube", 
                "embed_url": embed_url, 
                "is_embeddable": True,
                "icon": "fa-brands fa-youtube", 
                "color": "bg-red-600"
            }
            
        elif "tiktok.com" in url:
            return {"platform": "tiktok", "url": url, "is_embeddable": False, "icon": "fa-brands fa-tiktok", "color": "bg-black"}
        elif "facebook.com" in url:
            return {"platform": "facebook", "url": url, "is_embeddable": False, "icon": "fa-brands fa-facebook", "color": "bg-blue-600"}
        elif "x.com" in url or "twitter.com" in url:
            return {"platform": "x", "url": url, "is_embeddable": False, "icon": "fa-brands fa-x-twitter", "color": "bg-slate-900"}
        elif "snapchat.com" in url:
            return {"platform": "snapchat", "url": url, "is_embeddable": False, "icon": "fa-brands fa-snapchat", "color": "bg-yellow-400 text-black"}
            
        return {"platform": "generic", "url": url, "is_embeddable": False, "icon": "fa-solid fa-link", "color": "bg-brand-green text-black"}

    def __str__(self):
        return f"{self.ref_code} - {self.title}"


class PropertyImage(models.Model):
    property = models.ForeignKey(Property, on_delete=models.CASCADE, related_name='gallery')
    image = CloudinaryField('image', blank=True, null=True)
    caption = models.CharField(max_length=150, blank=True)

    def __str__(self):
        return f"Gallery Image for {self.property.title}"