from django.contrib import admin
from django.utils.html import format_html
from django.contrib.auth.models import Permission

from management.models import Car, Promo, Rent


# Register your models here.


class CarAdmin(admin.ModelAdmin):

    list_display = ['id','name','years','color','image_tag',]
    list_per_number = 15
    list_filter = ['name', 'color', 'years']
    search_fields = ['name']    

    def image_tag(self, obj):
        return format_html('<img src="/media/{}" style="width:30%; margin-left: 20%;" />'.format(obj.pic_url))

    image_tag.short_description = 'Image'


    

class RentAdmin(admin.ModelAdmin):
    list_display = ['create_time','status','total_price','start_date','end_date','car_id','customer_id']
    list_per_number = 15
    list_filter = ['car_id','customer_id','status','total_price','start_date','end_date',]
    search_fields = ['car_id','customer_id','status','total_price','start_date','end_date',]

class PromoAdmin(admin.ModelAdmin):
    list_display = ['id','name','desc','promotion_code','discount_percent','minimum_cost','expire_day']
    list_per_number = 15
    list_filter = ['name', 'discount_percent', 'expire_day']
    search_fields = ['name']

admin.site.register(Car, CarAdmin)

admin.site.register(Permission)

admin.site.register(Promo, PromoAdmin)

admin.site.register(Rent, RentAdmin)
