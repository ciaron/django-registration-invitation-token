django-registration-invitation-token
====================================

A django-registration backend for accepting new registrations only with a valid invitation code

Installation
------------

Copy this subdirectory (or symlink it) to your registration/backends directory, and call it "token".

You should already have "registration" in your INSTALLED_APPS, and you will need to add "registration.backends.token".

In urls.py, make sure you have:
> url(r'^accounts/', include('registration.backends.token.urls')) 

instead of the standard "backends.simple" or "backends.default"

Run "python manage.py syncdb".

Add some tokens to the database.


