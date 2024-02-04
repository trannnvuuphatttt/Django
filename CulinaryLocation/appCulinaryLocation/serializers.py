from dataclasses import fields
from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from .models import User, ShipmentDetails, Menu, MenuDetails, Bill, Dish, Account, Confirm, Address, Food, Time, SaleTime, BillDetails, Review, Follow, Comment
from django.contrib.auth.hashers import make_password


class InformationUserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username", "phone", "account_id", "name", "avatar"]


class TimeSerializer(ModelSerializer):
    class Meta:
        model = Time
        fields = ["id", "session", "startTime", "endTime"]


class SaleTimeSerializer(ModelSerializer):
    class Meta:
        model = SaleTime
        fields = ["id", "dish_id", "menu_id", "time_id"]


class ShipmentDetailsSerializer(ModelSerializer):
    addressType = serializers.PrimaryKeyRelatedField(queryset=Address.objects.all())

    class Meta:
        model = ShipmentDetails
        fields = ["id", "deliveryAddress", "name", "address_id", "user_id"]


class UserSerializer(ModelSerializer):
    accountType = serializers.PrimaryKeyRelatedField(queryset=Account.objects.all())

    genderSelect = (
        (0, 'Nam'),
        (1, 'Nữ')
    )

    gender = serializers.ChoiceField(choices=genderSelect)

    class Meta:
        model = User
        fields = ['id',
                  'name',
                  'email',
                  'phone',
                  'username',
                  'password',
                  'avatar',
                  'gender',
                  'date',
                  'confirm_id',
                  'account_id',
                  'longitude',
                  'latitude']

    def to_representation(self, instance):
        representation = super().to_representation(instance)

        if representation.get('avatar'):
            representation['avatar'] = "https://res.cloudinary.com/dpp5kyfae/" + representation['avatar']

        return representation

    def create(self, validated_data):
        confirmDefault = Confirm.objects.get(pk=1)
        validated_data['Xác Nhận'] = confirmDefault.id

        password = validated_data.pop('password', None)

        user = User.objects.create(**validated_data)
        if password:
            user.password = make_password(password)
            user.save()
        return user


class ShopSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ['name', 'email', 'phone', 'avatar', 'longitude', 'latitude']


class DishSerializer(ModelSerializer):
    class Meta:
        model = Dish
        fields = ["id", "name", "price", "describe", "user_id", "food_id", "quantity", "image"]

    def to_representation(self, instance):
        representation = super().to_representation(instance)

        if representation.get('image'):
            representation['image'] = "https://res.cloudinary.com/dpp5kyfae/" + representation['image']

        return representation

    def update(self, instance, validated_data):
        instance.quantity = validated_data.get("quantity", instance.so_luong)
        instance.save()
        return instance


class FoodSerializer(ModelSerializer):
    class Meta:
        model = Food
        fields = ["id", "name"]


class MenuSerializer(ModelSerializer):
    class Meta:
        model = Menu
        fields = ["id", "title", "user_id", "dateCreated", "status", "image"]

    def to_representation(self, instance):
        representation = super().to_representation(instance)

        if representation.get('image'):
            representation['image'] = "https://res.cloudinary.com/dpp5kyfae/" + representation['image']

        return representation


class AccountSerializer(ModelSerializer):
    userSet = UserSerializer(many=True)

    class Meta:
        model = Account
        fields = ["id", "name", "userSet"]


class AddDishSerializer(ModelSerializer):
    food = serializers.PrimaryKeyRelatedField(queryset=Food.objects.all())

    class Meta:
        model = Dish
        fields = ["name", "price", "describe", "image",
                  "quantity", "food_id"]

    def create(self, validated_data):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            try:
                tai_khoan = User.objects.get(username=request.user.username)
                validated_data['nguoi_dung_id'] = tai_khoan.id
                mon_an = Dish.objects.create(**validated_data)
                return mon_an
            except User.DoesNotExist:
                raise serializers.ValidationError("Không thể tạo món ăn")

        raise serializers.ValidationError("Vui lòng đăng nhập để thêm món ăn")


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ["noi_dung"]

    def create(self, validated_data):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            try:
                tai_khoan = User.objects.get(username=request.user.username)

                validated_data['nguoi_dung_id'] = tai_khoan.id
                binh_luan = Review.objects.create(**validated_data)
                return binh_luan
            except User.DoesNotExist:
                raise serializers.ValidationError("Không the viết bình luận ")

        raise serializers.ValidationError("Vui lòng đăng nhập để viết bình luận")


class ReplyToCommentsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ["noi_dung"]

    def create(self, validated_data):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            try:
                binh_luan_cha = Review.objects.all()
                validated_data['binh_luan_cha_id'] = binh_luan_cha
                binh_luan = Review.objects.create(**validated_data)
                return binh_luan
            except Review.DoesNotExist:
                raise serializers.ValidationError("Không the viết bình luận ")

        raise serializers.ValidationError("Vui lòng đăng nhập để sử dụng")


# class LoginSerializer(serializers.Serializer):
#     username = serializers.CharField()
#     password = serializers.CharField(write_only=True)


class MenuDetailsSerializer(serializers.ModelSerializer):
    mon_an = serializers.PrimaryKeyRelatedField(queryset=Dish.objects.all())

    class Meta:
        model = MenuDetails
        fields = ["id", "menu", "dish_id", "quantity"]


class BillSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bill
        fields = ["id", "user", "dateCreated"]


class BillDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = BillDetails
        fields = ["id", "bill_id", "dish_id"]


class FollowSerializer(serializers.ModelSerializer):
    class Meta:
        model = Follow
        fields = ["id", "shop_id", "user_id"]

    def create(self, validated_data):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            try:
                tai_khoan = User.objects.get(username=request.user.username)
                validated_data['nguoi_dung_id'] = tai_khoan.id
                mon_an = Follow.objects.create(**validated_data)
                return mon_an
            except User.DoesNotExist:
                raise serializers.ValidationError("Không thể tạo món ăn")

        raise serializers.ValidationError("Vui lòng đăng nhập để thêm món ăn")


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ["id", "diem_so", "cua_hang", "mon_an", "nguoi_dung"]
