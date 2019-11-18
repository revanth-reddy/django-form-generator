import requests

url = 'http://127.0.0.1:8000/api/design/forms/'


def get_forms_list():
    response = requests.get(url)
    print(response.content)


def add_form():
    with requests.Session() as s:

        # get list of existing forms
        # this is just for get csrf token
        response = s.get(url)

        data = {
            'form_title': 'profile',
            'fields': [
                {
                    'title': 'name',
                    'type': 'text',
                    'required': True,
                    'admin_only': False
                },
                {
                    'title': 'age',
                    'type': 'number',
                    'required': False,
                    'admin_only': False
                },
                {
                    'title': 'gender',
                    'type': 'select',
                    'required': False,
                    'admin_only': False,
                    'choices': [
                        {
                            'value': 1,
                            'text': 'male'
                        },
                        {
                            'value': 0,
                            'text': 'female'
                        }
                    ]
                },
                {
                    'title': 'birthday',
                    'type': 'date',
                    'required': False,
                    'admin_only': False
                }
            ]
        }

        s.headers.update({'X-CSRFToken': s.cookies.get('csrftoken')})
        s.headers.update({'Content-type': 'application/json'})

        # request for adding new form
        response = s.post(url=url, json=data)
        print(response.content)


def get_form(form_id):
    # get a form by requesting it's ID
    response = requests.get(url + str(form_id) + '/')
    print(response.content)


def edit_form(form_id):
    with requests.Session() as s:
        # get a form by requesting it's ID
        response = s.get(url + str(form_id) + '/')
        print(response.content)

        data = {
            'form_title': 'profile',
            'fields': [
                {
                    'title': 'full_name',
                    'type': 'text',
                    'required': True,
                    'admin_only': False
                },
                {
                    'title': 'age',
                    'type': 'number',
                    'required': True,
                    'admin_only': False
                },
                {
                    'title': 'gender',
                    'type': 'select',
                    'required': True,
                    'admin_only': False,
                    'choices': [
                        {
                            'value': 1,
                            'text': 'male'
                        },
                        {
                            'value': 0,
                            'text': 'female'
                        }
                    ]
                },
                {
                    'title': 'birthday',
                    'type': 'date',
                    'required': False,
                    'admin_only': False
                }
            ]
        }

        s.headers.update({'X-CSRFToken': s.cookies.get('csrftoken')})
        s.headers.update({'Content-type': 'application/json'})

        # request for adding new form
        response = s.put(url=url + str(form_id) + '/', json=data)
        print(response.content)


def delete_form(form_id):
    with requests.Session() as s:
        # get a form by requesting it's ID
        response = s.get(url + str(form_id) + '/')
        print(response.content)

        s.headers.update({'X-CSRFToken': s.cookies.get('csrftoken')})

        response = s.delete(url + str(form_id) + '/')
        print(response.content)


get_forms_list()
add_form()
# edit_form(1)
# get_form(1)
# delete_form(1)
