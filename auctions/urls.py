from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create", views.create, name="create"),
    path("listings/<int:id>",views.listings,name="listings"),
    path("<int:id>/watch",views.watchList,name="watch"),
    path("<int:id>/unlist",views.unlist,name="unlist"),
    path("<int:id>/comment",views.postcomment,name="comment"),
    path("watchlist",views.get_watchlist,name="watchlist"),
    path("categories",views.list_by_categories,name="categories"),
    path("<int:id>/category",views.list_auctions_categories,name="auctioncategory")
]
