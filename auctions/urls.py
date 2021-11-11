from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create", views.create, name="create"),
    path("listing/<str:list_id>", views.bid_listing, name="bid_listing"),
    path("listing/<int:list_id>/watchlist", views.watchlist, name="watchlist"),
    path("listing/<int:list_id>/deletelist", views.deletelist, name="deletelist"),
    path("userwatchlist", views.userwatchlist, name="userwatchlist"),
    path("category", views.category, name="category"),
    path("category/<str:entry>", views.find_category, name="find_category")
]
