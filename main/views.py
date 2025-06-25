from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from .models import Product, Category, Brand


def home(request):
    # Получаем рекомендуемые товары
    featured_products = Product.objects.filter(is_featured=True, is_available=True)[:8]
    new_products = Product.objects.filter(is_new=True, is_available=True)[:8]
    sale_products = Product.objects.filter(is_sale=True, is_available=True)[:8]
    categories = Category.objects.all()

    context = {
        'featured_products': featured_products,
        'new_products': new_products,
        'sale_products': sale_products,
        'categories': categories,
    }
    return render(request, 'main/product/home.html', context)


def product_list(request):
    products = Product.objects.filter(is_available=True)

    # Фильтрация по категории, ниже по бренду 
    category_slug = request.GET.get('category')
    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        products = products.filter(category=category)
    
    brand_slug = request.GET.get('brand')
    if brand_slug:
        brand = get_object_or_404(Brand, slug=brand_slug)
        products = products.filter(brand=brand)
    
    sort_by = request.GET.get('sort', 'name')
    if sort_by == 'price_low':
        products = products.order_by('price')
    elif sort_by == 'price_high':
        products = products.order_by('-price')
    elif sort_by == 'newest':
        products = products.order_by('-created_at')
    else:
        products = products.order_by('name')
    
    # Пагинация
    paginator = Paginator(products, 12)#Разбивает products на страницы по 12 элементов на каждой
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)#для безопас получ стр(номер)

    context = {
        'page_obj': page_obj,
        'categoties': Category.objects.all(),
        'brands': Brand.objects.all(),
    }
    return render(request, 'main/product/product_list.html', context)

def product_detail(request, slug):
    product = get_object_or_404(Product, slug=slug, is_available=True)#закид объект с продукта если слаг совпад и достпуность тру
    related_products = Product.object.filter(category=product.category, is_availalbe=True).exclude(id=product.id)[:4]#ex исключ одинаковые товары и показ макс 4 

    context = {
        'product': product,
        'related_products': related_products,
    }
    return(request, 'main/product/product_detail.html', context)


def category_detail(request, slug):
    category = get_object_or_404(Category, slug=slug)
    products = Product.objects.filter(category=category, is_available=True)

    sort_by = request.GET.get('sort', 'name')
    if sort_by == 'price_low':
        products = products.order_by('price')
    elif sort_by == 'price_high':
        products = products.order_by('-price')
    elif sort_by == 'newest':
        products = products.order_by('-created_at')
    else:
        products = products.order_by('name')
    
    paginator = Paginator(products, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'category': category,
        'page_obj': page_obj,
    }
    return render(request, 'main/product/category_detail.html', context)