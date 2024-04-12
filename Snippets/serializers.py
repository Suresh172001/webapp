from rest_framework import serializers
from .models import TableText,MappingTable
from django.contrib.auth import get_user_model
UserUsers = get_user_model()

# from django.contrib.auth.hashers import check_password
from rest_framework import serializers

class UserSerializer(serializers.ModelSerializer):
    username = serializers.CharField(max_length=25)
    password = serializers.CharField(max_length=25)
    class Meta:
        model = UserUsers
        fields = ['username', 'password']


class UserData (serializers.ModelSerializer):
    id = serializers.IntegerField()
    username = serializers.CharField(max_length=25)
    is_superuser = serializers.CharField(default=True)
    is_staff = serializers.CharField(default=True)
    is_active = serializers.CharField(default=True)
    password = serializers.CharField(max_length=25)
    email = serializers.CharField(max_length=25)
    class Meta:
        model = UserUsers
        fields = '__all__'

class TitleCreateSerializer(serializers.ModelSerializer):
    title = serializers.CharField(max_length=50)
    class Meta:
        model = MappingTable
        fields = '__all__'

    def create(self,title):
        data = MappingTable.objects.filter(title=title)
        if not data:
            add_title = MappingTable.objects.create(title=title)
        return add_title

class SnippetCreateSerializer(serializers.ModelSerializer):
    
    title = serializers.CharField(max_length=50)
    snippets = serializers.CharField(max_length=150)
    created_user = serializers.CharField(max_length=150)
    class Meta:
        model = TableText
        fields = '__all__'

    def update(self,id, validated_data):
        data = TableText.objects.filter(id=id).update(**validated_data)
        return data


class SnippetSerializer(serializers.Serializer):

    title = serializers.CharField(max_length=50)
    snippets = serializers.CharField(max_length=150)
    created_user = serializers.CharField(max_length=150)
    created_at_date = serializers.DateTimeField()
    updated_at_date = serializers.DateTimeField()
    
class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=25)
    password = serializers.CharField()
 
    
