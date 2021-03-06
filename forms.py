"""
Forms and validation code for user registration.

Note that all of these forms assume Django's bundle default ``User``
model; since it's not possible for a form to anticipate in advance the
needs of custom user models, you will need to write your own forms if
you're using a custom model.

"""


from django.contrib.auth.models import User
from django import forms
from django.utils.translation import ugettext_lazy as _

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Fieldset, Reset
from crispy_forms.bootstrap import FormActions, AppendedText

from registration.backends.token.models import InvitationCode

class TokenRegistrationForm(forms.Form):
    """
    Form for registering a new user account with a invitation token
    
    Validates that the requested username is not already in use, and
    requires the password to be entered twice to catch typos.

    Validates that a correct invitation code (token) has been supplied.
    
    Subclasses should feel free to add any additional validation they
    need, but should avoid defining a ``save()`` method -- the actual
    saving of collected user data is delegated to the active
    registration backend.

    """
    required_css_class = 'required'
    
    #username = forms.RegexField(regex=r'^[\w.@+-]+$',
    username = forms.RegexField(regex=r'^[\w+-]+$',
                                max_length=30,
                                label=_("Username"),
                                error_messages={'invalid': _("The username may contain only letters, numbers and + - _ characters.")})
    #firstname = forms.CharField(label=_("First name"))
    #lastname = forms.CharField(label=_("Last name"))
    email = forms.EmailField(label=_("E-mail"))
    password1 = forms.CharField(widget=forms.PasswordInput,
                                label=_("Password"))
    #password2 = forms.CharField(widget=forms.PasswordInput,
    #                            label=_("Password (again)"))
    token = forms.CharField(label=_("Invitation code"))

    def __init__(self, *args, **kwargs):
        self.helper = FormHelper()

        self.helper.layout = Layout(
            Fieldset(
                'create an account',
                'username',
                'email',
                'password1',
                #'password2',
                'token',
            ),
            FormActions(
                Submit('submit', 'Submit', css_class="btn-primary"),
            )
        )
        super(TokenRegistrationForm, self).__init__(*args, **kwargs)
    
    def clean_username(self):
        """
        Validate that the username is alphanumeric and is not already
        in use.
        
        """
        existing = User.objects.filter(username__iexact=self.cleaned_data['username'])
        if existing.exists():
            raise forms.ValidationError(_("A user with that username already exists."))
        else:
            return self.cleaned_data['username']

    def clean(self):
        """
        Verify that the values entered into the two password fields
        match. Note that an error here will end up in
        ``non_field_errors()`` because it doesn't apply to a single
        field.
        
        """
        #if 'password1' in self.cleaned_data and 'password2' in self.cleaned_data:
        #   if self.cleaned_data['password1'] != self.cleaned_data['password2']:
        #       raise forms.ValidationError(_("The two password fields didn't match."))
	
        if 'token' in self.cleaned_data:
            try:
                tk = InvitationCode.objects.get(code=self.cleaned_data['token'])
            except:
                tk = False

            if not tk:
                raise forms.ValidationError(_("The invitation code you entered is invalid"))
            else:
                if tk.is_used:
                    raise forms.ValidationError(_("The invitation code you entered has already been used, sorry!"))

        return self.cleaned_data

class RegistrationFormTermsOfService(TokenRegistrationForm):
    """
    Subclass of ``RegistrationForm`` which adds a required checkbox
    for agreeing to a site's Terms of Service.
    
    """
    tos = forms.BooleanField(widget=forms.CheckboxInput,
                             label=_(u'I have read and agree to the Terms of Service'),
                             error_messages={'required': _("You must agree to the terms to register")})


class RegistrationFormUniqueEmail(TokenRegistrationForm):
    """
    Subclass of ``RegistrationForm`` which enforces uniqueness of
    email addresses.
    
    """
    def clean_email(self):
        """
        Validate that the supplied email address is unique for the
        site.
        
        """
        if User.objects.filter(email__iexact=self.cleaned_data['email']):
            raise forms.ValidationError(_("This email address is already in use. Please supply a different email address."))
        return self.cleaned_data['email']


class RegistrationFormNoFreeEmail(TokenRegistrationForm):
    """
    Subclass of ``RegistrationForm`` which disallows registration with
    email addresses from popular free webmail services; moderately
    useful for preventing automated spam registrations.
    
    To change the list of banned domains, subclass this form and
    override the attribute ``bad_domains``.
    
    """
    bad_domains = ['aim.com', 'aol.com', 'email.com', 'gmail.com',
                   'googlemail.com', 'hotmail.com', 'hushmail.com',
                   'msn.com', 'mail.ru', 'mailinator.com', 'live.com',
                   'yahoo.com']
    
    def clean_email(self):
        """
        Check the supplied email address against a list of known free
        webmail domains.
        
        """
        email_domain = self.cleaned_data['email'].split('@')[1]
        if email_domain in self.bad_domains:
            raise forms.ValidationError(_("Registration using free email addresses is prohibited. Please supply a different email address."))
        return self.cleaned_data['email']
