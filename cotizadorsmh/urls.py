from django.urls import path
from . import views

urlpatterns = [
    path('SeguroGastosMedicosIndividual/', views.CotizadorSMH)
]