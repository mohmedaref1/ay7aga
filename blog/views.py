from django.core.files.storage import default_storage
from django.shortcuts import render
from django.http import HttpResponse
from blog.models import Massages
from base64 import urlsafe_b64decode
from django.contrib.sites.shortcuts import get_current_site
from tokenize import generate_tokens
from django.shortcuts import redirect, render
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.conf import settings
import django.core.mail
from django.template.loader import render_to_string
from django.contrib.auth import authenticate, login, logout
from . tokens import generate_token
import django.utils.encoding

# Create your views here.

from django.core.files.storage import FileSystemStorage
from django.http import JsonResponse




def loginn(request):

   if not request.user.is_authenticated:

        if request.method=="POST":

            username = request.POST['username']

            password1 = request.POST['pass1']


            us = authenticate(request,username=username, password=password1)


            if us is not None:


                login(request, us)


                u = User.objects.get(username=username)


                return redirect( 'index')
            else:

                messages.error(request, 'ataced mn al username aw elpass')
        return render(request, 'login.html')
   else :
       return redirect('index')


def logoutt(request):
    logout(request)
    messages.success(request, 'you are logged out')
    return redirect('status')


def status(request):
    return render(request, 'status.html')


def reg(request):
    if not  request.user.is_authenticated:
        if request.method == 'POST':
            username = request.POST['username']
            fname = request.POST['fname']
            lname = request.POST['lname']
            email1 = request.POST['email']
            password1 = request.POST['pass1']
            password2 = request.POST['pass2']
            if User.objects.filter(username=username):
                messages.error(request, 'The user is already exist')
                return redirect('status')
            elif User.objects.filter(email=email1):
                messages.error(request, 'The Email is already Regesterid')
                return redirect('status')
            elif len(username) > 10:
                messages.error(request, 'the user is len than 10 characters')
                return redirect('status')
            elif password1 != password2:
                messages.error(request, 'Passwords dont match')
                return redirect('status')
            elif not username.isalnum():
                messages.error(request, 'must be alphabetic')
                return redirect('status')
            else:
                myuser = User.objects.create_user(username, email1, password1)
                myuser.frist_name = fname
                myuser.last_name = lname
                myuser.is_active = True

                myuser.save()
                return redirect('loginn')

        return render(request, 'reg.html')
    else :
        return redirect('index')


"""   messages.success(request, "your acc is created")
            smail = django.core.mail.EmailMessage(
                'hi',
                'THIS IS Auto Mail FROM Eslam Qadri',
                'ekadryahmed@gmail.com',
                [email1]

            )

            smail.send(fail_silently=False)

            current_site = get_current_site(request)
        email_subject = "Confirm your Email @ GFG - Django Login!!"
        message2 = render_to_string('email_confirmation.html', {

            'name': myuser.first_name,
            'domain': current_site.domain,
            'uid': django.utils.encoding.urlsafe_base64_encode(django.utils.encoding.force_bytes(myuser.pk)),
            'token': generate_token.make_token(myuser)
        })
        email = django.core.mail.EmailMessagee(
            email_subject,
            message2,
            settings.EMAIL_HOST_USER,
            [myuser.email],
        )
        email.fail_silently = True
        email.send()
        return redirect('status')
"""

def activate(request, uidb64, token):
    try:
        uid = django.utils.encoding.force_text(urlsafe_b64decode(uidb64))
        myuser = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        myuser = None

    if myuser is not None and generate_tokens.check_token(myuser, token):
        myuser.is_active = True
        # user.profile.signup_confirmation = True
        myuser.save()
        login(request, myuser)
        messages.success(request, "Your Account has been activated!!")
        return redirect('signin')
    else:
        return render(request, 'activation_failed.html')

#################################################################################

list_to_train =[
    "hi",
    "hi,there",
    "What's your name?",
    "I am just a chatbot",
    "What's your fav food",
    "I like nothing",
    "what's your fav sport",
    "I like all sports",
    "do you have children",
    "no"
]

d = {"hi":
     "hi,there",
     "What's your name?":
     "I am just a chatbot",
     "What's your fav food":
     "I like nothing",
     "what's your fav sport":
     "I like all sports",
     "do you have children":
     "no"
     }

#list_trainer = ListTrainer(bot)
#list_trainer.train(list_to_train)

# chatterbotCorpusTrainer = ChatterBotCorpusTrainer(bot)

# chatterbotCorpusTrainer.train('chatterbot.corpus.english')


@login_required
def index(request):
    

    chats=Massages.objects.filter(user=request.user).order_by('pk')
    return render(request, 'index.html',{"chats":chats})


@login_required()
def getResponse(request):
    if request.method == 'POST':
        user_message = request.POST.get('userMessage')
        file = request.FILES.get('file')

        # Save the file to the media folder
        if file:
            filename = default_storage.save(file.name, file)
            file_url = request.scheme + '://' + \
                request.get_host() + settings.MEDIA_URL + filename
            user_message = file_url
        else:
            file_url = None

        # Process the user message and generate a response
        chat_response = d.get(user_message, "didn't learn that yet")

        # Save the message and response to the database
        Massages.objects.create(massages=user_message,
                                user=request.user, replay=chat_response)

        # Prepare the data to send back to the client
        data = {
            "file_link": file_url,
            "response": chat_response
        }

        return JsonResponse(data)

    return JsonResponse({"error": "Invalid request"})
