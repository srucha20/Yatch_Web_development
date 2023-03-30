from django.db import models
from django.contrib.auth.models import User
# Create your models here.



############################ SELLLER ######################################################
class seller(models.Model):
    user    = models.ForeignKey(User , on_delete=models.CASCADE)
    name    = models.CharField(max_length=50)
    phone   = models.CharField(max_length=20 , null=True , blank=True)
    address = models.CharField(max_length=20 , null=True , blank=True)


    def __str__(self):
        return self.name
sizes = (
    ('24' ,'24 meters') ,
    ('80' , '80 meters')
)


class yacht_details(models.Model):
    seller_id               = models.ForeignKey(seller , on_delete=models.CASCADE)
    yacht_type              = models.CharField(max_length=100)
    yacht_sizes             = models.CharField(max_length=50)
    yacht_style_categories  = models.CharField(max_length=100)
    rent_price              = models.BigIntegerField(default=0)
    yacht_image             = models.ImageField(upload_to="Yacht Images")

    def __str__(self):
        return  self.seller_id.name



############################ CUSTOMER ######################################################

class customer(models.Model):
    user        = models.ForeignKey(User , on_delete=models.CASCADE)
    name        = models.CharField(max_length=50)
    phone       = models.CharField(max_length=20 , null=True , blank=True)
    address     = models.CharField(max_length=20 , null=True , blank=True)
    price_range = models.IntegerField(default=0)


class book_yatch(models.Model):
    yacht_details_id = models.ForeignKey(yacht_details , on_delete=models.CASCADE)
    customer_id      = models.ForeignKey(customer , on_delete=models.CASCADE)
    rent_weeks       = models.CharField(max_length=50)
    price            = models.BigIntegerField(default=0)



