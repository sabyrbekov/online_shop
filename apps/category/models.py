from django.db import models

class Category(models.Model):
    title = models.CharField(
        max_length=255, db_index=True,
        )
    parent = models.ForeignKey(
        'self', on_delete=models.CASCADE, null=True, blank=True,
        related_name='children'
    )

    class Meta:
        ordering = ('title', )
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        if self.parent:
            return f"{self.parent} --> {self.title}"
        return self.title

class Brand(models.Model):
    title = models.CharField(max_length=100, db_index=True)
    image = models.ImageField(upload_to='brands', blank=True)

    class Meta:
        verbose_name = 'Бренд'
        verbose_name_plural = 'Бренды'

    def __str__(self):
        return self.title



