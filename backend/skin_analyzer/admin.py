from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, UploadedImage, AnalysisResult, Product, Appointment

@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = ('email', 'username', 'is_staff', 'is_active', 'date_joined')
    list_filter = ('is_staff', 'is_active', 'role')
    search_fields = ('email', 'username')
    ordering = ('-date_joined',)
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('username', 'first_name', 'last_name')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'role')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', 'is_staff', 'is_active')}
        ),
    )

@admin.register(UploadedImage)
class UploadedImageAdmin(admin.ModelAdmin):
    list_display = ('user', 'image', 'uploaded_at')
    list_filter = ('uploaded_at',)
    search_fields = ('user__email', 'user__username')
    readonly_fields = ('uploaded_at',)

@admin.register(AnalysisResult)
class AnalysisResultAdmin(admin.ModelAdmin):
    list_display = ('user', 'condition', 'confidence', 'timestamp')
    list_filter = ('condition', 'timestamp')
    search_fields = ('user__email', 'condition')
    readonly_fields = ('timestamp',)

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'brand', 'category', 'price')
    list_filter = ('category', 'brand')
    search_fields = ('name', 'description', 'brand')
    list_editable = ('price', 'category')

@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = ('user', 'dermatologist', 'date', 'status')
    list_filter = ('status', 'date')
    search_fields = ('user__email', 'dermatologist__email')
    readonly_fields = ('created_at',) 