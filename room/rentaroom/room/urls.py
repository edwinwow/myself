from django.conf.urls import patterns, url
from django.contrib.auth.decorators import login_required

from .views import RoomForRentList, RoomForRentDetail, RoomForRentCreate, RentalContractCreate, RentalPaymentCreate, RentalContractDetail, RentalContractCreate, RentalPaymentDetail, RentalPaymentCreate
from .views import confirmed, RentalContractList

urlpatterns = patterns("",
    url("^$",
        RoomForRentList.as_view(),
        name="home"),
    url("^room_for_rent/create/$",
        login_required(RoomForRentCreate.as_view()),
        name="room_for_rent_create"),
    url("^room_for_rent/(?P<pk>\d+)/$",
        RoomForRentDetail.as_view(),
        name="room_for_rent_detail"),
    url("^room_for_rent/(?P<pk>\d+)/make_a_contract/$",
        RentalContractCreate.as_view(),
        name="rental_contract_create"),
    url("^rental_contract/((?P<pk>\d+)/make_a_payment/$",
        RentalPaymentCreate.as_view(),
        name="rental_payment_create"),
    url("^rental_contract/list/$",
        RentalContractList.as_view(),
        name="rental_contract_list"),
    url("^rental_contract/((?P<pk>\d+)/$",
        RentalContractDetail.as_view(),
        name="rental_contract_detail"),
    url("^rental_payment/((?P<pk>\d+)/$",
        RentalPaymentDetail.as_view(),
        name="rental_payment_detail"),
    
    url("^rental_contract/((?P<pk>\d+)/rental_payment_create/$",
        login_required(RentalPaymentCreate.as_view()),
        name="rental_payment_create"),
    
    url("^rental_contract/((?P<pk>\d+)/confirm/$",
        view.confirmed,
        name="rental_contract_confirm"),
    url("^rental_contract/((?P<pk>\d+)/decline/$",
        view.declined,
        name="rental_contract_decline"),
    url("^rental_contract/((?P<pk>\d+)/cancel/$",
        view.cancelled,
        name="rental_contract_cancel"),
    url("^rental_payment/((?P<pk>\d+)/rentalfeepaied/$",
        view.rentalfeepaied,
        name="rental_payment_rentalfeepaied"),
    url("^rental_payment/((?P<pk>\d+)/networkfeepaied/$",
        view.networkfeepaied,
        name="rental_payment_networkfeepaied"),
    url("^rental_payment/((?P<pk>\d+)/hubfeepaied/$",
        view.hubfeepaied,
        name="rental_payment_hubfeepaied"),
)
