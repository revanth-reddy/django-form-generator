from django.http.response import JsonResponse, HttpResponse
from django.views.generic.base import View
from form_design_app.models import Field, Form, Choice
from django.views.decorators.csrf import ensure_csrf_cookie
from django.utils.decorators import method_decorator
import json


@method_decorator(ensure_csrf_cookie, name='dispatch')
class FormListView(View):
    def get(self, request):
        forms = list(Form.objects.all().values('id', 'title'))
        if not forms:
            return HttpResponse(status=200, content='No form exists')

        if 'format' in request.GET:
            if request.GET['format'] == 'json':
                return JsonResponse(forms, safe=False)
            else:
                # Other formats such as XML could be implemented
                return HttpResponse(status=400, content='Unsupported format')

        # Default format is json. This could change to other formats.
        return JsonResponse(forms, safe=False)

    def post(self, request):
        data = json.loads(request.body.decode())
        form = Form.objects.create(title=data['form_title'])
        for item in data['fields']:
            field = Field.objects.create(
                form=form,
                title=item['title'],
                type=item['type'],
                required=item['required'],
                admin_only=item['admin_only']
            )

            if item['type'] == 'select':
                for choice in item['choices']:
                    Choice.objects.create(
                        field=field,
                        value=choice['value'],
                        text=choice['text']
                    )

        return HttpResponse('Successfully added form')


@method_decorator(ensure_csrf_cookie, name='dispatch')
class FormView(View):
    def get(self, request, form_id):
        try:
            form = Form.objects.get(id=form_id)
        except Form.DoesNotExist:
            return HttpResponse(status=404, content='Form not found')

        fields = Field.objects.filter(form__id=form_id).values('id', 'title', 'type', 'required', 'admin_only', 'style')

        fields_list = list()
        for field in fields:
            choices = list(Choice.objects.filter(field__id=field['id']).values('value', 'text'))
            if choices:
                field['choices'] = choices
            fields_list.append(field)

        output = dict()
        output['form_id'] = form.id
        output['form_title'] = form.title
        output['fields'] = fields_list

        if 'format' in request.GET:
            if request.GET['format'] == 'json':
                return JsonResponse(output, safe=False)
            else:
                return HttpResponse(status=400, content='Unsupported format')

        return JsonResponse(output, safe=False)

    def put(self, request, form_id):
        try:
            form = Form.objects.get(id=form_id)
        except Form.DoesNotExist:
            return HttpResponse(status=404, content='Form not found')

        Field.objects.filter(form__id=form_id).delete()
        Choice.objects.filter(field__form__id=form_id).delete()

        data = json.loads(request.body.decode())

        form.title = data['form_title']
        form.save()

        for item in data['fields']:
            field = Field.objects.create(
                form=form,
                title=item['title'],
                type=item['type'],
                required=item['required'],
                admin_only=item['admin_only']
            )

            if item['type'] == 'select':
                for choice in item['choices']:
                    Choice.objects.create(field=field, value=choice['value'], text=choice['text'])

        return HttpResponse('Successfully modified form')

    def delete(self, request, form_id):
        try:
            form = Form.objects.get(id=form_id)
        except Form.DoesNotExist:
            return HttpResponse(status=404, content='Form not found')

        Field.objects.filter(form__id=form_id).delete()
        Choice.objects.filter(field__form__id=form_id).delete()
        form.delete()

        return HttpResponse('Successfully deleted form')