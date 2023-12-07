from django.core.mail import send_mail, mail_admins, BadHeaderError
from django.shortcuts import render

def say_hello(request):
    try:
        send_mail('subject', 'message', 'dinidutharuka@gmail.com', ['dinidutharuka7779@gmail.com'])
    except BadHeaderError:
        pass
    return render(request, 'hello.html', {'name':'Dinindu'})
