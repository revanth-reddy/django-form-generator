from django.http.response import JsonResponse, HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.views.generic.base import View
from form_data_app.models import FormData
from form_design_app.models import Form, Field, Choice


class RecordListView(View):
    def get(self, request, form_id):
        try:
            form = Form.objects.get(id=form_id)
        except Form.DoesNotExist:
            return HttpResponse(status=404, content='Form not found')

        data = FormData.objects.filter(form__id=form_id)
        fields = Field.objects.filter(form__id=form_id).values('id', 'title', 'type')

        record_list = list()
        output = dict()

        for data_item in data:
            record = dict()
            record['id'] = data_item.id
            record['create_date'] = data_item.create_date
            fields_list = list()
            for field in fields:
                field['value'] = data_item.data[str(field['id'])]
                if field['type'] == 'select':
                    field['text'] = Choice.objects.get(field__id=field['id'], value=field['value']).text
                fields_list.append(field)
            record['fields'] = fields_list
            record_list.append(record)
            output['records'] = record_list

        # for fields for adding new record
        fields_list = list()
        for field in fields:
            if field['type'] == 'select':
                choices = list(Choice.objects.filter(field__id=field['id']).values('value', 'text'))
                print(choices)
                if choices:
                    field['choices'] = choices
            fields_list.append(field)
        output['fields'] = fields_list

        output['form_id'] = form.id
        output['form_title'] = form.title

        if 'format' in request.GET:
            if request.GET['format'] == 'json':
                return JsonResponse(output, safe=False)
            else:
                return HttpResponse(status=400, content='Unsupported format')

        return render(request, 'formRecordList.html', {'form': output})

    def post(self, request, form_id):
        try:
            form = Form.objects.get(id=form_id)
        except Form.DoesNotExist:
            return HttpResponse(status=404, content='Form not found')

        fields = Field.objects.filter(form__id=form_id)
        values = dict()
        for field in fields:
            values[field.id] = request.POST[str(field.id)]

        FormData.objects.create(form=form, data=values)
        return HttpResponseRedirect('/api/data/forms/' + form_id + '/records/')


class RecordView(View):
    def get(self, request, form_id, record_id):
        try:
            form = Form.objects.get(id=form_id)
        except Form.DoesNotExist:
            return HttpResponse(status=404, content='Form not found')

        try:
            record = FormData.objects.get(id=record_id)
        except FormData.DoesNotExist:
            return HttpResponse(status=404, content='Record not found')

        fields = Field.objects.filter(form__id=form_id).values('id', 'title', 'type')

        fields_list = list()
        for field in fields:
            choices = list(Choice.objects.filter(field__id=field['id']).values('value', 'text'))
            if choices:
                field['choices'] = choices

            field['value'] = record.data[str(field['id'])]
            if field['type'] == 'select':
                field['text'] = Choice.objects.get(field__id=field['id'], value=field['value']).text
            fields_list.append(field)

        output = dict()
        output['form_id'] = form.id
        output['record_id'] = record.id
        output['form_title'] = form.title
        output['fields'] = fields_list
        output['create_date'] = record.create_date

        if 'format' in request.GET:
            if request.GET['format'] == 'json':
                return JsonResponse(output, safe=False)
            else:
                return HttpResponse(status=400, content='Unsupported format')

        return render(request, 'formRecord.html', {'form': output})

    def post(self, request, form_id, record_id):
        # Define for compatibility with old HTML Forms that don't support PUT and DELETE methods
        method = request.POST['_method']
        if method.strip().lower() == 'put':
            return self.put(request, form_id, record_id)
        elif method.strip().lower() == 'delete':
            return self.delete(request, form_id, record_id)
        else:
            return HttpResponse(status=405)

    def put(self, request, form_id, record_id):
        try:
            form = Form.objects.get(id=form_id)
        except Form.DoesNotExist:
            return HttpResponse(status=404, content='Form not found')

        try:
            record = FormData.objects.get(id=record_id)
        except FormData.DoesNotExist:
            return HttpResponse(status=404, content='Record not found')

        fields = Field.objects.filter(form__id=form_id)
        values = dict()
        for field in fields:
            values[field.id] = request.POST[str(field.id)]

        record.data = values
        record.save()

        return HttpResponse('Successfully modified record')

    def delete(self, request, form_id, record_id):
        try:
            form = Form.objects.get(id=form_id)
        except Form.DoesNotExist:
            return HttpResponse(status=404, content='Form not found')

        try:
            record = FormData.objects.get(id=record_id)
        except FormData.DoesNotExist:
            return HttpResponse(status=404, content='Record not found')

        record.delete()

        return HttpResponseRedirect('/api/data/forms/' + form_id + '/records/')


class FormListView(View):
    def get(self, request):
        forms = Form.objects.all()
        if not forms:
            return HttpResponse(status=200, content='No form exists')

        if 'format' in request.GET:
            if request.GET['format'] == 'json':
                return JsonResponse(list(forms), safe=False)
            else:
                # Other formats such as XML could be implemented
                return HttpResponse(status=400, content='Unsupported format')

        return render(request, 'formList.html', {'forms': forms})