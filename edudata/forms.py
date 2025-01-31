from django import forms
from .models import SchoolLocation
from .location_data import PROVINCES, DISTRICTS, SECTORS, CELLS, VILLAGES


class SchoolLocationForm(forms.ModelForm):
    class Meta:
        model = SchoolLocation
        fields = "__all__"
        widgets = {
            "province": forms.Select(choices=[("", "---------")] + list(PROVINCES)),
            "district": forms.Select(),
            "sector": forms.Select(),
            "cell": forms.Select(),
            "village": forms.Select(),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Populate province choices
        self.fields["province"].widget.choices = [("", "---------")] + list(PROVINCES)

        # Get initial values
        province = (
            self.data.get("province") or self.instance.province
            if self.instance
            else None
        )
        district = (
            self.data.get("district") or self.instance.district
            if self.instance
            else None
        )
        sector = (
            self.data.get("sector") or self.instance.sector if self.instance else None
        )
        cell = self.data.get("cell") or self.instance.cell if self.instance else None

        # Set choices dynamically
        self.fields["district"].widget.choices = (
            [("", "---------")] + DISTRICTS.get(province, [])
            if province
            else [("", "---------")]
        )
        self.fields["sector"].widget.choices = (
            [("", "---------")] + SECTORS.get(district, [])
            if district
            else [("", "---------")]
        )
        self.fields["cell"].widget.choices = (
            [("", "---------")] + CELLS.get(sector, [])
            if sector
            else [("", "---------")]
        )
        self.fields["village"].widget.choices = (
            [("", "---------")] + VILLAGES.get(cell, [])
            if cell
            else [("", "---------")]
        )
