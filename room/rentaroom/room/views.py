from django.contrib.auth.models import User
from django.forms.models import inlineformset_factory
from django.forms.models import modelform_factory
from django.views.generic import ListView, CreateView, DetailView
from .models import Address, CheckList, RoomForRent, RentalContract, RentalPayment, Profile
from .forms import AddressFormSet, CheckListFormSet, RoomForRentForm, RentalContractForm, RentalPaymentForm

from django.contrib.messages import info, error
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponseRedirect,  HttpResponse

class RoomForRentView(object):
    
    """
    List and detail view mixin for rooms for rent - just defines the correct
    queryset.
    """
    
    def get_queryset(self):
        return RoomForRent.objects.published()
    

class RoomForRentList(RoomForRentView, ListView):
    """
    list by publish date
    """
    
    date_field = "publish_date"
    
    def get_title(self, context):
        if context["profile_user"]:
            return "Rooms by %s" % context["profile_user"].profile
        else:
            return "Newest"

class ExtraContextMixin(object):
    
    """
    show two or more model in one view
    """
    
    extra = {}

    def get_context_data(self, **kwargs):
        context = super(ExtraContextMixin, self).get_context_data(**kwargs)
        context.update(self.extra())
        return context
       
class RoomForRentDetail(ExtraContextMixin, DetailView):
    model = RoomForRent
    
    def extra(self):
        extra=Address.objects.all
        return dict(extra=extra)


    
class RoomForRentCreate(CreateView):

    form_class = RoomForRentForm
    model = RoomForRent
    success_url = 'success/'
    
    def get(self, request, *args, **kwargs):
        
        """Handles GET requests and instantiates blank versions of the form
        and its inline formsets.
        """
        self.object = None
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        address_form = AddressFormSet()
        checklist_form = CheckListFormSet()
        return self.render_to_response(self.get_context_data(form=form, address_form=address_form, checklist_form=checklist_form))
    
    def post(self, request, *args, **kwargs):
        """
        Handles POST requests, instantiating a form instance and its inline
        formsets with the passed POST variables and then checking them for
        validity.
        """
        self.object = None
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        address_form = AddressFormSet(self.request.POST)
        checklist_form = CheckListFormSet(self.request.POST)
        if (form.is_valid() and address_form.is_valid() and checklist_form.is_valid()):
            return self.form_valid(form, address_form, checklist_form)   
        else:
            return self.form_invalid(form, address_form, checklist_form)
    
    def form_valid(self, form, address_form, checklist_form):
        
        form.instance.user = self.request.user
        form.instance.gen_description = False
        self.object = form.save()
        address_form.instance = self.object
        address_form.save()
        checklist_form.instance = self.object
        checklist_form.save()
        return HttpResponseRedirect(self.get_success_url())
    
    def form_invalid(self, form, address_form, checklist_form):
        """
        Called if a form is invalid. Re-renders the context data with the
        data-filled forms and errors.
        """
        return self.render_to_response(
            self.get_context_data(form=form,
                                  address_form=address_form,
                                  checklist_form=checklist_form))
        

class RentalContractDetail(DetailView):
    
    model = RentalContract
    
class RentalContractView(object):
    
    """
    List and detail view mixin for rooms for rent - just defines the correct
    queryset.
    """
    
    def get_queryset(self):
        return RentalContract.objects.published()
    
class RentalContractList(RentalContractView, ListView):
    
    date_field = "publish_date"
    
    def get_title(self, context):
        if context["profile_user"]:
            return "Rentalcontracts by %s" % context["profile_user"].profile
        else:
            return "Newest"      
            
class RentalContractCreate(CreateView):
   
    form_class = RentalContractForm
    model = RentalContract
    
    def get_initial(self, request):
        
        # Get the initial dictionary from the superclass method
        initial = super(YourView, self).get_initial()
        # Copy the dictionary so we don't accidentally change a mutable dict
        initial = initial.copy()
        slug = request.GET.get('slug', '')
        room_for_rent = get_object_or_404(RoomForRent, slug=slug)
        check_list = CheckList.objetcts.get(RoomForRent_exact=pk)
        initial['room_for_rent'] = room_for_rent.pk
        initial['room_owner'] = room_for_rent.room_owner
        initial['rental_fee'] = room_for_rent.rental_fee
        if check_list.internet_fee_status = 'INCLUDED':
            initial['internet_fee'] = '0'
        else:
            initial['internet_fee'] = room_for_rent.internet_fee
        if check_list.hub_fee_status = 'INCLUDED':
            initial['hub_fee'] = '0'
        else:
            initial['hub_fee'] = room_for_rent.hub_fee

        return initial
        
    def form_valid(self, form):
        form.instance.room_owner = self.request.user
        info(self.request, "Rental Contract created")
        return super(RentalContractCreate, self).form_valid(form)

class RentalPaymentDetail(DetailView):
    model = RentalPayment     
    
class RentalPaymentCreate(CreateView):
    
    form_class = RentalPaymentForm
    model = RentalPayment
    
    def get_initial(self, request):
        
        # Get the initial dictionary from the superclass method
        initial = super(YourView, self).get_initial()
        # Copy the dictionary so we don't accidentally change a mutable dict
        initial = initial.copy()
        slug = request.GET.get('slug', '')
        rental_contract = get_object_or_404(RentalContract, slug=slug)
        initial['rental_contract'] = rental_contract.pk
        initial['rental_fee'] = rental_contract.rental_fee
        initial['internet_fee'] = rental_contract.internet_fee
        initial['hub_fee'] = rental_contract.hub_fee
        return initial
        
 
class RentalPaymentDetail(DetailView):
    model = RentalPayment
 
@login_required   
def confirmed(request, pk):
    rental_contract = get_object_or_404(RentalContract, pk=pk)
    if rental_contract.room_renter != request.user:
        return HttpResponse("You dont have right to do it")
    rental_contract.contract_status = 'CONFIRMED'
    rental_contract.save()
    return redirect('rental_contract_detail')

@login_required   
def declined(request, pk):
    rental_contract = get_object_or_404(RentalContract, pk=pk)
    if rental_contract.room_renter != request.user:
        return HttpResponse("You dont have right to do it")
    rental_contract.contract_status = 'DECLINED'
    rental_contract.save()
    return redirect('rental_contract_detail')
    
    
@login_required   
def cancelled(request, pk):
    rental_contract = get_object_or_404(RentalContract, pk=pk)
    if rental_contract.room_renter != request.user:
        return HttpResponse("You dont have right to do it")
    rental_contract.contract_status = 'CANCLED'
    rental_contract.save()
    return redirect('rental_contract_detail')
    
@login_required     
def rentalfeepaied(request, pk):
    rental_payment = get_object_or_404(RentalPayment, pk=pk)
    if rental_payment.renta;_contract.room_owner != request.user:
        return HttpResponse("You dont have right to do it")
    rental_payment.rental_fee_status = 'PAID'
    rental_payment.save()
    return redirect('rental_payment_detail')
    
@login_required     
def networkfeepaied(request, pk):
    rental_payment = get_object_or_404(RentalPayment, pk=pk)
    if rental_payment.renta;_contract.room_owner != request.user:
        return HttpResponse("You dont have right to do it")
    rental_payment.internet_fee_status = 'PAID'
    rental_payment.save()
    return redirect('rental_payment_detail')

@login_required    
def hubfeepaied(request, pk):
    rental_payment = get_object_or_404(RentalPayment, pk=pk)
    if rental_payment.renta;_contract.room_owner != request.user:
        return HttpResponse("You dont have right to do it")
    rental_payment.hub_fee_status = 'PAID'
    rental_payment.save()
    return redirect('rental_payment_detail')
    

        




    

