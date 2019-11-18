from django.db import models
from django.contrib.postgres.fields import JSONField
from form_design_app.models import Form


class FormData(models.Model):
    form = models.ForeignKey(Form, on_delete = models.CASCADE)
    data = JSONField()
    create_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = 'Form Data'

    def __str__(self):
        return self.form.title + ' ' + str(self.id)
