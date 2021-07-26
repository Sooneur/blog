from django.db import models


class User(models.Model):
    id = models.AutoField(primary_key=True)
    login = models.CharField(unique=True, max_length=50, verbose_name='Логин')
    password = models.CharField(max_length=50, verbose_name='Пароль')
    email = models.EmailField(max_length=100, verbose_name='Email')
    registered = models.DateTimeField(auto_now_add=True, verbose_name='Дата публикации')
    is_online = models.BooleanField(default=False, verbose_name='Сейчас онлайн')
    was_online = models.DateTimeField(auto_now=True, verbose_name='Обновлено')

    def __str__(self):
        return f'{self.id}: {self.login}'

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        ordering = ['login', 'is_online', 'was_online', 'registered']


class Note(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User.id, on_delete=models.PROTECT)
    title = models.CharField(max_length=150, verbose_name='Наименование')
    content = models.TextField(verbose_name='Контент')
    created = models.DateTimeField(auto_now_add=True, verbose_name='Дата публикации')
    updated = models.DateTimeField(auto_now=True, verbose_name='Обновлено')
    is_published = models.BooleanField(default=False, verbose_name='Опубликовано')
    published = models.DateTimeField(null=True, verbose_name='Обновлено')
    category = models.ForeignKey('Category', on_delete=models.PROTECT, null=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Запись'
        verbose_name_plural = 'Записи'
        ordering = ['-created', 'title']


class File(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User.id, on_delete=models.PROTECT)
    title = models.CharField(max_length=150, verbose_name='Наименование')
    file = models.FileField(upload_to='%Y%m%d%', verboze_name='Файл')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Файл'
        verbose_name_plural = 'Файлы'
        ordering = ['user', 'title', 'id']


class NoteFileConnection(models.Model):
    note = models.ForeignKey(Note.id, on_delete=models.PROTECT)
    file = models.ForeignKey(File.id, on_delete=models.PROTECT)

    def __str__(self):
        return self.note, self.file

    class Meta:
        verbose_name = 'Запись'
        verbose_name_plural = 'Записи'
        ordering = ['note', 'file']


class Like(models.Model):
    user = models.ForeignKey(User.id, on_delete=models.CASCADE)
    note = models.ForeignKey(Note.id, on_delete=models.PROTECT)
