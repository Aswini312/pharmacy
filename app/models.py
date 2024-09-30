from django.db import models
from django.contrib.auth.models import User



class Product(models.Model):

  title = models.CharField(max_length=100)
  price = models.FloatField()
  description = models.TextField()  
  expiry_date = models.DateField() 
  mg = models.IntegerField()  
  net_quantity = models.PositiveIntegerField()
  batch_no = models.CharField(max_length=50)
  brand = models.CharField(max_length=100)
  # item_weight = models.DecimalField(max_digits=10, decimal_places=2)
  item_form = models.CharField(max_length=50)
  age_range = models.CharField(max_length=20)
  item_dimension = models.CharField(max_length=50)
  availability_status = models.CharField(max_length=20)
  product_image = models.ImageField(upload_to='product')



class CartItem(models.Model):
  product = models.ForeignKey(Product, on_delete=models.CASCADE)
  quantity = models.IntegerField(default=1)
  user = models.ForeignKey(User, default=1, on_delete=models.CASCADE)



class Wishlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)

    def _str_(self):
      return f'{self.user.username} Wishlist'  
    

class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    total_price = models.FloatField(default=0.0)
    

    def __str__(self):
        return f'Order {self.id} by {self.user.username}'


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()

    def __str__(self):
        return f'{self.quantity} of {self.product.title}'        
  

class Booking(models.Model):
    booking_id = models.CharField(max_length=100)
    total = models.FloatField()
    book_date = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # Link to User

    def __str__(self):
        return f'Booking {self.booking_id} by {self.user.username}'


# ... existing code ...

class ProductDetail(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    total_price = models.FloatField()

    def __str__(self):
        return f'{self.product.title} - Quantity: {self.quantity}, Total: {self.total_price}'


