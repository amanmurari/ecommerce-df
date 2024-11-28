from django.db import models
import uuid
from django.contrib.auth.models import User
from django.utils.html import html_safe
from ckeditor.fields import RichTextField
# Create y.our models here.
USER_type= {
     "vendor":"vendor",
     "customer":"customer"
}
RATEING={
     "1":"⭐",
     "2":"⭐⭐",
     "3":"⭐⭐⭐",
     "4":"⭐⭐⭐⭐",
     "5":"⭐⭐⭐⭐⭐",


}
STATUS = {
     "review": "review",
      "published": "published",
       "reject": "reject",

}
DELIVERY_METHODS = [
        (1, 'Courier delivery'),
        (2, 'Pickup at a parcel locker'),
        (3, 'Personal pickup'),     
    ]
    
PAYMENT_METHODS = [
        (1, 'Cash/card payment on delivery'),
        (2, 'Online payment by credit card'),
        (3, 'Traditional money transfer'),
    ]




class Profile(models.Model):
     user= models.OneToOneField(User,on_delete=models.CASCADE)
     usertype= models.CharField(max_length=200,choices=USER_type)
     image= models.ImageField(upload_to="image",null=True,blank=True)
     full_name= models.CharField(max_length=200,null=True,blank=True)
     mobile= models.IntegerField(null=True,blank=True)
     type= models.CharField(max_length=200,choices=USER_type,null=True,blank=True)

     def __str__(self) -> str:
          return self.user.username


class Category(models.Model):
    slug =models.SlugField(max_length=100,default=uuid.uuid4())
    name = models.CharField(max_length=100)
    image= models.ImageField(upload_to="image",blank=True,null=True)
    description=models.TextField()


    def __str__(self) -> str:
          return self.name
    

    class Meta:
         verbose_name= "Categorie"





class Products(models.Model):
    slug =models.SlugField(max_length=100,default=uuid.uuid4(),db_index=True,editable=False)
    category = models.ForeignKey(Category,on_delete=models.CASCADE)
    title= models.CharField(max_length=300)
    subtitle = models.TextField()
    description= models.TextField()

    
    image= models.ImageField(upload_to="products",blank=True,null=True)
    price= models.DecimalField(decimal_places=2,max_digits=12)
    sale_price= models.DecimalField(decimal_places=2,max_digits=12,blank=True,null=True)
    stock= models.IntegerField(default=100)
    status= models.CharField(max_length=40,choices=STATUS)
    publish_date= models.DateTimeField(auto_now=True,editable=False)
    update_date = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
          return self.title

    def discount_percent(self):
          disc= (self.price*self.discount)/100
          total= self.price-disc
          return total
    class Meta:
         verbose_name= "Products"
    


class Order(models.Model):
     

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='order_user', blank=True, null=True)
    first_name_order = models.CharField(max_length=255, blank=False, null=False)
    last_name_order = models.CharField(max_length=255, blank=False, null=False)
    delivery_method_order = models.IntegerField(choices=DELIVERY_METHODS, default=1, blank=False, null=False)
    payment_method_order = models.IntegerField(choices=PAYMENT_METHODS, default=1, blank=False, null=False)
    country_order = models.CharField(max_length=255, blank=False, null=False)
    city_order = models.CharField(max_length=255, blank=False, null=False)
    street_order = models.CharField(max_length=255, blank=False, null=False)
    house_number_order = models.CharField(max_length=255, blank=False, null=False)
    zip_code_order = models.CharField(max_length=255, blank=False, null=False)
    phone_number_order = models.CharField(max_length=255, blank=False, null=False)
    email_order = models.EmailField(max_length=255, blank=False, null=False)
    date_time_order = models.DateTimeField(auto_now=True, blank=False, null=False)


class OrderProduct(models.Model):
    product = models.ForeignKey(Products, on_delete=models.CASCADE, related_name='orderproduct_product', blank=False, null=False)
    quantity = models.FloatField(default=1.0, blank=False, null=False)
    order_id = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='orderproduct_order_id', blank=True, null=True)

    @property
    def get_total(self):
        total = self.product.price * self.quantity
        return total
    
    def __str__(self):
        return str(self.id)


class Cart(models.Model):
     product= models.ForeignKey(Products,on_delete=models.CASCADE)
     user= models.ForeignKey(User,on_delete=models.CASCADE)
     noi= models.IntegerField()
     date= models.DateField(auto_now=True)
     def price(self):
          if self.product.sale_price is None:
               return (self.product.price*self.noi)
          return [(self.product.sale_price*self.noi),
               (self.product.price*self.noi)
          ]


class Wishlist(models.Model):
     product= models.ForeignKey(Products,on_delete=models.CASCADE)
     user= models.ForeignKey(User,on_delete=models.CASCADE)
     noi= models.IntegerField()
     date= models.DateField(auto_now=True)


class Rateing(models.Model):
     product= models.ForeignKey(Products,on_delete=models.CASCADE)
     user= models.ForeignKey(User,on_delete=models.CASCADE)
     star= models.CharField(choices=RATEING,max_length=100)
     review= models.TextField()
     date= models.DateField(auto_now=True)
    