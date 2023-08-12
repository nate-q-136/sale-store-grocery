from django.db import models
from shortuuid.django_fields import ShortUUIDField
from userauths.models import User
from django.utils.safestring import mark_safe
# Create your models here.

# make key, value
STATUS_CHOICE = (
    ("process", "Processing"),
    ("shiped", "Shipped"),
    ("delivered", "Delivered"),
)

STATUS = (
    ("draft", "Draft"),
    ("disabled", "Disabled"),
    ("rejected", "Rejected"),
    ("in_review", "In Review"),
    ("published", "Published"),
)

RATING = (
    (1,"★☆☆☆☆"),
    (2,"★★☆☆☆"),
    (3,"★★★☆☆"),
    (4,"★★★★☆"),
    (5,"★★★★★"),
)

def user_directory_path(instance, filename):
    return 'user_{0}/{1}'.format(instance.user.id, filename)
    pass


class Category(models.Model):
    id = ShortUUIDField(primary_key=True, unique=True, length=10, max_length=30, prefix="cat", alphabet="abcdefgh12345") # cat2371889475
    title = models.CharField(max_length=100, default="Food")
    image = models.ImageField(upload_to="category", default="category.jpg") # hình ảnh sẽ được tải lên thư mục "category"
    
    # class Meta dùng để cung cấp các cấu hình bổ sung cho model
    class Meta:
        # config như thế này thì khi nào trang admin thì thay vì thấy Category thì sẽ thấy Categories ở hàng danh mục quản lý
        verbose_name_plural = "Categories"
        
    
    def category_image(self):
        return mark_safe('<img src="%s" width="50" height="50" />' % (self.image.url))
    
    # show thuộc tính khi truy xuất mà đc print
    def __str__(self):
        return self.title


class Tags(models.Model):
    pass


# Vendor: nhà cung cấp, người ta cũng sẽ có cái account User riêng để bán hàng
class Vendor(models.Model):
    id = ShortUUIDField(primary_key=True, unique=True, length=15, max_length=20, prefix="venv", alphabet="abcdefgh12345")
    
    title = models.CharField(max_length=255, null=True, blank=True, default="Vinamilk")
    image = models.ImageField(upload_to=user_directory_path, default="vendor.jpg")
    description = models.TextField(null=True, blank=True,default="I am a great vendor")
    address = models.CharField(max_length=255, null=True, blank=True, default="218 Nguyen Luong Bang")
    contact = models.CharField(max_length=255, null=True, blank=True, default="+84 0974 2836")
    
    # thể hiện phần trăm response tin nhắn của Vendor
    chat_resp_time = models.CharField(max_length=255, null=True, default="100")
    
    # thể hiện phần trăm ship đúng giờ tin nhắn của Vendor
    shipping_on_time = models.CharField(max_length=255, null=True, default="100")
    authentic_rating = models.CharField(max_length=255, null=True, default="100")
    warranty_period = models.CharField(max_length=255, null=True, default="100")
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    
    
    class Meta:
        verbose_name_plural = "Vendors"
    
    def vendor_image(self):
        return mark_safe("<img src='%s' width='50' height='50' />" % (self.image.url))
    
    def __str__(self):
        return self.title
    pass


class Product(models.Model):
    id = ShortUUIDField(primary_key=True, unique=True, length=10, max_length=20, alphabet='abcdefgh12345')
    
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    Category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)
    
    title = models.CharField(max_length=100, default="Fresh Banana")
    image = models.ImageField(upload_to=user_directory_path, default="product.jpg")
    description = models.TextField(null=True, blank=True, default="This is the product")
    
    price = models.DecimalField(max_digits=100, decimal_places=2, default="1.99")
    old_price = models.DecimalField(max_digits=100, decimal_places=2, default="2.99")
    
    # Thông số kĩ thuật
    specifications = models.TextField(null=True, blank=True)
    # tag kiểu #food #vinamilk,...
    tags = models.ForeignKey(Tags, on_delete=models.SET_NULL, null=True, blank=True)
    
    product_status = models.CharField(choices=STATUS, max_length=10, default="in_review")
    
    status = models.BooleanField(default=True)
    in_stock = models.BooleanField(default=True)
    # làm nổi bật sản phẩm ko
    featured = models.BooleanField(default=False)
    # sản phẩm digital, ko có hiện vật ko
    digital = models.BooleanField(default=False)
    
    sku = ShortUUIDField(unique=True, length=4, max_length=10, prefix="sku", alphabet="1234567890")
    date = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(null=True, blank=True)
    
    
    class Meta:
        verbose_name_plural = "Products"
    
    def product_image(self):
        return mark_safe("<img src='%s' width='50 height='50'/>" % (self.image.url))
    
    def __str__(self):
        return self.title
        
    def get_percentage(self):
        new_price = (self.price / self.old_price) * 100
        return new_price
    
# user may add multiple image for a product
class ProductImages(models.Model):
    images = models.ImageField(upload_to='product_images', default='product.jpg')
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    date = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name_plural = 'Product Images'

    pass

#------------------- Cart, Order, OrderItems and Address --------------------

# Các giỏ hàng đặt hàng
class CartOrder(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=100, decimal_places=2, default="1.99")
    paid_status = models.BooleanField(default=False)
    order_date = models.DateTimeField(auto_now_add=True)
    product_status = models.CharField(choices=STATUS_CHOICE, max_length=10, default="processing")
    pass


class CartOrderItems(models.Model):
    order = models.ForeignKey(CartOrder, on_delete=models.CASCADE)
    invoice_no = models.CharField(max_length=200)
    product_status = models.CharField(max_length=200)
    item = models.CharField(max_length=200)
    image = models.CharField(max_length=200)
    quantity = models.IntegerField(default=0)
    price = models.DecimalField(max_digits=100, decimal_places=2, default="1.99")
    total = models.DecimalField(max_digits=100, decimal_places=2, default="1.99")
    pass

    class Meta:
        verbose_name_plural = "Cart Order Items"
        
    
    def order_img(self):
        return mark_safe('<img src="/media/%s" width="50" height="50"/>' % (self.image))



# ----------------------Product Review, wishlists, Address---------------------#

class ProductReview(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    review = models.TextField()
    rating = models.IntegerField(choices=RATING, default=5)
    date = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name_plural = "Product Reviews"
    
    def __str__(self):
        return self.product.title
    
    def get_rating(self):
        return self.rating
    pass 

class wishlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    date = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name_plural = "wishlists"
        
    def __str__(self):
        return self.product.title

class Address(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    address = models.CharField(max_length=255, null=True)
    status = models.BooleanField(default=False)
    
    class Meta:
        verbose_name_plural = "Addresses"
