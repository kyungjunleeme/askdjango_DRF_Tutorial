from django.shortcuts import render
from rest_framework import viewsets
from rest_framework import generics
from rest_framework.filters import SearchFilter, OrderingFilter

from rest_framework.response import Response
from rest_framework.serializers import Serializer
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from .permissions import IsAuthorOrReadonly

from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import api_view
from .serializers import PostSerializer
from .models import Post
from rest_framework.decorators import action
from rest_framework.renderers import TemplateHTMLRenderer
from management import serializers


# option#1 generics 사용하기
# class PublicPostListAPIView(generics.ListAPIView):
#     # queryset = Post.objects.filter(is_public=True)
#     queryset = Post.objects.all()  # filter(is_public=True)
#     serializer_class = PostSerializer

# option#2 APIView 사용하기
# class PublicPostListAPIView(APIView):
#     def get(self, request):
#         qs = Post.objects.filter(is_public=True)
#         serializer = PostSerializer(qs, many=True)
#         return Response(serializer.data)


# public_post_list = PublicPostListAPIView.as_view()


# option3 함수 기반 뷰 사용하기
# @api_view(["GET"])
# def public_post_list(request):
#     qs = Post.objects.filter(is_public=True)
#     serializer = PostSerializer(qs, many=True)
#     return Response(serializer.data)


# post_list, post_detail의 2개의 url을 ModelViewset이 내부적으로 처리 해줌
class PostViewSet(ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [
        IsAuthenticated,
        IsAuthorOrReadonly,
    ]  # 인증이 되어 있음을 보장 받음
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ["message"]

    # def dispatch(self, request, *args, **kwargs):
    #     print("request.body", request.body)
    #     print("request.POST", request.POST)
    #     return super().dispatch(request, *args, **kwargs)

    def perform_create(self, serializer):
        # FIXME: 인증이 되어있다는 가정하에, author를 지정해보겠습니다.
        author = self.request.user
        ip = self.request.META["REMOTE_ADDR"]
        serializer.save(author=author, ip=ip)

    @action(detail=False, methods=["GET"])
    def public(self, request):
        qs = self.get_queryset().filter(is_public=True)
        serializer = self.get_serializer(
            qs, many=True
        )  # serializer = PostSerializer(qs, many=True) 이거 대신에 get_serializer
        return Response(serializer.data)

    @action(detail=True, methods=["PATCH"])
    def set_public(self, request, pk):
        instance = self.get_object()  # get_object_or_404 대신에 get_object 멤버함수 사용
        instance.is_public = True
        instance.save(update_fields=["is_public"])  # .save() 하면 전체 field update 됨
        serializer = self.get_serializer(instance)
        return Response(serializer.data)  # status_code 추가 가능(인자 명 방식 확인 필요)


# def post_list(request):
#     # 2개 분기
#     pass

# def post_detail(request, pk):
#     # request.method # => 3개 분기
#     pass


class PostDetailAPIView(generics.RetrieveAPIView):
    queryset = Post.objects.all()
    renderer_classes = [TemplateHTMLRenderer]
    # TemplateHTMLRenderer 쓸 경우는 serializer 사용할 필요 없이 바로 넘기면 됨 post 바로 넘기고,
    # JSONRenderer 같은 경우는 serializer 도움 받아라
    template_name = "management/post_detail.html"

    def get(self, request, *args, **kwargs):
        post = self.get_object()  # RetrieveAPIView 내에 구현이 되어 있음
        return Response(
            {
                "post": PostSerializer(post).data,
            }
        )
