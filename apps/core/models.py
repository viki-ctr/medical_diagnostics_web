from django.db import models
from django.utils.translation import gettext_lazy as _


class AboutPage(models.Model):
    """
    Модель страницы 'О клинике'
    """
    title = models.CharField(_('Заголовок'), max_length=200)
    content = models.TextField(_('Основной контент'))
    mission = models.TextField(_('Миссия клиники'))
    values = models.TextField(_('Наши ценности'), help_text=_('забота, эффективность, отзывчивость'))
    updated_at = models.DateTimeField(_('Последнее обновление'), auto_now=True)
    is_active = models.BooleanField(_('Активная страница'), default=True)

    class Meta:
        verbose_name = _('Страница "О клинике"')
        verbose_name_plural = _('Страницы "О клинике"')

    def __str__(self):
        return self.title

    def values_as_list(self):
        import re
        return [v.strip() for v in re.split(r'[,.]', self.values) if v.strip()]

    def save(self, *args, **kwargs):
        if self.is_active:
            AboutPage.objects.exclude(pk=self.pk).update(is_active=False)
        super().save(*args, **kwargs)


class TeamMember(models.Model):
    """
    Модель члена команды для страницы 'О клинике'
    """
    about_page = models.ForeignKey(
        AboutPage,
        on_delete=models.CASCADE,
        related_name='team_members',
        verbose_name=_('Страница "О клинике"')
    )
    name = models.CharField(_('Имя'), max_length=100)
    position = models.CharField(_('Должность'), max_length=100)
    photo = models.ImageField(
        _('Фотография'),
        upload_to='team_photos/',
        null=True,
        blank=True
    )
    bio = models.TextField(_('Биография'))
    education = models.TextField(_('Образование'), blank=True)
    experience = models.TextField(_('Опыт работы'), blank=True)
    order = models.PositiveIntegerField(_('Порядок отображения'), default=0)
    is_visible = models.BooleanField(_('Отображать на сайте'), default=True)

    class Meta:
        verbose_name = _('Член команды')
        verbose_name_plural = _('Члены команды')
        ordering = ['order']

    def __str__(self):
        return f"{self.name} - {self.position}"


class HomePageContent(models.Model):
    """
    Модель контента главной страницы
    """
    main_title = models.CharField(_('Основной заголовок'), max_length=200)
    main_description = models.TextField(_('Основное описание'))
    featured_image = models.ImageField(
        _('Изображение'),
        upload_to='homepage/',
        help_text=_('Рекомендуемый размер: 1200x800 пикселей')
    )
    services_title = models.CharField(
        _('Заголовок блока услуг'),
        max_length=100,
        default='Наши услуги'
    )
    testimonials_title = models.CharField(
        _('Заголовок блока отзывов'),
        max_length=100,
        default='Отзывы наших пациентов'
    )
    is_active = models.BooleanField(_('Активная конфигурация'), default=True)
    updated_at = models.DateTimeField(_('Последнее обновление'), auto_now=True)

    class Meta:
        verbose_name = _('Контент главной страницы')
        verbose_name_plural = _('Контент главной страницы')

    def __str__(self):
        return f"Конфигурация главной страницы ({self.updated_at})"

    def save(self, *args, **kwargs):
        if self.is_active:
            HomePageContent.objects.exclude(pk=self.pk).update(is_active=False)
        super().save(*args, **kwargs)


class Testimonial(models.Model):
    """
    Модель отзыва для главной страницы
    """
    author = models.CharField(_('Автор'), max_length=100)
    position = models.CharField(_('Должность/статус'), max_length=100, blank=True)
    content = models.TextField(_('Текст отзыва'))
    photo = models.ImageField(
        _('Фото автора'),
        upload_to='testimonials/',
        blank=True,
        null=True
    )
    rating = models.PositiveSmallIntegerField(
        _('Рейтинг'),
        choices=[(i, i) for i in range(1, 6)],
        default=5
    )
    is_featured = models.BooleanField(_('Показывать на главной'), default=False)
    created_at = models.DateTimeField(_('Дата создания'), auto_now_add=True)

    class Meta:
        verbose_name = _('Отзыв')
        verbose_name_plural = _('Отзывы')
        ordering = ['-created_at']

    def __str__(self):
        return f"Отзыв от {self.author}"

    def stars(self):
        return '★' * self.rating + '☆' * (5 - self.rating)


class FAQ(models.Model):
    """
    Модель часто задаваемых вопросов
    """
    question = models.CharField(_('Вопрос'), max_length=255)
    answer = models.TextField(_('Ответ'))
    category = models.ForeignKey(
        'FAQCategory',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name=_('Категория')
    )
    order = models.PositiveIntegerField(_('Порядок отображения'), default=0)
    is_active = models.BooleanField(_('Активный'), default=True)

    class Meta:
        verbose_name = _('FAQ')
        verbose_name_plural = _('FAQs')
        ordering = ['order', 'question']

    def __str__(self):
        return self.question


class FAQCategory(models.Model):
    """
    Категории для FAQ
    """
    name = models.CharField(_('Название'), max_length=100)
    slug = models.SlugField(_('URL-адрес'), unique=True)
    description = models.TextField(_('Описание'), blank=True)
    order = models.PositiveIntegerField(_('Порядок отображения'), default=0)

    class Meta:
        verbose_name = _('Категория FAQ')
        verbose_name_plural = _('Категории FAQ')
        ordering = ['order', 'name']

    def __str__(self):
        return self.name


class SiteSetting(models.Model):
    """
    Основные настройки сайта
    """
    site_name = models.CharField(_('Название сайта'), max_length=100, default='МедДиагностика')
    logo = models.ImageField(
        _('Логотип'),
        upload_to='site_settings/',
        null=True,
        blank=True
    )
    favicon = models.ImageField(
        _('Фавикон'),
        upload_to='site_settings/',
        null=True,
        blank=True
    )
    phone = models.CharField(_('Телефон'), max_length=20)
    email = models.EmailField(_('Email'))
    address = models.TextField(_('Адрес'))
    working_hours = models.CharField(_('Режим работы'), max_length=100)
    facebook_url = models.URLField(_('Facebook'), blank=True)
    instagram_url = models.URLField(_('Instagram'), blank=True)
    telegram_url = models.URLField(_('Telegram'), blank=True)
    meta_description = models.TextField(_('Мета-описание'), blank=True)
    meta_keywords = models.TextField(_('Мета-ключевые слова'), blank=True)

    class Meta:
        verbose_name = _('Настройка сайта')
        verbose_name_plural = _('Настройки сайта')

    def __str__(self):
        return self.site_name

    def save(self, *args, **kwargs):
        if not self.pk:
            self.__class__.objects.all().delete()
        super().save(*args, **kwargs)
