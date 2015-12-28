__author__ = 'mousavi'
import models
for i in range(1000):
    category = models.Category.create(category_unique=str(i), category_name='mehdi', category_link='link')
    category.save()