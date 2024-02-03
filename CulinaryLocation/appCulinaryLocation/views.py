from django.shortcuts import render
from django.template import loader
from django.views.decorators.csrf import csrf_exempt
from firebase_admin.auth import get_user
from oauth2_provider.contrib.rest_framework import authentication
from oauthlib.uri_validate import query
from rest_framework import viewsets, permissions, status, generics
from rest_framework.response import Response
from django.http import JsonResponse, HttpResponse
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404

from .models import User, ShipmentDetails, Menu, MenuDetails, Bill, Dish, Account, Confirm, Address, Food, Time, \
    SaleTime, BillDetails, Review, Follow, Comment, BotChat, ChatbotModel
from .serializers import (InformationUserSerializer, TimeSerializer, SaleTimeSerializer,
                          ShipmentDetailsSerializer, UserSerializer, ShopSerializer,
                          DishSerializer, FoodSerializer, MenuSerializer,
                          AccountSerializer, AddDishSerializer, CommentSerializer,
                          ReplyToCommentsSerializer, MenuDetailsSerializer, BillSerializer, BillDetailsSerializer,
                          FollowSerializer, ReviewSerializer)
from rest_framework.decorators import action
from rest_framework.parsers import MultiPartParser
from rest_framework.views import APIView
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from django.utils import timezone


class MonAnHienTaiViewSet(viewsets.ModelViewSet):
    queryset = Dish.objects.all()
    serializer_class = DishSerializer

    def list(self, request, *args, **kwargs):
        # Lấy thời điểm hiện tại
        current_time = timezone.localtime(timezone.now())
        current_hour = current_time.hour

        print("Giờ hiện tại là:", current_hour)
        current_thoi_gian_bans = SaleTime.objects.filter(thoi_diem__thoi_gian_bat_dau__lte=current_time, thoi_diem__thoi_gian_ket_thuc__gte=current_time)

        mon_an_ids = current_thoi_gian_bans.values_list('mon_an', flat=True)
        queryset = Dish.objects.filter(id__in=mon_an_ids)

        serializer = DishSerializer(queryset, many=True)
        serialized_data = serializer.data

        return Response(serialized_data)


class ThongTinTaiKhoanView(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = InformationUserSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return User.objects.filter(id=self.request.user.id)


class ThoiDiemView(viewsets.ModelViewSet):
    queryset = Time.objects.all()
    serializer_class = TimeSerializer
    permission_classes = [IsAuthenticated]


class ThoiGianBanView(viewsets.ModelViewSet):
    queryset = SaleTime.objects.all()
    serializer_class = SaleTimeSerializer


class ThongTinGiaoHangView(viewsets.ModelViewSet):
    queryset = ShipmentDetails.objects.all()
    serializer_class = ShipmentDetailsSerializer


class DanhGiaViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer


class FollowViewSet(viewsets.ModelViewSet):
    queryset = Follow.objects.all()
    serializer_class = FollowSerializer


class ChiTietMenuViewSet(viewsets.ModelViewSet):
    queryset = MenuDetails.objects.all()
    serializer_class = MenuDetailsSerializer


class LoaiThucAnViewSet(viewsets.ModelViewSet):
    queryset = Food.objects.all()
    serializer_class = FoodSerializer


class MonAnViewSet(viewsets.ModelViewSet):
    queryset = Dish.objects.all()
    serializer_class = DishSerializer


class MenuHienTaiViewSet(viewsets.ModelViewSet):
    queryset=Menu.objects.all()
    serializer_class = MenuSerializer

    def list(self, request, *args, **kwargs):
        # Lấy thời điểm hiện tại
        current_time = timezone.localtime(timezone.now())
        current_hour = current_time.hour

        print("Giờ hiện tại là:", current_hour)
        current_thoi_gian_bans = SaleTime.objects.filter(thoi_diem__thoi_gian_bat_dau__lte=current_time,
                                                            thoi_diem__thoi_gian_ket_thuc__gte=current_time)

        menu_ids = current_thoi_gian_bans.values_list('menu', flat=True)
        queryset = Menu.objects.filter(id__in=menu_ids)

        serializer = MenuSerializer(queryset, many=True)
        serialized_data = serializer.data

        return Response(serialized_data)


class MenuViewSet(viewsets.ModelViewSet):
    queryset = Menu.objects.all()
    serializer_class = MenuSerializer

    @action(methods=['post'], detail=True, url_path='active-menu', url_name='active-menu')
    def hide_menu(self, request, pk):
        try:
            mn = Menu.objects.get(pk=pk)
            mn.trang_thai = not mn.trang_thai
            mn.save()
        except Menu.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        return Response(data=MenuSerializer(mn, context={'request': request}).data, status=status.HTTP_200_OK)

    @action(methods=['get'], detail=True, url_path='list-monan', url_name='list-monan')
    def list_monan(self, request, pk):
        # Lấy đối tượng Menu hoặc trả về 404 nếu không tìm thấy
        menu = get_object_or_404(Menu, pk=pk)

        # Lấy danh sách ChiTietMenu của Menu
        chitiet_menu_list = MenuDetailsSerializer.objects.filter(menu=menu)

        monan_list = [chitiet.mon_an for chitiet in chitiet_menu_list]

        # Serialize danh sách MonAn
        serializer = DishSerializer(monan_list, many=True, context={'request': request})

        return Response(data=serializer.data, status=status.HTTP_200_OK)


class TaiKhoanViewSet(viewsets.ViewSet,
                      generics.ListAPIView,
                      generics.CreateAPIView,
                      generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    @action(methods=['get'], detail=True, url_path='monans', url_name='monans')
    def list_MonAn_of_TaiKhoan(self, request, *args, **kwargs):
        tai_khoan_id = kwargs.get('pk')

        try:
            tai_khoan = User.objects.get(pk=tai_khoan_id)
            monans = Dish.objects.filter(nguoi_dung=tai_khoan)
            serializer = DishSerializer(monans, many=True)
            return Response(serializer.data)
        except User.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    @action(methods=['get'], detail=True, url_path='menus', url_name='menus')
    def list_Menu_of_TaiKhoan(self, request, *args, **kwargs):
        tai_khoan_id = kwargs.get('pk')
        try:
            tai_khoan = User.objects.get(pk=tai_khoan_id)
            menus = Menu.objects.filter(nguoi_dung=tai_khoan)
            serializer = MenuSerializer(menus, many=True)
            return Response(serializer.data)
        except User.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)


class LoaiTaiKhoanViewSet(viewsets.ModelViewSet):
    queryset = Account.objects.all()
    serializer_class = AccountSerializer


class ThemMonAnViewSet(viewsets.ModelViewSet):
    queryset = Dish.objects.all()
    serializer_class = AddDishSerializer


class BinhLuanViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer


class TraLoiBinhLuanViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = ReplyToCommentsSerializer


class HoaDonViewSet(viewsets.ModelViewSet):
    queryset = Bill.objects.all()
    serializer_class = BillSerializer


class ChiTietHoaDonViewset(viewsets.ModelViewSet):
    queryset = BillDetails.objects.all()
    serializer_class = BillDetailsSerializer


def chatBot(request):
    user = request.user
    botchat = BotChat(user)
    messages = botchat.receive_message()
    return render(request, "chat.html", {
        "user": user,
        "botchat": botchat,
        "messages": messages,
    })


# Create your views here.
def hello(request):
    template = loader.get_template('index.html')
    return HttpResponse(template.render())


@csrf_exempt
def chat(request):
    if request.method == 'POST':
        user = get_user(request)
        message = request.POST['message']

        # Lưu tin nhắn vào database
        chat_bot = ChatbotModel.objects.create(
            question=user.username,
            answer=message,
        )

        # Trả về tin nhắn phản hồi
        return HttpResponse(chat_bot.conversation)

    return render(request, 'chat.html')