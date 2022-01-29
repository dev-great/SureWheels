from django.db import models
from django.db.models.fields import CharField, DateTimeField
from django.forms.fields import ImageField
from django.conf import settings
from django.contrib.auth.models import User
from django.urls import reverse
import secrets
from cloudinary.models import CloudinaryField

from django.utils import timezone
# Create your models here.
class Car(models.Model):

    CATEGORY_CAR = (
        ('CITY','Within the city'),
        ('OUT_CITY', 'Out of city'),
    )

    COLOR = (
        ('BLUE','Blue'),
        ('RED','Red'),
        ('PINK','Pink'),
        ('ORANGE','Orange'),
        ('BLACK','Black'),
        ('WHI','White'),
        ('SILVER','Silver'),
        ('BRONZ','Brown'),
        ('YELLOW','Yellow'),
        ('Green', 'Green')
    )

    TYPE_GEAR = (
        ('AUTO','Automatic transmission'),
        ('MANUAL','Manual transmission'),
        ('CVT','CVT gear'),
        ('DTC','Semi-automatic transmission and DCT dual-clutch transmission')
    )

    STATUS = (
        ('AVAILABLE','Free'),
        ('NO_AVAILABLE','Unavailable'),
        ('HIDE','Hide')
    )
    REASON = (
        ('AIRPORT_TRANSFER','Airport pickup and dropoff'),
        ('RENT_LEASE','Rent and Lease'),
        ('ESCORT','Escort and protocol service')
    )

    name = models.CharField(max_length=60)
    years = models.CharField(max_length=4)
    color = models.CharField(max_length=20, choices=COLOR)
    reason = models.CharField(max_length=20, choices=REASON)
    category = models.CharField(max_length=10, choices=CATEGORY_CAR)
    type_gear = models.CharField(max_length=10, choices=TYPE_GEAR)
    number_seat = models.SmallIntegerField()
    number_door = models.SmallIntegerField()
    status = models.CharField(max_length=12, choices=STATUS)
    price = models.IntegerField()
    create_time = models.DateField(auto_now_add=True)
    update_time = models.DateField(auto_now=True)
    pic_url =  models.ImageField(upload_to='images/')


    def __str__(self):
        return self.name + " " + self.years + " ("+ self.status+")"
    

class Promo(models.Model):
    name = models.CharField(max_length=20)
    desc = models.CharField(max_length=50)
    promotion_code = models.CharField(max_length=8,unique=True)
    discount_percent = models.FloatField()
    minimum_cost = models.IntegerField()
    expire_day = models.DateTimeField()
    is_active = models.BooleanField()

class Rent(models.Model):
    STATUS = (
        ('Picked','Got the car'),
        ('Approved','Confirm'),   
        ('Denied','Refuse'),
        ('Returned','Returned'),
        ('Pending','Pending')
    )
    ref_code = models.CharField(max_length=20)
    create_time = models.DateField(auto_now_add=True)
    update_time = models.DateField(auto_now=True)
    status = models.CharField(max_length=8, choices=STATUS)
    total_price = models.IntegerField()
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    car_id = models.ForeignKey(Car, on_delete=models.DO_NOTHING)
    customer_id = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    promotion = models.ForeignKey(Promo, on_delete=models.DO_NOTHING, null=True)
    payment_order = models.ForeignKey('Payment', on_delete=models.SET_NULL, null=True,blank=True)
    ordered = models.BooleanField(default=False)
           



class Payment(models.Model):
    
    amount = models.ForeignKey(Rent, on_delete=models.DO_NOTHING)
    email = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    ref = models.CharField(max_length=200)
    verified = models.BooleanField(default=False)
    date_created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ("-date_created",)

    def __str__(self) -> str:
        return f"{self.user.username} - {self.amount}"

    def save(self, *args, **kwargs):
        while not self.ref:
            ref = secrets.token_urlsafe(50)
            object_with_similar_ref = Payment.objects.filter(ref=ref).first()
            if not object_with_similar_ref:
                self.ref = ref
        super().save(*args, **kwargs)

    def amount_value(self):
        return self.amount * 100

    

