from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("add", views.addListing, name="add"),
    path("showCat", views.showCat, name="showCat"),
    path("listing/<int:id>", views.listing, name="listing"),
    path("remove/<int:id>", views.remove, name="remove"),
    path("append/<int:id>", views.append, name="append"),
    path("watchlist", views.showWatchlist, name="watchlist"),
    path("postComment/<int:id>", views.postComment, name="postComment"),
    path("addBid/<int:id>", views.addBid, name="addBid"),
    path("close/<int:id>", views.close, name="close")
]
