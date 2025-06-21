from django.contrib import admin
from .models import Category, Brand, Product, ProductImage, ProductSpecification


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    search_fields = ['name']
    prepopulated_fields = {'slug': ('name',)}#prep_fiel это автозаполняемые поля


@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    search_fields = ['name']
    prepopulated_fields = {'slug': ('name',)}

class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1

class ProductSpecificationInline(admin.TabularInline):
    model = ProductSpecification
    extra = 1


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'brand', 'color', 'price',
    'is_available', 'is_featured', 'created_at']
    list_filter = ['category', 'brand', 'color', 'is_available', 'is_featured',
    'is_new', 'is_sale', 'created_at']
    search_fields = ['name', 'description', 'short_description']
    prepopulated_fields = {'slug': ('name',)}
    inlines = [ProductImageInline, ProductSpecificationInline]

    fieldsets = (
        ('Основная информация', {
            'fields': ['name', 'slug', 'category', 'brand',
            'description', 'short_description']
        }),
        ('Характеристики', {
            'fields': ['model_year', 'color', 'storage']
        }),
        ('Цены и наличие', {
            'fields': ['price', 'old_price', 'is_available', 
            'stock_quantity']
        }),
        ('Изображения', {
            'fields': ['main_image']
        }),
        ('SEO', {
            'fields': ['meta_title', 'meta_description'],
            'classes': ['collapse',]
        }),
        ('Статус', {
            'fields': ['is_featured', 'is_new', 'is_sale']
        }),
    )