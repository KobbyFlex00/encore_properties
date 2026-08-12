from django.contrib import admin
from .models import Location, Category, Property, PropertyImage


class PropertyImageInline(admin.TabularInline):
    model = PropertyImage
    extra = 3


@admin.register(Property)
class PropertyAdmin(admin.ModelAdmin):
    list_display = ('ref_code', 'title', 'listing_type', 'location', 'currency', 'price', 'is_featured', 'is_available', 'created_at')
    list_filter = ('listing_type', 'location', 'category', 'is_featured', 'is_available')
    search_fields = ('title', 'ref_code', 'description', 'location__name')
    prepopulated_fields = {'slug': ('title', 'ref_code')}
    inlines = [PropertyImageInline]


@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}