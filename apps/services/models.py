from django.db import models


class ServiceCategory(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    description = models.TextField()
    icon = models.CharField(
        max_length=50,
        default="fa-flask",
        blank=True,  # Разрешаем пустое значение
        null=True,  # Разрешаем NULL в базе
        help_text="Font Awesome icon class (например, 'fa-heart')",
    )
    is_main = models.BooleanField(default=False)

    class Meta:
        verbose_name = "Категория исследований"
        verbose_name_plural = "Категории исследований"


class Service(models.Model):
    category = models.ForeignKey(ServiceCategory, on_delete=models.CASCADE, related_name="services")
    name = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    duration = models.DurationField()
    image = models.ImageField(upload_to="services/", null=True, blank=True)
    is_available = models.BooleanField(default=True)
    preparation = models.TextField(
        "Подготовка к услуге", blank=True, help_text="Инструкции для пациента перед процедурой"
    )

    class Meta:
        verbose_name = "Услуга"
        verbose_name_plural = "Услуги"

    def __str__(self):
        return self.name
