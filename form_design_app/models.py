from django.db import models


class Form(models.Model):
    title = models.CharField(max_length=255, null=True, blank=True)
    style = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.title


class Field(models.Model):
    form = models.ForeignKey(Form, null=False, blank=False, on_delete = models.CASCADE)
    title = models.CharField(max_length=100, null=False, blank=False)
    TYPE_CHOICES = (
        ('text', 'text input'),
        ('number', 'number input'),
        ('date', 'date input'),
        ('select', 'select input')
    )
    type = models.CharField(choices=TYPE_CHOICES, max_length=6, default='text')
    required = models.BooleanField(default=False)
    admin_only = models.BooleanField(default=False)
    style = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.form.title + ' - ' + self.title


class Choice(models.Model):
    field = models.ForeignKey(Field, null=False, blank=False, on_delete = models.CASCADE)
    value = models.TextField(null=True, blank=True)
    text = models.CharField(max_length=255, null=False, blank=False)

    def __str__(self):
        return self.field.form.title + ' - ' + self.field.title + ' - ' + self.text

