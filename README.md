creo
====

Build system developed in python to assist with computational flows.


Django Custom Setup:

    Declare a new setting for the Component to link configurations to
    In my case I am assuming it is called 'Comp' in 'myapp' app.

    CREO_COMPONENT_MODEL = 'myapp.models.Comp'


    settings.AUTH_USER_MODEL also linked to for record keeping


    add 'creo' to installed apps

    ensure you have a base template named 'base.html'
