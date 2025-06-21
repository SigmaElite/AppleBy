from django.db import models
from django.urls import reverse

class Category(models.Model):
    name = models.CharField(max_length=100, verbose_name='Название категории')
    slug = models.SlugField(max_length=100, unique=True)
    image = models.ImageField(upload_to='categories/%Y/%m/%d/', blank=True, null=True)

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
        ordering = ['name']  #сортировка по имени
    
    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse("main:category_detail", kwargs={"slug": self.slug})
    

class Brand(models.Model):
    """Бренды (в основном Apple, но можно добавить аксессуары других брендов)"""
    name = models.CharField(max_length=50)
    slug = models.SlugField(max_length=50, unique=True)
    logo = models.ImageField(upload_to='brands/', blank=True, null=True)
    
    class Meta:
        verbose_name = "Бренд"
        verbose_name_plural = "Бренды"
        ordering = ['name']
    
    def __str__(self):
        return self.name
    

class Product(models.Model):
    COLOR_CHOICES = [   #1 тех назв(хран в бд) 2 человекочитаемое
        ('space_gray', 'Space Gray'),
        ('silver', 'Silver'),
        ('gold', 'Gold'),
        ('rose_gold', 'Rose Gold'),
        ('midnight', 'Midnight'),
        ('starlight', 'Starlight'),
        ('blue', 'Blue'),
        ('pink', 'Pink'),
        ('purple', 'Purple'),
        ('red', 'Red'),
        ('green', 'Green'),
        ('yellow', 'Yellow'),
        ('white', 'White'),
        ('black', 'Black')
    ]

    STORAGE_CHOICES = [
        ('64GB', '64GB'),
        ('128GB', '128GB'),
        ('256GB', '256GB'),
        ('512GB', '512GB'),
        ('1TB', '1TB'),
        ('2TB', '2TB'),
        ('4TB', '4TB'),
        ('8TB', '8TB'),
    ]

    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE)

    description = models.TextField()
    short_description = models.CharField(max_length=300)

    model_year = models.PositiveIntegerField(null=True, blank=True)
    color = models.CharField(max_length=20, choices=COLOR_CHOICES)#ch огранич ввод тольок теми вариками
    storage = models.CharField(max_length=10, choices=STORAGE_CHOICES)
    
    price = models.DecimalField(max_digits=10, decimal_places=2)
    old_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    is_available = models.BooleanField(default=True)
    stock_quantity = models.BooleanField(default=True, verbose_name='наличие на складе')

    main_image = models.ImageField(upload_to='product/%Y/%m/%d/', blank=True, null=True)

    # SEO
    meta_title = models.CharField(max_length=200, blank=True, verbose_name="Meta Title")
    meta_description = models.CharField(max_length=300, blank=True, verbose_name="Meta Description")

    is_featured = models.BooleanField(default=False)
    is_new = models.BooleanField(default=False)
    is_sale = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Продукт'
        verbose_name_plural = 'Продукты'
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.name} - {self.color}'
    
    def get_absolute_url(self):
        return reverse("main:product_detail", kwargs={"slug": self.slug})
 
    @property   #для автоматического расчета процента скидки на товар
    def discount_percentage(self):
        if self.old_price and self.old_price > self.price:
            return int(((self.old_price - self.price) / self.old_price) * 100)
        return 0 
    

class ProductImage(models.Model):
    product = models.ForeignKey(Product, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='products/gallery/')
    alt_text = models.CharField(max_length=100, blank=True)
    order = models.PositiveIntegerField(default=0)#ручная сортировка

    class Meta:
        verbose_name = 'изображение продукта'
        verbose_name_plural = 'изображения продуктов'
        ordering = ['order']

    def __str__(self):
        return f"Изображение для {self.product.name}"
    

class ProductSpecification(models.Model):  #Технические характеристики продукта
    product = models.ForeignKey(Product, related_name='specification', on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    value = models.CharField(max_length=200)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        verbose_name = 'Характеристика'
        verbose_name_plural = 'Характеристики'
        ordering = ['order']

    def __str__(self):
        return f'{self.name.product} - {self.name} - {self.value}'