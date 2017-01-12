from django import forms
import account.forms
import models


# TODO: If needed put validation/clean methods here
class SignupForm(account.forms.SignupForm):
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


class CheckoutShippingForm(forms.Form):
    shipping_address = forms.ModelChoiceField(
        label="Shipping Address",
        queryset=models.Address.objects.none(),
        widget=forms.RadioSelect,
        required=True,
        empty_label=None,
    )

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', -1)
        super(CheckoutShippingForm, self).__init__(*args, **kwargs)
        self.fields['shipping_address'].queryset = models.Address.objects.filter(user=user)


class CheckoutReviewForm(forms.Form):
    filler_field = forms.CharField(
        label="Filler Field",
        widget=forms.HiddenInput,
        required=False,
    )


class ProfileForm(account.forms.SignupForm):
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

    def __init__(self, *args, **kwargs):
        super(ProfileForm, self).__init__(*args, **kwargs)
        del self.fields["email"]
        del self.fields["password"]
        del self.fields["password_confirm"]
        del self.fields["code"]

    def clean_username(self):
        if 'username' in self.changed_data:
            return super(ProfileForm, self).clean_username()
        else:
            return self.cleaned_data["username"]

    # def clean_email(self):
        # if 'email' in self.changed_data:
            # return super(ProfileForm, self).clean_email()
        # else:
            # return self.cleaned_data["email"]
