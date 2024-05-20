#programado por: Andres Rua
from django.urls import path, include
from .views import *
payment_service = checkPayment()  # Reemplaza esto con tu servicio de pago real
pdf_service = PDFGenerator()


urlpatterns = [
    path("", HomePageView.as_view(), name='home'),
    path('about/', AboutPageView.as_view(), name='about'),
    path('signup/', SignupView.as_view(), name='signup'),
    path('login/', LoginView.as_view(), name='login1'),
    path('logout/', LogOutView.as_view(), name="logout1"),
    path("i18n/", include("django.conf.urls.i18n")),


    path('ropa/', RopaListView.as_view(), name='ropa_index'),
    path('ropa/create', RopaCreateView.as_view(), name='ropa_create'),
    path('ropa/<str:id>', RopaShowView.as_view(), name='show'),
    path('ropa/<int:id>/delete/', RopaDeleteView.as_view(), name='ropa_delete'),

    path('regalos/', RegaloIndexView.as_view(), name='regalos'),
    path('regalos/create', RegaloCreateView.as_view(), name='regalos_create'),
    path('regalos/<str:id>', RegaloShowView.as_view(), name='regalo_show'),
    path('regalos/<int:id>/delete/', RegaloDeleteView.as_view(), name='regalo_delete'),

    path('reviews/', ReviewIndexView.as_view(), name='misreviews'),
    path('reviews/create', ReviewCreateView.as_view(), name='forreview'),
    path('reviews/<str:id>', ReviewShowView.as_view(), name='reviews'),
    path('reviews/<int:id>/delete/', ReviewDeleteView.as_view(), name='review_delete'),  

    path('cart/', CartView.as_view(), name='cart_index'),
    path('cart/add/<str:ropa_id>', CartView.as_view(), name='cart_add'),
    path('cart/removeAll', CartRemoveAllView.as_view(), name='cart_removeAll'),
    path('finalizar-compra/', FinalizarCompraView.as_view(), name='finalizar_compra'),
    path('download-pdf/', download_pdf, name='download_pdf'),

    path('api/json/', lista_productos, name='lista_productos_json'),
    path('check/', mostrar_cheque, name = 'check'),
]
