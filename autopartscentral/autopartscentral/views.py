from django.views.generic import TemplateView, FormView, CreateView, UpdateView
from django.http import JsonResponse, HttpResponse, HttpResponseRedirect
from django.utils.encoding import smart_unicode
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.db.models import Max, Min
from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404
import json
import models
import forms
import account.views
import account.forms
from carton.cart import Cart
from decimal import Decimal, ROUND_UP


def compute_subtotal_vat(total):
    subtotal = total / Decimal('1.12')
    subtotal = subtotal.quantize(Decimal('.01'), rounding=ROUND_UP)
    vat = total - subtotal
    return {'subtotal': subtotal, 'vat': vat}


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
            user=self.created_user,
            first_name=form.cleaned_data['first_name'],
            last_name=form.cleaned_data['last_name'],
            contact_no=form.cleaned_data['contact_no'],
            line_1=form.cleaned_data['address_line_1'],
            line_2=form.cleaned_data['address_line_2'],
            city=form.cleaned_data['address_city'],
            province=form.cleaned_data['address_province'],
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


@method_decorator(login_required, name='dispatch')
class AccountDashboardView(TemplateView):
    template_name = "account-dashboard.html"

    def pending_orders(self):
        return models.Order.objects.filter(customer=self.request.user.id).exclude(status__in=['RE', 'CA']).order_by('-placed_timestamp')


# TODO Add change email with email verification
@method_decorator(login_required, name='dispatch')
class AccountProfileView(FormView):
    template_name = "account-profile.html"
    form_class = forms.ProfileForm
    success_url = reverse_lazy('account_profile')

    def form_valid(self, form):
        user = models.User.objects.get(id=self.request.user.id)
        user.username = form.cleaned_data['username']
        user.save()

        user.userprofile.first_name = form.cleaned_data['first_name']
        user.userprofile.middle_name = form.cleaned_data['middle_name']
        user.userprofile.last_name = form.cleaned_data['last_name']
        user.userprofile.contact_no = form.cleaned_data['contact_no']
        user.userprofile.save()
        return super(AccountProfileView, self).form_valid(form)

    def get_form_kwargs(self):
        kwargs = super(AccountProfileView, self).get_form_kwargs()
        kwargs.update({'initial': {'email': self.request.user.email,
                                   'username': self.request.user.username,
                                   'first_name': self.request.user.userprofile.first_name,
                                   'middle_name': self.request.user.userprofile.middle_name,
                                   'last_name': self.request.user.userprofile.last_name,
                                   'contact_no': self.request.user.userprofile.contact_no}})
        return kwargs


@method_decorator(login_required, name='dispatch')
class AccountAddressesView(TemplateView):
    template_name = "account-address.html"

    def addresses(self):
        return models.Address.objects.filter(user=self.request.user)


@method_decorator(login_required, name='dispatch')
class AccountAddressesAddView(CreateView):
    template_name = "address_add.html"
    form_class = forms.AddressForm
    success_url = reverse_lazy('account_addresses')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(AccountAddressesAddView, self).form_valid(form)


@method_decorator(login_required, name='dispatch')
class AccountAddressesUpdateView(UpdateView):
    template_name = "address_add.html"
    form_class = forms.AddressForm
    success_url = reverse_lazy('account_addresses')

    def dispatch(self, request, *args, **kwargs):
        if self.get_object().user != self.request.user:
            return HttpResponseRedirect(reverse_lazy('account_addresses'))
        return super(AccountAddressesUpdateView, self).dispatch(request, *args, **kwargs)

    def get_object(self, queryset=None):
        return get_object_or_404(models.Address, id=self.kwargs['id'])


@method_decorator(login_required, name='dispatch')
class AccountOrdersView(TemplateView):
    template_name = "account-all-orders.html"

    def orders(self):
        return models.Order.objects.filter(customer=self.request.user).order_by('-placed_timestamp')


@method_decorator(login_required, name='dispatch')
class AccountOrdersDetailView(TemplateView):
    template_name = "account-single-order.html"

    def dispatch(self, request, *args, **kwargs):
        if self.order().customer != self.request.user:
            return HttpResponseRedirect(reverse_lazy('account_orders'))
        return super(AccountOrdersDetailView, self).dispatch(request, *args, **kwargs)

    def order(self):
        return get_object_or_404(models.Order, id=self.kwargs['id'])

    def subtotal_vat(self):
        return compute_subtotal_vat(self.order().net_price)


# TODO if manual input model id not in make
# TODO Error404 or something for wrong category and make/model/year combination
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
        vehicle_make = self.request.GET.get('make')
        vehicle_model = self.request.GET.get('model')
        vehicle_year = self.request.GET.get('year')

        objects = models.Part.objects.all()
        if vehicle_make:
            objects = objects.filter(compatibility__model__make__id=vehicle_make).distinct()
        if vehicle_model:
            objects = objects.filter(compatibility__model__id=vehicle_model).distinct()
        #if vehicle_year:
            #objects = objects.filter(compatibility__model__id=vehicle_model).distinct()

        if category3:
            objects = objects.filter(category_l3__slug=category3).distinct()
        elif category2:
            objects = objects.filter(category_l2__slug=category2).distinct()
        elif category1:
            objects = objects.filter(category_l1__slug=category1).distinct()

        return objects


class ShopDetailView(TemplateView):
    template_name = "single-product.html"

    def part(self):
        return get_object_or_404(models.Part, slug=self.kwargs['slug'])


# TODO Show shopping cart is empty
class CartView(TemplateView):
    template_name = "cart-page.html"

    def subtotal_vat(self):
        return compute_subtotal_vat(Cart(self.request.session).total)


class CheckoutLoginView(account.views.LoginView):
    template_name = "checkout-step-1.html"
    form_class = account.forms.LoginEmailForm

    # Auto redirect back to cart if cart is empty
    def dispatch(self, request, *args, **kwargs):
        if Cart(request.session).is_empty:
            return HttpResponseRedirect(reverse_lazy('cart'))
        return super(CheckoutLoginView, self).dispatch(request, *args, **kwargs)

    # Auto redirect to next checkout step after logging in
    def get_context_data(self, **kwargs):
        ctx = super(CheckoutLoginView, self).get_context_data(**kwargs)
        ctx.update({"redirect_field_value": reverse_lazy('checkout_shipping')})
        return ctx

    # Auto redirect to next checkout step if already logged in
    def get_success_url(self, fallback_url=None, **kwargs):
        return super(CheckoutLoginView, self).get_success_url(reverse_lazy('checkout_shipping'), **kwargs)


# TODO Use SessionWizard if more steps will be added or implement one page like partspro - use javascript
@method_decorator(lambda x: login_required(x, login_url=reverse_lazy('checkout_login')), name='dispatch')
class CheckoutShippingView(FormView):
    template_name = "checkout-step-2.html"
    form_class = forms.CheckoutShippingForm
    success_url = reverse_lazy('checkout_review')

    # Auto redirect back to cart if cart is empty
    def dispatch(self, request, *args, **kwargs):
        if Cart(request.session).is_empty:
            return HttpResponseRedirect(reverse_lazy('cart'))
        return super(CheckoutShippingView, self).dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        self.request.session['checkout_shipping_address_id'] = form.cleaned_data['shipping_address'].id
        return super(CheckoutShippingView, self).form_valid(form)

    def get_form_kwargs(self):
        kwargs = super(CheckoutShippingView, self).get_form_kwargs()
        kwargs.update({'user': self.request.user.id})
        # kwargs.update({'initial': {'shipping_address': self.request.user.userprofile.default_shipping_address}})
        return kwargs


@method_decorator(lambda x: login_required(x, login_url=reverse_lazy('checkout_login')), name='dispatch')
class CheckoutReviewView(FormView):
    template_name = "checkout-step-4.html"
    form_class = forms.CheckoutReviewForm
    success_url = reverse_lazy('checkout_complete')

    # Auto redirect back to cart if cart is empty or to shipping if no shipping
    def dispatch(self, request, *args, **kwargs):
        if Cart(request.session).is_empty:
            return HttpResponseRedirect(reverse_lazy('cart'))
        if 'checkout_shipping_address_id' not in request.session:
            return HttpResponseRedirect(reverse_lazy('checkout_shipping'))
        return super(CheckoutReviewView, self).dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        cart = Cart(self.request.session)
        shipping_address = models.Address.objects.get(id=self.request.session['checkout_shipping_address_id'])

        order = models.Order.objects.create(
            customer=self.request.user,
            shipping_address_first_name=shipping_address.first_name,
            shipping_address_last_name=shipping_address.last_name,
            shipping_address_contact_no=shipping_address.contact_no,
            shipping_address_line_1=shipping_address.line_1,
            shipping_address_line_2=shipping_address.line_2,
            shipping_address_city=shipping_address.city,
            shipping_address_province=shipping_address.province,
            shipping_address_country=shipping_address.country,
            net_price=cart.total
        )
        for item in cart.items:
            models.OrderDetails.objects.create(
                order=order,
                part=item.product,
                part_name=item.product.name,
                part_number=item.product.part_number,
                unit_price=item.price,
                quantity=item.quantity,
                net_price=item.subtotal
            )
        self.request.session['checkout_order_id'] = order.id
        # TODO Send email

        # TODO Confirmation if order was placed (error if e.g. cart is empty, other errors)

        return super(CheckoutReviewView, self).form_valid(form)

    def shipping_address(self):
        return models.Address.objects.get(id=self.request.session['checkout_shipping_address_id'])

    def subtotal_vat(self):
        return compute_subtotal_vat(Cart(self.request.session).total)


@method_decorator(lambda x: login_required(x, login_url=reverse_lazy('checkout_login')), name='dispatch')
class CheckoutCompleteView(TemplateView):
    template_name = "checkout-complete.html"

    checkout_order_id = 0
    checkout_shipping_address_id = 0
    checkout_cart_total = 0

    # Auto redirect back to shop if no order id
    # TODO Redirect profile orders
    def dispatch(self, request, *args, **kwargs):
        if 'checkout_order_id' not in request.session:
            return HttpResponseRedirect(reverse_lazy('shop'))
        else:
            self.checkout_order_id = self.request.session['checkout_order_id']
            self.checkout_shipping_address_id = request.session['checkout_shipping_address_id']
            self.checkout_cart_total = Cart(self.request.session).total
            del self.request.session['checkout_order_id']
            del self.request.session['checkout_shipping_address_id']
            Cart(self.request.session).clear()
        return super(CheckoutCompleteView, self).dispatch(request, *args, **kwargs)

    def order_details(self):
        return {'checkout_order_id': self.checkout_order_id,
                'checkout_shipping_address': models.Address.objects.get(id=self.checkout_shipping_address_id),
                'checkout_cart_total': self.checkout_cart_total}


# TODO JsonResponse shouldn't be safe=False, find a better way to send JSON data
# TODO vehicle_max_year can be changed to current year
def vehicle_filter(request):
    if request.is_ajax() and request.GET:
        if 'vehicle_make' in request.GET:
            vehicle_models = models.VehicleModel.objects.filter(make=request.GET['vehicle_make'])
            return JsonResponse([{'id': i.id, 'name': smart_unicode(i)} for i in vehicle_models], safe=False)
        if 'vehicle_model' in request.GET:
            vehicle_min_year = models.Vehicle.objects.filter(
                model=request.GET['vehicle_model']).aggregate(Min('year_start'))['year_start__min']
            vehicle_max_year = models.Vehicle.objects.filter(
                model=request.GET['vehicle_model']).aggregate(Max('year_end'))['year_end__max']
            return JsonResponse([{'id': i, 'name': j}
                                 for i, j in enumerate(range(vehicle_min_year, vehicle_max_year+1))], safe=False)
    else:
        return JsonResponse({'error': 'Not Ajax or no GET'})


# TODO Check first if part is available
# TODO Quantity
def cart_add(request):
    if request.is_ajax() and request.POST and 'part' in request.POST:
        cart = Cart(request.session)
        product = models.Part.objects.get(slug=request.POST.get('part'))
        cart.add(product, price=product.price)
        return HttpResponse(content=product.name + " successfully added to cart")
    else:
        return HttpResponse(status=400, content="Error adding to cart")


# TODO Check if in cart
def cart_remove(request):
    if request.is_ajax() and request.POST and 'part' in request.POST:
        cart = Cart(request.session)
        product = models.Part.objects.get(slug=request.POST.get('part'))
        cart.remove(product)
        return HttpResponse(content=product.name + " successfully removed from cart")
    else:
        return HttpResponse(status=400, content="Error removing from cart")


# TODO Check if in cart
def cart_update(request):
    if request.is_ajax() and request.POST and 'data' in request.POST:
        cart = Cart(request.session)
        json_data = json.loads(request.POST.get('data'))
        for i in json_data:
            product = models.Part.objects.get(slug=i['part'])
            cart.set_quantity(product, quantity=i['quantity'])
        return HttpResponse("Successfully updated cart")
    else:
        return HttpResponse(status=400, content="Error updating cart")


def address_delete(request):
    if request.is_ajax and request.POST and 'address' in request.POST:
        address = models.Address.objects.get(id=request.POST.get('address'))
        if address.user.id == request.user.id and address.id != request.user.userprofile.default_shipping_address.id:
            address.delete()
        return HttpResponse("Successfully deleted address")
    else:
        return HttpResponse(status=400, content="Error deleting address")


def address_setdefault(request):
    if request.is_ajax and request.POST and 'address' in request.POST:
        address = models.Address.objects.get(id=request.POST.get('address'))
        if address.user.id == request.user.id and address.id != request.user.userprofile.default_shipping_address.id:
            request.user.userprofile.default_shipping_address = address
            request.user.userprofile.save()
        return HttpResponse("Successfully set address default")
    else:
        return HttpResponse(status=400, content="Error setting address default")
