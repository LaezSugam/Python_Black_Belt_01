from __future__ import unicode_literals

from django.db import models
from ..log_reg.models import Users

import datetime

# Create your models here.
class ItemManager(models.Manager):
    def create_item(self, postData, user_id):
        errors = []
        if len(postData["item"]) < 3:
            errors.append("Item name must be at least 3 characters")


        if not errors:
            user = Users.objects.get(id=user_id)
            try:
                wlist = WishList.objects.get(user=user)
            except:
                wlist = WishList.objects.create(user=user)

            new_item = self.create(name=postData["item"], user=user)
            new_item.wish_list.add(wlist)
            return (True, "Item successfully created.")
        else:
            return (False, errors)

class WishList(models.Model):
    user = models.OneToOneField(Users, related_name="wishlist_by_user")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Item(models.Model):
    name = models.CharField(max_length=255)
    user = models.ForeignKey(Users, related_name="items_by_user")
    wish_list = models.ManyToManyField(WishList, related_name="items_by_wishlist")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = ItemManager()
