from django.urls import path, include

from .views import RegisterUserView, LoginUserView, LogoutUserView, ProfileDetails, ProfileEdit, \
    AddAdressView, DeleteAddressView, WishlistView, OrdersView

urlpatterns = (
    path('register/', RegisterUserView.as_view(), name='register_user'),
    path('login/', LoginUserView.as_view(), name='login_user'),
    path('logout/', LogoutUserView.as_view(), name='logout_user'),
    path("profile/", include([
        path("details/<int:pk>", ProfileDetails.as_view(), name="profile_details"),
        path("edit/<int:pk>", ProfileEdit.as_view(), name="edit_profile"),
        path("add_address/", AddAdressView.as_view(), name="add_address"),
        path("delete_address/<int:pk>", DeleteAddressView.as_view(), name='delete_adress'),
        path("wishlist/", WishlistView.as_view(), name="wishlist"),
        path("orders/", OrdersView.as_view(), name="profile_orders"),
    ]))
)
