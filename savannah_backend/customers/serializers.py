from rest_framework import serializers
from .models import Customer

class CustomerSerializer(serializers.ModelSerializer):
    # Access User model fields via the related user
    name = serializers.CharField(source="user.get_full_name", read_only=True)
    email = serializers.EmailField(source="user.email", read_only=True)

    class Meta:
        model = Customer
        fields = ["id", "name", "email", "phone"]
