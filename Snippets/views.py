from django.http import JsonResponse
from rest_framework import status
from .models import TableText
from rest_framework.views import APIView
from .serializers import LoginSerializer,SnippetSerializer ,SnippetCreateSerializer,TitleCreateSerializer
from rest_framework.authentication import SessionAuthentication, BasicAuthentication

from django.contrib.auth import get_user_model
UserUsers = get_user_model()

from django.http import JsonResponse
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate
from django.contrib.auth import login,logout

from rest_framework.permissions import IsAuthenticated
from django.http import JsonResponse
from .serializers import  UserSerializer

import jwt
from datetime import datetime, timedelta
from django.conf import settings

class CustomAuthToken(ObtainAuthToken):
    
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        print(request.data)
        if not serializer.is_valid():
            return JsonResponse({"status": 403, 'message': 'Something went wrong'})

        username = serializer.validated_data['username']
        password = serializer.validated_data['password']

        user = UserUsers.objects.get(username=username)
        stored_password = user.password
        
        if not user:
            return JsonResponse({"status": 403, 'message': 'Invalid username or password'})

        token, created = Token.objects.get_or_create(user=user)
        return JsonResponse({'token': token.key})

class UserDetails(APIView):
    authentication_classes = ()
    permission_classes = ()

    def post(token, request):
       
        serializer = LoginSerializer(data=request.data)

        if not serializer.is_valid():
            return JsonResponse({"status": 403, 'message': 'Something went wrong'})

        username = serializer.validated_data['username']
        password = serializer.validated_data['password']
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)

        token_payload = {
                'user_id': user.id,
                'username': username,
                'exp': datetime.now() + timedelta(days=1)  # Token expiration time
            }
        token = jwt.encode(token_payload, settings.SECRET_KEY, algorithm='HS256')
        response_data = {
            'Message': 'Login successful.',
            'User_details': {
                'User id': user.id,
                'User Name': username,
                'User Password': password,
                'User Email': user.email,
                'Is Staff': user.is_staff,
                'Is SuperUser': user.is_superuser,
                'Is Active': user.is_active,

            },

            'Token': token.decode('utf-8'),
        }

        return JsonResponse(response_data, safe=False)
        
 
class snippets(APIView):
    
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]
    # authentication_classes = ()
    # permission_classes = ()   
    def get(self,request):
        print("entered..")
        details = TableText.objects.all()
        total = TableText.objects.all().count()
        serializer = SnippetSerializer(instance=details, many=True)
        return JsonResponse({'Total Snippets': total,'details': serializer.data}, status=status.HTTP_200_OK)
    
    def post(self, request):
        data=request.data
        data['created_at_date']= datetime.now()
        serializer = SnippetCreateSerializer(data=data)
        add_title = TitleCreateSerializer(data=data['title'])
        if serializer.is_valid() :
            if add_title.is_valid():
                add_title.save()
            serializer.save()
            return JsonResponse({"status": "snippet_created_successfully"}, status=status.HTTP_201_CREATED)
        return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request):
        request1=request.data
        id=request1['id']
        data= TableText.objects.filter(id=id)
        if data:
            data.delete() 
            return JsonResponse({"status": "deleted_successfully"},status=status.HTTP_204_NO_CONTENT)
        else:
            return JsonResponse({"status": "data_not_found"},status=status.HTTP_204_NO_CONTENT)
    
    def put(self, request,id):
        
        data=request.data
        data['updated_at_date']= datetime.now()
        serializer = SnippetCreateSerializer(id,data=data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return JsonResponse({"status": "updated_successfully"}, status=status.HTTP_201_CREATED)
        return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def patch(self, request,id):
        serializer = SnippetCreateSerializer(id,data=request.data, partial = True)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse({"status": "updated_successfully"}, status=status.HTTP_201_CREATED)
        return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    