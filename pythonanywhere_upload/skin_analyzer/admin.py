from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, UploadedImage, AnalysisResult, Product, Appointment

class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'age', 'is_staff')
    fieldsets = UserAdmin.fieldsets + (
        ('Additional Info', {'fields': ('age',)}),
    )

class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'brand', 'category', 'price', 'when_to_apply')
    list_filter = ('category', 'brand', 'when_to_apply')
    search_fields = ('name', 'description', 'brand')
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'brand', 'category', 'price')
        }),
        ('Product Details', {
            'fields': ('description', 'image', 'suitable_for', 'targets', 'when_to_apply')
        }),
    )
    list_editable = ('price', 'category', 'brand')

admin.site.register(User, CustomUserAdmin)
admin.site.register(UploadedImage)
admin.site.register(AnalysisResult)
admin.site.register(Product, ProductAdmin)
admin.site.register(Appointment)
