from rest_framework import serializers
from .models import User, UploadedImage, AnalysisResult, Product, Appointment

class UserSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=True)
    password = serializers.CharField(write_only=True, required=True)
    first_name = serializers.CharField(required=True)
    last_name = serializers.CharField(required=True)
    age = serializers.IntegerField(required=False, allow_null=True)
    sex = serializers.CharField(required=False, allow_null=True)
    country = serializers.CharField(required=False, allow_null=True)
    skin_type = serializers.JSONField(required=False)
    skin_concerns = serializers.JSONField(required=False)
    is_active = serializers.BooleanField(required=False, default=True)
    last_skin_condition = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = (
            'id', 'username', 'email', 'first_name', 'last_name',
            'age', 'sex', 'country', 'skin_type', 'skin_concerns',
            'password', 'is_active', 'last_skin_condition'
        )

    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("A user with this email already exists.")
        return value

    def create(self, validated_data):
        # Generate username from email if not provided
        if 'username' not in validated_data:
            email = validated_data['email']
            username = email.split('@')[0]
            # Make username unique if necessary
            base_username = username
            counter = 1
            while User.objects.filter(username=username).exists():
                username = f"{base_username}{counter}"
                counter += 1
            validated_data['username'] = username

        # Create user with all fields
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password']
        )

        # Update additional fields
        for field in ['first_name', 'last_name', 'age', 'sex', 'country', 'skin_type', 'skin_concerns']:
            if field in validated_data:
                setattr(user, field, validated_data[field])
        user.save()

        return user

    def get_last_skin_condition(self, obj):
        if hasattr(obj, 'last_skin_condition'):
            return obj.last_skin_condition
        return 'No analysis yet'

class UploadedImageSerializer(serializers.ModelSerializer):
    image_url = serializers.SerializerMethodField()

    class Meta:
        model = UploadedImage
        fields = ('id', 'image', 'image_url', 'upload_timestamp')
        read_only_fields = ('upload_timestamp',)

    def get_image_url(self, obj):
        request = self.context.get('request')
        if obj.image and hasattr(obj.image, 'url'):
            return request.build_absolute_uri(obj.image.url) if request else obj.image.url
        return None

class AnalysisResultSerializer(serializers.ModelSerializer):
    class Meta:
        model = AnalysisResult
        fields = ('id', 'image', 'condition', 'confidence', 'recommendation_type', 'message', 'timestamp')
        read_only_fields = ('timestamp',)

class ProductSerializer(serializers.ModelSerializer):
    price = serializers.DecimalField(max_digits=10, decimal_places=2, coerce_to_string=False)
    image = serializers.ImageField(required=False)

    class Meta:
        model = Product
        fields = ('id', 'name', 'description', 'image', 'suitable_for', 'targets', 'when_to_apply', 'price', 'category', 'brand', 'stock')

class AppointmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Appointment
        fields = ('id', 'appointment_date', 'message', 'assigned_dermatologist', 'status', 'created_at')
        read_only_fields = ('created_at',) 