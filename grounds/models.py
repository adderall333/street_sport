from django.db import models

import datetime


DISTRICTS = [
        ('Приволжский', 'Приволжский'),
        ('Московский', 'Московский'),
        ('Советский', 'Советский'),
        ('Вахитовский', 'Вахитовский'),
        ('Ново-Савиновский', 'Ново-Савиновский'),
        ('Кировский', 'Кировский'),
        ('Авиастроительный', 'Авиастроительный')
    ]

TYPES = [
        ('Футбол', 'football'),
        ('Баскетбол', 'basketball'),
        ('Волейбол', 'volleyball'),
        ('Хоккей', 'hockey')
    ]


class Ground(models.Model):
    district = models.CharField(max_length=20, choices=DISTRICTS)
    coordinates = models.CharField(max_length=50)
    short_description = models.CharField(max_length=50)
    long_description = models.TextField()
    last_update = models.DateField()
    main_image = models.ImageField()
    type = models.CharField(max_length=20, choices=TYPES)
    is_confirmed = models.BooleanField(default=False)

    def add(self, request):
        """Заполняет и сохраняет объект площадки в БД"""
        self.district = request.POST.get('dis')
        self.coordinates = request.POST.get('crd')
        self.short_description = request.POST.get('sh_desc')
        self.long_description = request.POST.get('ln_desc')
        self.last_update = datetime.datetime.now()
        self.save()
        imgs = request.FILES.getlist('img')
        if imgs:
            self.main_image = imgs[0]
        for img in imgs:
            image = Image()
            image.ground = self
            image.image = img
            image.save()
        self.type = request.POST.get('tps')
        self.is_confirmed = False
        self.save()

    def edit(self, request):
        """Заполняет и сохраняет объект изменений площадки в БД"""
        changes = Changes()
        changes.ground = self
        changes.district = request.POST.get('dis')
        changes.coordinates = request.POST.get('crd')
        changes.short_description = request.POST.get('sh_desc')
        changes.long_description = request.POST.get('ln_desc')
        changes.last_update = datetime.datetime.now()
        imgs = request.FILES.getlist('img')
        for img in imgs:
            image = Image()
            image.ground = changes
            image.image = img
            image.save()
        changes.type = request.POST.get('tps')
        changes.save()

    def get_x(self):
        """Возвращает широту объекта площадки"""
        return float(self.coordinates.split()[0])

    def get_y(self):
        """Возвращает долготу объекта площадки"""
        return float(self.coordinates.split()[1])

    def close_grounds(self):
        """Возвращает три ближайшие площадки"""
        grounds = sorted(Ground.objects.exclude(id=self.id),
                         key=lambda ground: self.get_x() * self.get_y() + ground.get_x() * ground.get_y())
        if len(grounds) < 3:
            return grounds
        else:
            return [grounds[i] for i in range(3)]

    def __str__(self):
        return self.short_description

    class Meta:
        verbose_name = 'Площадка'
        verbose_name_plural = 'Площадки'

    def delete(self, *args, **kwargs):
        super(Ground, self).delete(*args, **kwargs)
        if self.main_image:
            storage, path = self.main_image.storage, self.main_image.path
            storage.delete(path)


class Changes(models.Model):
    ground = models.ForeignKey(Ground, on_delete=models.CASCADE)
    district = models.CharField(max_length=20, choices=DISTRICTS)
    coordinates = models.CharField(max_length=30)
    short_description = models.CharField(max_length=50)
    long_description = models.TextField()
    type = models.CharField(max_length=20, choices=TYPES)
    last_update = models.DateField()

    def __str__(self):
        return self.short_description

    class Meta:
        verbose_name = 'Изменение площадки'
        verbose_name_plural = 'Изменения площадки'


class Image(models.Model):
    ground = models.ForeignKey(Ground, on_delete=models.CASCADE)
    image = models.ImageField()

    def add(self, gr, img):
        """Добавляет изображение к объекту площадки"""
        self.ground = gr
        self.image = img

    class Meta:
        verbose_name = 'Картинка'
        verbose_name_plural = 'Картинки'

    def delete(self, *args, **kwargs):
        super(Image, self).delete(*args, **kwargs)
        if self.image:
            storage, path = self.image.storage, self.image.path
            storage.delete(path)
