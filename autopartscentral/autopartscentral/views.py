from django.views.generic import TemplateView
import models
import forms
import account.views
import account.forms


class IndexView(TemplateView):
    template_name = "index.html"

    def part_featured(self):
        products = models.Part.objects.all()
        return products


class LoginView(account.views.LoginView):
    template_name = "login.html"
    form_class = account.forms.LoginEmailForm


class SignupView(account.views.SignupView):
    template_name = "signup.html"
    form_class = forms.SignupForm

    def generate_username(self, form):
        pass

    def after_signup(self, form):
        super(SignupView, self).after_signup(form)
        self.create_userprofile(form)

    # TODO Better make sure this is in sync with the form, any error would result to user without UserProfile, etc.
    def create_userprofile(self, form):
        default_shipping_address = models.Address.objects.create(
            line_1=form.cleaned_data['address_line_1'],
            line_2=form.cleaned_data['address_line_2'],
            city=form.cleaned_data['address_city'],
            state=form.cleaned_data['address_state'],
            country=form.cleaned_data['address_country'],
        )
        models.UserProfile.objects.create(
            user=self.created_user,
            first_name=form.cleaned_data['first_name'],
            middle_name=form.cleaned_data['middle_name'],
            last_name=form.cleaned_data['last_name'],
            contact_no=form.cleaned_data['contact_no'],
            default_shipping_address=default_shipping_address
        )

    """
    def form_valid(self, form):
        self.created_user = self.create_user(form, commit=False)  # TODO: Called twice, here and in super, improve
        self.created_address = models.Address(
            line_1=form.cleaned_data['address_line_1'],
            line_2=form.cleaned_data['address_line_2'],
            city=form.cleaned_data['address_city'],
            state=form.cleaned_data['address_state'],
            country=form.cleaned_data['address_country'],
        )
        self.created_userprofile = models.UserProfile(
            user=self.created_user,
            first_name=form.cleaned_data['first_name'],
            middle_name=form.cleaned_data['middle_name'],
            last_name=form.cleaned_data['last_name'],
            contact_no=form.cleaned_data['contact_no'],
            default_shipping_address=self.created_address
        )

        try:
            self.created_address.full_clean()
            self.created_userprofile.full_clean()  # Check if created_userprofile is valid
        except ValidationError as e:
            print "Validation Error in SignupView"
            print e.messages
            return super(SignupView, self).form_invalid(form)  # TODO: Create own form_invalid
            # self.non_field_errors = e.message_dict[NON_FIELD_ERRORS]
        else:
            super(SignupView, self).form_valid(form)  # Calls created_user.save()
            self.created_address.save()
            self.created_userprofile.save()
    """


class ShopView(TemplateView):
    template_name = "product-grid-left-sidebar.html"

    def categories_l1(self):
        return models.CategoryL1.objects.all()

    def vehicle_makes(self):
        return models.VehicleMake.objects.all()

    def parts(self):
        category1 = self.request.GET.get('category1')
        category2 = self.request.GET.get('category2')
        category3 = self.request.GET.get('category3')

        if category3:
            return models.Part.objects.filter(category_l3__name=category3)
        elif category2:
            return models.Part.objects.filter(category_l2__name=category2)
        elif category1:
            return models.Part.objects.filter(category_l1__name=category1)
        else:
            return models.Part.objects.all()
