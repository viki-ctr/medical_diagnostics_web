from django import forms

from .models import Feedback


class FeedbackForm(forms.ModelForm):
    class Meta:
        model = Feedback
        fields = ["name", "email", "phone", "subject", "message"]
        widgets = {
            "message": forms.Textarea(attrs={"rows": 4}),
        }
