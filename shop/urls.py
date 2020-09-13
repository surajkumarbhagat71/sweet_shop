from django.urls import path
from shop.views import *

urlpatterns = [
    path('',HomeView.as_view(),name = 'home'),
    ############  User ###########################
    path('login', LoginView.as_view(),name='login'),
    path('order_summary/', OrderSummaryView.as_view(), name="order_summary"),
    path('user_registations/',UserRegistationView.as_view(),name = 'user_registations'),
    path('addtocart/<int:pk>',AddToCartView.as_view(),name='add_to_cart'),
    path('removeformtocart/<int:pk>/',RemoveItemFormCart.as_view(),name="removeformtocart"),
    path('checkout',CheckoutView.as_view(),name="checkout"),
    path('payment',PaymentView.as_view(),name="payment"),
    path('myorder',MyOrderView.as_view(),name='myorder'),
    path('user_logout',UserLogoutView.as_view(),name='logout'),


    ###############################   Admin ################################

    path('dashaboard',Dashaboard.as_view(),name="dashaboard"),
    path('owner_login',OwnerLoginView.as_view(),name="owner_login"),
    path('addsweet',AddSweet.as_view(),name='addsweet'),
    path('allsweet',AllSweetView.as_view(),name="allsweet"),
    path('admin_logout',AdminLogoutView.as_view(),name="admin_logout"),
]
