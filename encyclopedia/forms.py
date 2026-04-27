from django import forms


class NewEntryForm(forms.Form):
    title = forms.CharField(
        label='Title',
        widget=forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Enter page title'})
    )
    content = forms.CharField(
        label='Markdown Content',
        widget=forms.Textarea(attrs={'class': 'form-textarea', 'rows': 18, 'placeholder': 'Write Markdown here...'})
    )


class EditEntryForm(forms.Form):
    content = forms.CharField(
        label='Markdown Content',
        widget=forms.Textarea(attrs={'class': 'form-textarea', 'rows': 18})
    )
