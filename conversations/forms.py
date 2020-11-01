from django import forms

class AddCommentForm(forms.Form):

    message = forms.CharField(required=True, widget=forms.TextInput(attrs={"placeholder": "Type your message", "padding":"5px"}))