from django.urls import include, path
from rest_framework import routers
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register("post", views.PostViewSet)  # 2개의 URL을 만들어줍니다
# router.urls  # list 형태로 url 패턴 가지고 있음

urlpatterns = [
    # path("mypost/<int:pk>/", views.PostDetailAPIView.as_view()),
    # path("public/", views.public_post_list),
    path("", include(router.urls)),
]
