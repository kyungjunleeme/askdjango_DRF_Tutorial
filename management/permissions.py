from rest_framework import permissions


class IsAuthorOrReadonly(permissions.BasePermission):
    # 인증이 되어야야만, 목록조회/포스팅등록을 허용
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated

    # SAFE_METHODS = ('GET', 'HEAD', 'OPTIONS')

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True

        # 포스팅 작성자에게 수정권한만 부여하고, 삭제는 superuser에게만.
        if request.method == "DELETE":
            return request.user.is_superuser  # 또는 request.user.is_staff

        return obj.author == request.user
