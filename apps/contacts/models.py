from django.db import models


class ContactInfo(models.Model):
    address = models.TextField()
    phone = models.CharField(max_length=20)
    email = models.EmailField()
    working_hours = models.CharField(max_length=100)
    map_embed_code = models.TextField(blank=True)

    def get_working_hours_list(self):
        if self.working_hours:
            return str(self.working_hours).split(";")
        return []


class Feedback(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=20, blank=True)
    subject = models.CharField(max_length=200)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_processed = models.BooleanField(default=False)

    def get_short_message(self):
        return self.message[:50] + "..." if len(self.message) > 50 else self.message

    get_short_message.short_description = "Сообщение"


class Branch(models.Model):
    name = models.CharField("Название филиала", max_length=100)
    address = models.TextField("Адрес")
    phone = models.CharField("Телефон", max_length=20)
    email = models.EmailField("Email")
    working_hours = models.CharField("Режим работы", max_length=100)
    map_embed_code = models.TextField("Код карты", blank=True)
    photo = models.ImageField("Фото", upload_to="branches/", null=True, blank=True)
    is_main = models.BooleanField("Главный филиал", default=False)
    order = models.PositiveIntegerField("Порядок отображения", default=0)

    class Meta:
        verbose_name = "Филиал"
        verbose_name_plural = "Филиалы"
        ordering = ["order"]

    def __str__(self):
        return self.name

    def get_map_iframe(self):
        return self.map_embed_code.replace('width="600"', 'width="100%"')
