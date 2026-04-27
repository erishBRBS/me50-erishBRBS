from django import forms
from .models import Comment, Listing


class ListingForm(forms.ModelForm):
    class Meta:
        model = Listing
        fields = ["title", "description", "starting_bid", "image_url", "category"]
        labels = {
            "image_url": "Image URL",
            "starting_bid": "Starting bid",
        }
        widgets = {
            "title": forms.TextInput(attrs={"class": "form-control", "placeholder": "Listing title"}),
            "description": forms.Textarea(attrs={"class": "form-control", "rows": 4, "placeholder": "Describe your item"}),
            "starting_bid": forms.NumberInput(attrs={"class": "form-control", "step": "0.01", "min": "0.01"}),
            "image_url": forms.URLInput(attrs={"class": "form-control", "placeholder": "https://example.com/image.jpg"}),
            "category": forms.Select(attrs={"class": "form-control"}),
        }


class BidForm(forms.Form):
    amount = forms.DecimalField(
        max_digits=10,
        decimal_places=2,
        min_value=0.01,
        widget=forms.NumberInput(attrs={
            "class": "form-control",
            "step": "0.01",
            "min": "0.01",
            "placeholder": "Enter your bid"
        })
    )


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ["content"]
        labels = {"content": "Comment"}
        widgets = {
            "content": forms.Textarea(attrs={
                "class": "form-control",
                "rows": 3,
                "placeholder": "Write a comment..."
            })
        }
