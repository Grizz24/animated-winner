from django import forms

from .models import Show


class ShowForm(forms.ModelForm):
    """Full form used by the Add Show page."""

    class Meta:
        model = Show
        fields = ["name", "media_type", "seasons", "episodes", "genre", "status"]

    def clean(self):
        cleaned = super().clean()
        if cleaned.get("media_type") == Show.MediaType.SERIES:
            if not cleaned.get("seasons"):
                self.add_error("seasons", "Series need a number of seasons.")
            if not cleaned.get("episodes"):
                self.add_error("episodes", "Series need a number of episodes.")
        else:
            # Movies don't have seasons or episodes.
            cleaned["seasons"] = None
            cleaned["episodes"] = None
        return cleaned


class QuickAddForm(forms.ModelForm):
    """Small form on the home page: just a name and a status."""

    class Meta:
        model = Show
        fields = ["name", "status"]
