from django import forms

from .models import CommunityApplication


class CommunityApplicationForm(forms.ModelForm):
    class Meta:
        model = CommunityApplication
        fields = (
            "plan", "business_name", "contact_name", "email", "phone", "website",
            "location", "category", "team_size", "message", "accepts_updates",
        )
        widgets = {
            "plan": forms.RadioSelect,
            "business_name": forms.TextInput(attrs={"placeholder": "Your business name"}),
            "contact_name": forms.TextInput(attrs={"placeholder": "Your name"}),
            "email": forms.EmailInput(attrs={"placeholder": "you@business.com"}),
            "phone": forms.TextInput(attrs={"placeholder": "+34 ..."}),
            "website": forms.URLInput(attrs={"placeholder": "https://"}),
            "location": forms.TextInput(attrs={"placeholder": "Town or island-wide"}),
            "category": forms.TextInput(attrs={"placeholder": "e.g. Wellness, trades, hospitality"}),
            "team_size": forms.TextInput(attrs={"placeholder": "e.g. Just me, 2–5, 6+"}),
            "message": forms.Textarea(attrs={"rows": 5, "placeholder": "What do you do, and what would you bring to the community?"}),
        }
