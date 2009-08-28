from django import forms
from django.conf import settings
from sugar.widgets.admin_image.widget import AdminImageWidget

class AdminImageForm(forms.ModelForm):
    '''
    Basic form to handle wiring up the AdminImageWidget to your
    model that has a 'file' field. This assumes your models
    has a file field. If it doesn't then don't use this form
    but create your own.
    
    '''
    
    file = forms.FileField(widget=AdminImageWidget, required=True)