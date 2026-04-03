"""Forms used by the Topiq website app."""

from django import forms


class SearchForm(forms.Form):
    """Simple search form for topic queries and optional semester filtering."""

    q = forms.CharField(
        min_length=2,
        max_length=200,
        widget=forms.TextInput(
            attrs={
                "placeholder": "Search your study topic… e.g. Deadlock, Binary Tree",
                "class": "search-input",
                "autocomplete": "off",
            }
        ),
    )
    semester = forms.ModelChoiceField(
        queryset=None,
        required=False,
        empty_label="All Semesters",
    )

    def __init__(self, *args, **kwargs):
        """Populate the semester field with active semester choices."""
        super().__init__(*args, **kwargs)
        from website.models import Semester

        self.fields["semester"].queryset = Semester.objects.filter(is_active=True).order_by("order")
