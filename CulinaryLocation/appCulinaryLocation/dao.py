from django.db.models import Count, F
from .models import User, Account

def countUser():

    return User.objects.filter(Confirm=1).annotate(total=Count('id')).values('id', 'name', 'confirm_id')
