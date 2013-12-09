from django.forms import ModelForm
from django.forms.models import inlineformset_factory

from .models import Address, CheckList, RoomForRent, RentalContract, RentalPayment, Profile

class RoomForRentForm(ModelForm):
    class Meta:
        model = RoomForRent
        fields=("title", "start_date", "price", "description",)
        
AddressFormSet = inlineformset_factory(RoomForRent, Address)
CheckListFormSet = inlineformset_factory(RoomForRent, CheckList)
        
        
class RentalContractForm(ModelForm):
    class Meta:
        model = RentalContract
        fields=("room_for_rent","room_renter", "date_start", "date_end", "rental_fee", "internet_fee", "hub_fee",)
        
class RentalPaymentForm(ModelForm):
    class Meta:
        model = RentalPayment
        fields=("date_start", "date_end", "rental_fee", "internet_fee", "hub_fee",)
        
        
        
