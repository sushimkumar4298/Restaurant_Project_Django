from django.db import models

# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length= 100)
    slug =models.SlugField(max_length= 100, unique=True)
    
    def __str__(self):
        return self.name

class MenuItem(models.Model):
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name='items'
    )
    title = models.CharField(max_length=200)
    description = models.TextField()
    price = models.DecimalField(max_digits=6, decimal_places=2)
    image = models.ImageField(upload_to='menu_items/')
    is_available = models.BooleanField(default=True)

    def __str__(self):
        return self.title