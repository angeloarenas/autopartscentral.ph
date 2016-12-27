from django import forms
import account.forms
import models


class SignupForm(account.forms.SignupForm):

    # TODO: If needed put validation/clean methods here

    first_name = forms.CharField(
        label="First Name",
        max_length=30,
        widget=forms.TextInput(),
        required=True
    )

    middle_name = forms.CharField(
        label="Middle Name",
        max_length=30,
        widget=forms.TextInput(),
        required=False
    )

    last_name = forms.CharField(
        label="Last Name",
        max_length=30,
        widget=forms.TextInput(),
        required=True
    )

    contact_no = forms.CharField(
        label="Contact Number",
        max_length=30,
        widget=forms.TextInput(),
        required=True
    )

    address_line_1 = forms.CharField(
        label="Line 1",
        max_length=40,
        widget=forms.TextInput(),
        required=True
    )

    address_line_2 = forms.CharField(
        label="Line 2",
        max_length=40,
        widget=forms.TextInput(),
        required=False
    )

    address_city = forms.CharField(
        label="City",
        max_length=30,
        widget=forms.TextInput(),
        required=True
    )

    address_province = forms.CharField(
        label="Province",
        max_length=30,
        widget=forms.TextInput(),
        required=True
    )

    address_country = forms.ChoiceField(
        label="Country",
        choices=models.COUNTRY_CHOICES,
        widget=forms.Select(),
        required=True
    )
