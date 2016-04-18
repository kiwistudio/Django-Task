from django import forms
from django.core.urlresolvers import reverse

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from crispy_forms.bootstrap import FormActions

from .models import UserProfile


class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['birthday']

    def __init__(self, *args, **kwargs):
	    super(UserUpdateForm, self).__init__(*args, **kwargs)

	    self.helper = FormHelper(self)

	        # set form tag attributes
	    self.helper.form_action = reverse('user_edit', kwargs={'pk': kwargs['instance'].id})
	    self.helper.form_method = 'POST'
	    self.helper.form_class = 'form-horizontal'

	        # set form field properties
	    self.helper.help_text_inline = True
	    self.helper.html5_required = True
	    self.helper.label_class = 'col-sm-2 control-label'
	    self.helper.field_class = 'col-sm-10'

	        # add buttons
	    self.helper.layout[-1] = FormActions(
	        Submit('add_button', 'Save', css_class="btn btn-primary"),
	        Submit('cancel_button', 'Cancel', css_class="btn btn-link"),
	    )   

