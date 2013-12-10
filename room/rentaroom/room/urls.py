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
    url("^room_for_rent/(?P<slug>.*)/$",
        RoomForRentDetail.as_view(),
        name="room_for_rent_detail"),
    url("^room_for_rent/make_a_contract",
        RentalContractCreate.as_view(),
        name="rental_contract_create"),
    url("^room_for_rent/make_a_payment",
        RentalPaymentCreate.as_view(),
        name="rental_payment_create"),
    url("^rental_contract/list/$",
        RentalContractList.as_view(),
        name="rental_contract_list"),
    url("^rental_contract/(?P<slug>.*)/$",
        RentalContractDetail.as_view(),
        name="rental_contract_detail"),
    url("^rental_payment/(?P<slug>.*)/$",
        RentalPaymentDetail.as_view(),
        name="rental_payment_detail"),
    
    url("^rental_contract/(?P<slug>.*)/rental_payment_create/$",
        login_required(RentalPaymentCreate.as_view()),
        name="rental_payment_create"),
    url(r'^rental_payment/(?P<pk>\d+)/confirmed/$', confirmed, name='rental_contract_confirmed'),
)