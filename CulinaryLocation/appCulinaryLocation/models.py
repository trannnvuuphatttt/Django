from django.contrib.auth.models import AbstractUser
from django.db import models
from cloudinary.models import CloudinaryField

# Create your models here.


class Member(models.Model):
    firstname = models.CharField(max_length=255)
    lastname = models.CharField(max_length=255)
    phone = models.IntegerField(null=True)
    joined_date = models.DateField(null=True)


class Account(models.Model):
    name = models.CharField(max_length=50, null=False, blank=False)

    def __str__(self):
        return self.name


class Confirm(models.Model):
    name = models.CharField(max_length=50, null=False, blank=False)

    def __str__(self):
        return self.name


class User(AbstractUser):
    name = models.CharField(max_length=50, null=True, blank=True)
    username = models.CharField(max_length=50, null=False, blank=False, unique=True)
    password = models.CharField(max_length=200, null=False, blank=False)
    date = models.DateField(null=True, blank=True)
    email = models.EmailField(null=True, blank=True)
    phone = models.CharField(max_length=50, null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True, default=0)
    latitude = models.FloatField(null=True, blank=True, default=0)
    gender = models.BooleanField(default=False, null=True, blank=True)
    account_id = models.ForeignKey(Account, on_delete=models.PROTECT, null=True, blank=True)
    confirm_id = models.ForeignKey(Confirm, on_delete=models.PROTECT, null=True, blank=True)
    openTime = models.DateTimeField(null=True, blank=True)
    closingTime = models.DateTimeField(null=True, blank=True)
    avatar = models.ImageField(upload_to='uploads/%y/%m')

    def __str__(self):
        return self.username


class Address(models.Model):
    name = models.CharField(max_length=50, null=False, blank=False)

    def __str__(self):
        return self.name


class ShipmentDetails(models.Model):
    deliveryAddress = models.CharField(max_length=50, null=False, blank=False)
    address_id = models.ForeignKey(Address, on_delete=models.PROTECT, null=False, blank=False)
    user_id = models.ForeignKey(User, on_delete=models.PROTECT, null=False, blank=False)
    name = models.CharField(max_length=50, null=False, blank=False)

    def __str__(self):
        return self.name


class Search(models.Model):
    name = models.CharField(max_length=50, null=False, blank=False)
    nameOfFood = models.CharField(max_length=50, null=False, blank=False)
    nameOfTheStore = models.CharField(max_length=50, null=False, blank=False)
    user_id = models.ForeignKey(User, on_delete=models.PROTECT, null=False, blank=False)

    def __str__(self):
        return self.nameOfFood


class Comment(models.Model):
    content = models.CharField(max_length=50, null=False, blank=False)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, null=False, blank=False)
    commentFirst = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True)
    image = models.ImageField(upload_to='', null=True, blank=True)
    commentDish = models.ForeignKey('Dish', on_delete=models.CASCADE, null=True, blank=True)


    def __str__(self):
        return self.content


class Menu(models.Model):
    dateCreated = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=50, null=True, blank=True)
    dish_id = models.ManyToManyField('Dish', through='MenuDetails', related_name='menus')
    status = models.BooleanField(default=True)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    image = models.ImageField(upload_to='', null=True, blank=True)

    def __str__(self):
        return self.title


class MenuDetails(models.Model):
    menu = models.ForeignKey(Menu, on_delete=models.CASCADE, null=False, blank=False)
    dish_id = models.ForeignKey('Dish', on_delete=models.CASCADE, null=False, blank=False)
    quantity = models.IntegerField(null=False, blank=False, default=0)


class Food(models.Model):
    name = models.CharField(max_length=50, null=False, blank=False)

    def __str__(self):
        return self.name


class Time(models.Model):
    session = models.CharField(max_length=50, null=True, blank=True)
    startTime = models.TimeField()
    endTime = models.TimeField()
    dish_id = models.ManyToManyField('Dish', through='SaleTime', related_name='thoidiems')

    def __str__(self):
        return self.session


class SaleTime(models.Model):
    time_id = models.ForeignKey(Time, on_delete=models.CASCADE, null=False, blank=False)
    dish_id = models.ForeignKey('Dish', on_delete=models.CASCADE, null=True, blank=False)
    menu_id = models.ForeignKey(Menu, on_delete=models.CASCADE, null=True, blank=False)

    def __str__(self):
        return self.time_id


class Bill(models.Model):
    dateCreated = models.DateTimeField(auto_now_add=True)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, null=False, blank=False)
    dish_id = models.ManyToManyField('Dish', through='BillDetails', related_name='hoadons')

    def __str__(self):
        return self.dateCreated


class BillDetails(models.Model):
    bill_id = models.ForeignKey(Bill, on_delete=models.CASCADE, null=False, blank=False)
    dish_id = models.ForeignKey('Dish', on_delete=models.CASCADE, null=False, blank=False)

    def __str__(self):
        return self.bill_id


class Dish(models.Model):
    name = models.CharField(max_length=50, null=True, blank=True)
    price = models.IntegerField(null=True, blank=True)
    describe = models.CharField(max_length=50, null=True, blank=True)
    food_id = models.ForeignKey(Food, on_delete=models.CASCADE, null=True, blank=True)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    status = models.BooleanField(default=True)
    image = models.ImageField(upload_to='uploads/%y/%m')
    quantity = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return self.name


class Follow(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, null=False, blank=False,
                                   related_name='following_users')
    shop_id = models.ForeignKey(User, on_delete=models.CASCADE, null=False, blank=False,
                                 related_name='tracking_store')

    def __str__(self):
        return self.user_id


class Review(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, null=False, blank=False,
                                   related_name='user_reviews')
    shop_id = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True,
                                 related_name='shop_reviews')
    dish_id = models.ForeignKey(Dish, on_delete=models.CASCADE, null=True, blank=True)
    scores = models.IntegerField(null=False, blank=False)

    def __str__(self):
        return self.user_id


class Voucher(models.Model):
    code = models.CharField(max_length=50, null=False, blank=False)
    percent = models.DecimalField(max_digits=5, decimal_places=2)

    def __str__(self):
        return self.code


#python manage.py makemigrations


class ChatbotModel(models.Model):
    question = models.CharField(max_length=255)
    answer = models.TextField()

    def __str__(self):
        return self.question

from firebase_admin import firestore

class BotChat(object):

    def __init__(self, user):
        self.user = user

    def get_user_name(self):
        return self.user.username

    def get_user_id(self):
        return self.user.id

    def send_message(self, message):
        firestore.collection("messages").add({
            "sender_id": self.user.id,
            "message": message,
        })

    def receive_message(self):
        messages = firestore.collection("messages").where("sender_id", "!=", self.user.id).get()
        return [message.to_dict() for message in messages]
