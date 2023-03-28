from django.urls import path
from app import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_view
from .forms import Login_form,MyPasswordChangeForm,myPasswordResetForm,MySetPassword
urlpatterns = [
    path('',views.productView.as_view(),name='home'),
    path('product-detail/<int:pk>', views.productdetailView.as_view(),
    name='product-detail'),
    path('cart/',views.show_cart,name='showcart'),
    path('add-to-cart/',views.add_to_cart,name='add-to-cart'),
    path('buy/',views.buy_now,name='buy-now'),
    path('profile/',views.profileView.as_view(),name='profile'),
    path('address/',views.address,name='address'),
    path('orders/',views.orders,name='orders'),
    path('kurta/', views.kurta,name='kurta'),
    path('kurta/<slug:data>',views.kurta,name='kurta1'),
    path('accounts/login/',auth_view.LoginView.as_view(template_name='app/login.html',
    authentication_form=Login_form),name='login'),
    path('logout/',auth_view.LogoutView.as_view(next_page='login'),name='logout'),
    path('registration/',views.customerregistrationView.as_view(),name='customerregistration'),
    path('checkout/', views.checkout,name='checkout'),
    path('passwordchange/',auth_view.PasswordChangeView.as_view(template_name='app/passwordchange.html',
    form_class=MyPasswordChangeForm,success_url='/passwordchangedone/'),name='passwordchange'),
    path('passwordchangedone/',auth_view.PasswordChangeView.as_view(template_name='app/passwordchangedone.html'),
    name='passwordchangedone'),
    path('password-reset/',auth_view.PasswordResetView.as_view(template_name='app/password_reset.html',
    form_class=myPasswordResetForm),name='password_reset'),
    path('password-reset/done/',auth_view.PasswordResetCompleteView.as_view(template_name='app/password_reset_done.html'),
    name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>/',auth_view.PasswordResetConfirmView.as_view(template_name='app/password_reset_confirm.html',
    form_class=MySetPassword),name='password_reset_confirm'),
    path('password-reset-complete/',auth_view.PasswordResetDoneView.as_view(template_name='app/password_reset_complete.html'),
    name='password_reset_complete'),
    path('pluscart/',views.plus_cart),
    path('minuscart/',views.minus_cart),
    path('removecart/',views.remove_cart),
    path('paymentdone/', views.payment_done,name='paymentdone'),
    path('search/',views.SearchResultsView.as_view(), name='search_results'),
]+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
