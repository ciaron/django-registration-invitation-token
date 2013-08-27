django-registration-invitation-token
====================================

A django-registration backend for accepting new registrations only with a valid invitation code

Installation
------------

1. Copy this subdirectory (or symlink it) to your registration/backends directory, and call it "token".

2. You should already have "registration" in your INSTALLED_APPS, and you will need to add "registration.backends.token".

3. In urls.py, make sure you have:
> url(r'^accounts/', include('registration.backends.token.urls')) 

instead of the standard "backends.simple" or "backends.default"

4. Run "python manage.py syncdb".

5. Add some tokens to the database.


