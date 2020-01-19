from django.shortcuts import render

# Create your views here.
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import *
from django.shortcuts import HttpResponse
from django.core import serializers
from rest_framework import serializers
from rest_framework import mixins
from rest_framework import generics
from rest_framework import viewsets
from rest_framework.authentication import BaseAuthentication
from rest_framework.permissions import BasePermission
from rest_framework.authentication import exceptions
from django.http import JsonResponse
from rest_framework.throttling import BaseThrottle
import time

VISIT_RECORD ={}

class VisitThrottle(BaseThrottle):
    def __init__(self):
        self.history = None

    def allow_request(self, request, view):
        remote_addr = request.META.get('REMOTE_ADDR')
        print(remote_addr)
        ctime = time.time()


        if remote_addr not in VISIT_RECORD:
            VISIT_RECORD[remote_addr]=[ctime,]
            return True
        history = VISIT_RECORD.get(remote_addr)
        self.history = history

        while history and history[-1]<ctime-60:
            history.pop()

        if len(history)<3:
            history.insert(0,ctime)
            return True
        else:
            return False
    def wait(self):
        ctime = time.time()
        return 60-(ctime-self.history[-1])




# class BookSerializers(serializers.Serializer):
#     title = serializers.CharField(max_length=32)
#     price = serializers.IntegerField()
#     pub_date = serializers.DateField()
#     publish = serializers.CharField(source='publish.name')
#     authors = serializers.SerializerMethodField()
#     def get_authors(self,obj):
#         temp = []
#         for author in obj.authors.all():
#             temp.append(author.name)
#         return temp

class Authentication(BaseAuthentication):

    def authenticate(self, request):
        token = request.GET.get('token')
        token_obj = member_token.objects.filter(token=token).first()
        if not token_obj:
            raise exceptions.AuthenticationFailed('验证失败！')
        return (token_obj.user,token_obj.token)


class Permission(BasePermission):
    def has_permission(self, request, view):
        if request.user.type == 1:
            return True
        return False

def get_random_str(user):
    import hashlib,time
    ctime = str(time.time())
    md5 = hashlib.md5(bytes(user,encoding='utf-8'))
    md5.update(bytes(ctime,encoding='utf-8'))
    return md5.hexdigest()


class LoginViewSet(APIView):
    authentication_classes = [Authentication,]
    permission_classes = [Permission,]
    throttle_classes = [VisitThrottle,]
    def post(self,request):
        username = request.data.get('username')
        password = request.data.get('password')
        user = member.objects.filter(username=username,password=password).first()
        ret = {'code':1000,'msg':''}
        if user:
            token = get_random_str(user.username)
            member_token.objects.update_or_create(user = user,defaults={'token':token})
            ret['token']= token

        else:
            ret['msg']='失败'
            ret['code']=1001
        return  JsonResponse(ret)



        return Response('login...')


class BookSerializers(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = '__all__'

    # publish = serializers.HyperlinkedIdentityField(
    #     view_name='publish_detail',
    #     lookup_field = 'publish_id',
    #     lookup_url_kwarg='id'
    #
    # )


class PublishSerializers(serializers.ModelSerializer):
    class Meta:
        model = Publish
        fields = '__all__'


class AuthorSerializers(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields ="__all__"





#     def create(self, validated_data):
#         authors = validated_data.pop('authors')
#         obj = Book.objects.create(**validated_data)
#         obj.authors.add(*authors)
#         # return obj

# class BookViewSet(APIView):
#
#     def get(self,request,*args,**kwargs):
#         book_list = Book.objects.all()
#         bs = BookSerializers(book_list,many=True,context={'request': request})
#         return Response(bs.data)
#
#     def post(self,request,*args,**kwargs):
#         bs = BookSerializers(data=request.data,many=False,context={'request': request})
#         if bs.is_valid():
#             bs.save()
#             return Response(bs.data)
#         else:
#             return Response(bs.errors)
#
#
# class BookDetailViewSet(APIView):
#     def get(self,request,id):
#         book = Book.objects.filter(id = id).first()
#         bs = BookSerializers(book)
#         return Response(bs.data)
#     def put(self,request,id):
#         book = Book.objects.filter(id = id).first()
#         bs = BookSerializers(book,data=request.data,context={'request': request})
#         if bs.is_valid():
#             bs.save()
#             return Response(bs.data)
#         else:
#             return Response(bs.errors)
#     def delete(self,request,id):
#         book = Book.objects.filter(id =id ).first()
#         book.delete()
#         return Response('')

# class BookViewSet(mixins.ListModelMixin,
#                   mixins.CreateModelMixin,
#                   generics.GenericAPIView):
#     queryset = Book.objects.all()
#     serializer_class = BookSerializers
#
#     def get(self,request):
#         return self.list(request)
#     def post(self,request):
#         return self.create(request)
#
#
# class BookDetailViewSet(mixins.RetrieveModelMixin,
#                         mixins.UpdateModelMixin,
#                         mixins.DestroyModelMixin,
#                         generics.GenericAPIView):
#
#     queryset = Book.objects.all()
#     serializer_class = BookSerializers
#
#     def get(self,request,*args,**kwargs):
#         return self.retrieve(request,*args,**kwargs)
#     def put(self,request,*args,**kwargs):
#         return self.update(request,*args,**kwargs)
#     def delete(self,request,*args,**kwargs):
#         return self.destroy(request,*args,**kwargs)

# class BookViewSet(generics.ListCreateAPIView):
#     queryset = Book.objects.all()
#     serializer_class = BookSerializers
#
# class BookDetailViewSet(generics.RetrieveUpdateDestroyAPIView):
#     queryset = Book.objects.all()
#     serializer_class = BookSerializers
class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializers

class PublishViewSet(APIView):
    def get(self,request):
        publish_list = Publish.objects.all()
        ps = PublishSerializers(publish_list,many=True)
        return Response(ps.data)

    def post(self,request):
        ps = PublishSerializers(data=request.data,many=False)
        if ps.is_valid():
            ps.save()
            return Response(ps.data)
        else:
            return Response(ps.errors)


class PublishDetailViewSet(APIView):
    def get(self,request,id):
        publisher = Publish.objects.filter(id = id).first()
        ps = PublishSerializers(publisher)
        return Response(ps.data)
    def put(self,request,id):
        publisher = Publish.objects.filter(id = id).first()
        ps = PublishSerializers(publisher,data=request.data)
        if ps.is_valid():
            ps.save()
            return Response(ps.data)
        else:
            return Response(ps.errors)
    def delete(self,request,id):
        publisher = Publish.objects.all().filter(id = id).first()
        publisher.delete()
        return Response()


class AuthorViewSet(APIView):
    def get(self,request):
        author_list = Author.objects.all()
        ap = AuthorSerializers(author_list,many=True)
        return Response(ap.data)
    def post(self,request):
        ap = AuthorSerializers(data=request.data,many=False)
        if ap.is_valid():
            ap.save()
            return Response(ap.data)
        else:
            return  Response(ap.errors)


class AuthorDetailViewSet(APIView):
    def get(self,request,id):
        author = Author.objects.filter(id = id).first()
        au = AuthorSerializers(author)
        return Response(au.data)
    def put(self,request,id):
        author = Author.objects.filter(id =id).first()
        au = AuthorSerializers(author,data=request.data)
        if au.is_valid():
            au.save()
            return Response(au.data)
        else:
            return Response(au.errors)
    def delete(self,request,id):
        author = Author.objects.filter(id = id).first()
        author.delete()
        return Response('')