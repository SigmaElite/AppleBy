from .models import Category

def categories_processor(request):
    #Добавляет категории во все шаблоны
    return {
        'categories': Category.objects.all()
    }