from rest_framework import serializers
from django.contrib.auth.models import User
from expense.models import Expenses

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username", "password", "email"]
        read_only_fields = ["id"]

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)


class ExpenseSerializer(serializers.ModelSerializer):
    class Meta:
        model=Expenses
        fields="__all__"
        read_only_fields=["id","created_at","owner"] 