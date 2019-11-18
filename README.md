Django form generator

> PostgreSQL used in this project as database. Form designs are stored 
  in regular relational tables. Form data are stored in json format using
  postgres json type and django JsonField

> test folder contains some test cases for form design.
> screenshots folder contains output pictures in browser using JsonView extension

> Database "FormGenDB" should be created in PostgreSQL before migrate

--------------------------------------------------------
--------------------------------------------------------
--------------------------------------------------------

How to run:

	- $: pip install -r requirements.txt
	- $: python manage.py makemigrations
	- $: python manage.py migrate
	- $: python manage.py runserver 127.0.0.1:8000

Run test (get, add, edit, delete form design):

	- $: python test/form_design.py
		

--------------------------------------------------------
--------------------------------------------------------
--------------------------------------------------------

All urls and implementations are RESTful compatible. 
	- based on: https://en.wikipedia.org/wiki/Representational_state_transfer#Relationship_between_URL_and_HTTP_methods
	
API Doc:

	/api/design/forms/
        GET:
            - input: format (define output format)
            - output: List of all existing forms
            
        POST:
            - input: json string.
                     sample:
                     {
                            'title': [title],
                            'fields': [
                                {
                                    'title': [title],
                                    'type': text | number | date | select
                                    'required': true | false
                                    'admin_only': true | false
                                    'choices': [
                                        {
                                            'value': [value],
                                            'text': [text]
                                        },
                                        }
                                        { ... },
                                    ]
                                },
                                { ... },
                                ...
                            ]
                     }
    
            - output: success message


    /api/design/forms/<form_id>/
        GET:
            - input: format [optional] (currently json supported)
            - output: Details of the specified form

        PUT:
            - input: json string
                     sample:
                     {
                            'title': [title],
                            'fields': [
                                {
                                    'title': [title],
                                    'type': text | number | date | select
                                    'required': true | false
                                    'admin_only': true | false
                                    'choices': [
                                        {
                                            'value': [value],
                                            'text': [text]
                                        },
                                        }
                                        { ... },
                                    ]
                                },
                                { ... },
                                ...
                            ]
                     }
            - output: success message

        DELETE:
            - input: -
            - output: success message


    /api/data/forms/
        GET:
            input: -
            output: Form list page



    /api/data/forms/<form_id>/records/
        GET:
            - input: format [optional] (currently json supported)
            - output: List of records related to the specified form

        POST:
            - input: form fields (field_id: value)
            - output: redirect to records list page


    /api/data/forms/<form_id>/records/<record_id>/
        GET:
            - input: format [optional] (currently json supported)
            - output: record details

        POST: (This method is just a fallback for old HTML forms which not support PUT and DELETE methods)
        	- input: _method (PUT or DELETE)
			- output: redirect to put or delete method

	    PUT:
	        - input: form fields (field_id: value)
	        - output: success message

	    DELETE:
	        - input: -
	        - output: redirect to records list page


--------------------------------------------------------
--------------------------------------------------------
--------------------------------------------------------
		
		
Additional Info:

	tested on:
		- OS: Windows 10
		- Interpreter: Python 3.5.2
		- Web framework: Django 1.10
		- Database: PostgreSQL 9.6
		
--------------------------------------------------------
--------------------------------------------------------
--------------------------------------------------------

Future works:

	- Validate inputs
	- Handle possible exceptions
	- Add UI
	
	

