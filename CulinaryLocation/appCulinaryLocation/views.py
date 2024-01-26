from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from .models import Member, ChatbotModel, BotChat
from firebase_admin.auth import get_user
#from botchat import Botchat

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