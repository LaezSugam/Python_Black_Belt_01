
from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index, name = "index"),
    url(r'^add_item$', views.add_item, name = "add_item"),
    url(r'^create_item/(?P<user_id>\d+)$', views.create_item, name = "create_item"),
    url(r'^delete_item/(?P<item_id>\d+)$', views.delete_item, name = "delete_item"),
    url(r'^item/(?P<item_id>\d+)$', views.item, name = "item"),
    url(r'^add_to_wishlist/(?P<user_id>\d+)/(?P<item_id>\d+)$', views.add_to_wishlist, name = "add_to_wishlist"),
    url(r'^remove_from_wishlist/(?P<user_id>\d+)/(?P<item_id>\d+)$', views.remove_from_wishlist, name = "remove_from_wishlist"),
]
