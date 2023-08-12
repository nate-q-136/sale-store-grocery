from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.

# extends and config AbstractUser
class User(AbstractUser):
    email = models.EmailField(max_length=255, unique=True, null=False)
    username = models.CharField(max_length=255)
    bio = models.CharField(max_length=255)
    
    # Instead of using username as default to login and authenticate, use email because email was set unique in custom above
    USERNAME_FIELD = 'email'
    # Điều này đảm bảo rằng ngoài trường 'email' 
    #, bạn cũng cần có giá trị cho trường 'username' khi tạo người dùng mới
    # Nếu không có thì tạo người dùng chỉ cần email và password
    REQUIRED_FIELDS = ['username']
    
    def __str__(self):
        return self.username
    pass