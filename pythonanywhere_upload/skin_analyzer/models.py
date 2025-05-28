from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone

class User(AbstractUser):
    email = models.EmailField(unique=True)
    age = models.IntegerField(null=True, blank=True)
    sex = models.CharField(max_length=10, null=True, blank=True)
    country = models.CharField(max_length=100, null=True, blank=True)
    skin_type = models.JSONField(null=True, blank=True, default=dict)
    skin_concerns = models.JSONField(null=True, blank=True, default=dict)
    is_active = models.BooleanField(default=True)
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']
    
    def __str__(self):
        return self.email

class UploadedImage(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='uploaded_images')
    image = models.ImageField(upload_to='user_uploads/')
    upload_timestamp = models.DateTimeField(default=timezone.now)
    
    def __str__(self):
        return f"{self.user.username}'s image - {self.upload_timestamp}"

class AnalysisResult(models.Model):
    image = models.ForeignKey(UploadedImage, on_delete=models.CASCADE, related_name='analysis_results')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='analysis_results')
    condition = models.CharField(max_length=100)
    confidence = models.FloatField()
    recommendation_type = models.CharField(max_length=50)  # products, refer, cautious_products
    message = models.TextField(null=True, blank=True)
    timestamp = models.DateTimeField(default=timezone.now)
    
    def __str__(self):
        return f"Analysis for {self.user.username}'s image - {self.condition}"

class Product(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    image = models.ImageField(upload_to='product_images/')
    suitable_for = models.TextField()
    targets = models.TextField()
    when_to_apply = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    category = models.CharField(max_length=100, default='Skincare')
    brand = models.CharField(max_length=100, default='Generic')
    stock = models.IntegerField(default=0)
    
    def __str__(self):
        return self.name

class Appointment(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('cancelled', 'Cancelled'),
        ('completed', 'Completed'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='appointments')
    appointment_date = models.DateTimeField()
    message = models.TextField()
    assigned_dermatologist = models.CharField(max_length=100, null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(default=timezone.now)
    
    def __str__(self):
        return f"Appointment for {self.user.username} on {self.appointment_date}"
