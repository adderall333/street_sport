from django.db import models
import datetime


class Ground(models.Model):
    DISTRICTS = [
        'Приволжский',
        'Московский',
        'Советский',
        'Вахитовский',
        'Ново-Савиновский',
        'Кировский',
        'Авиастроительный'
    ]

    TYPES = [
        'Футбол',
        'Баскетбол',
        'Волейбол',
        'Хоккей'
    ]

    district = models.CharField(max_length=20, choices=DISTRICTS)
    coordinates = models.CharField(max_length=30)
    short_description = models.CharField(max_length=50)
    long_description = models.TextField()
    last_update = models.DateField()
    main_image = models.ImageField()
    types = models.CharField(max_length=20, choices=TYPES)

    def add_or_edit(self, dis=district, crd=coordinates, sh_desc=short_description, ln_desc=long_description, img=main_image, tps=types):
        self.district = dis
        self.coordinates = crd
        self.short_description = sh_desc
        self.long_description = ln_desc
        self.last_update = datetime.datetime.now()
        self.main_image = img
        self.types = tps

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


class Image(models.Model):
    ground = models.ForeignKey(Ground, on_delete=models.CASCADE)
    image = models.ImageField()

    def add(self, gr, img):
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


class Comment(models.Model):
    ground = models.ForeignKey(Ground, on_delete=models.CASCADE)
    pub_date = models.DateTimeField()
    author = models.CharField(max_length=50)
    text = models.TextField()

    def add(self, gr, date, auth, txt):
        self.ground = gr
        self.pub_date = date
        self.author = auth
        self.text = txt

    def __str__(self):
        return self.text

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'

