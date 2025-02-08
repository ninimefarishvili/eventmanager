from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.


# class Customer(models.Model):
#     username = models.CharField("iuzerneimi")

#     email = models.EmailField("ელ.ფოსტის მისამართი", unique=True)

#     is_active = models.BooleanField("აქტიურია", default=False)
#     def __str__(self):
#         return self.get_full_name()

#     def get_full_name(self):
#         return f"{self.first_name} {self.last_name}".strip() or self.email

#     get_full_name.verbose_name = "სრული სახელი"

#     def make_superuser(self):
#         self.is_active = True
#         self.is_staff = True
#         self.is_superuser = True

#     class Meta:
#         ordering = ("-id",)
#         verbose_name = "მომხმარებელი"
#         verbose_name_plural = "მომხმარებლები"

#         indexes = [
#             models.Index(fields=["is_active"]),
#             models.Index(fields=["is_staff"]),
#         ]