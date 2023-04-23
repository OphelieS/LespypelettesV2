import django
from django.shortcuts import render

from django.urls import path
from . import views
from .forms import SignUpForm, SignInForm
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
import speech_recognition as sr
urlpatterns = [

]


def index(request):
    context = {'user': request.user}
    return render(request, 'reading/index.html', context)

def home(request):
    return render(request,'home.html')



from django.contrib.auth import login as auth_login

def login(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        user = authenticate(request, email=email, password=password)
        if user is not None:
            auth_login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Invalid email or password.')
    return render(request, 'login.html')

def logout(request):
    return render(request,'logout.html')

def compte(request):
    return render(request,'compte.html')


from django.urls import reverse

def accueil(request):
    return render(request, 'accueil.html')

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

@login_required
@csrf_exempt
def update_user_stars(request):
    if request.method == 'POST':
        new_stars = request.POST.get('newStars')
        if new_stars is not None:
            try:
                new_stars = int(new_stars)
                user = request.user
                user.stars = new_stars
                user.save()
                return JsonResponse({'status': 'success', 'stars': new_stars})
            except ValueError:
                return JsonResponse({'status': 'error', 'message': "Valeur d'étoiles invalide."}, status=400)
        else:
            return JsonResponse({'status': 'error', 'message': "Les données requises n'ont pas été fournies."}, status=400)
    else:
        return JsonResponse({'status': 'error', 'message': 'Méthode de requête non autorisée.'}, status=405)

# Create your views here.
import speech_recognition as sr




#from .models import Progress

import random



import random

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, HttpResponse
import speech_recognition as sr

from .models import Sound

LEVEL_1_SOUNDS = ['les', 'ton', 'tes', 'rat', 'son', 'cri', 'bal', 'ses', 'moi', 'don','la', 'ma', 'tu', 'il', 'si', 'lu']
LEVEL_2_SOUNDS = ['balle', 'chat', 'mois', 'dans', 'donc', 'très', 'mais', 'belle', 'mars', 'lire']
LEVEL_3_SOUNDS = ['joue', 'terre','vert','mot', 'pour', 'base', 'pomme','clé', 'fête', 'cube']

@login_required(login_url='/accounts/login/')
def game(request):
    print('la def game est utilisée')
    result = request.POST.get("result")

    # Get the current user's progress in this level
    user = request.user
    level = user.level
    
    # Update user stars and level
    new_stars = int(request.POST.get('new_stars', 0))
    print('newstars:', new_stars)
    user.stars += new_stars
    if user.stars >= 10 and user.level < 10:
        user.level += 1
    user.save()

    if level == 1:
        sound_list = LEVEL_1_SOUNDS
        chosen_word = random.choice(sound_list)
    elif level == 2:
        sound_list = LEVEL_2_SOUNDS
        chosen_word = random.choice(sound_list)
    elif level == 3:
        sound_list = LEVEL_3_SOUNDS
        chosen_word = random.choice(sound_list)
    else:
        # Handle the case where the user's level is not recognized
        return HttpResponse('Invalid user level')

    # voir si l utilisateur peuvent passer au niveau supérieur
    can_unlock_next_level = user.stars >= 10 and user.level < 10
    
    # Regarder si l utilisateur à déjà lu ce son
    if request.method == 'POST' and 'chosen_word' in request.POST:
        chosen_word = request.POST['chosen_word']
        if chosen_word in sound_list:
            # user.stars += 1
            # user.save()
            print ('user save ----------------------------')
            # Use PyAudio and SpeechRecognition pour reconnaitre la voix
            r = sr.Recognizer()
            with sr.Microphone() as source:
                audio = r.listen(source)
            try:
                # Use Google Speech Recognition to transcribe the user's voice
                text = r.recognize_google(audio)
                
                return render(request, 'reading/game.html',  {'user': user, 'result': result,'chosen_word': chosen_word, 'correct': True, 'can_unlock_next_level': can_unlock_next_level})
            except sr.UnknownValueError:
                pass
    print ('user save end----------------------------', user.stars)  
    return render(request, 'reading/game.html', {'user': user, 'result': result,'chosen_word': chosen_word,  'can_unlock_next_level': can_unlock_next_level})


def get_new_word(request):
    user = request.user
    level = user.level
    
    if level == 1:
        sound_list = LEVEL_1_SOUNDS
    elif level == 2:
        sound_list = LEVEL_2_SOUNDS
    elif level == 3:
        sound_list = LEVEL_3_SOUNDS
    else:
        return HttpResponse('Invalid user level')

    chosen_word = random.choice(sound_list)
    return JsonResponse({'new_word': chosen_word})


from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from django.http import JsonResponse




from django.http import JsonResponse

def update_stars_and_get_new_word(request):
    
    if request.method == 'POST':
        #new_stars = int(request.POST.get('new_stars', 0))

        # Mettre à jour les étoiles pour l'utilisateur actuel
        user.stars = user.stars + 1
        if user.stars >= 10 :
            user.level += 1
            user.stars = 0
        user.save()

        chosen_word = random.choice(sound_list)
            

        response_data = {
            "audio-text": chosen_word,
            "user.stars": user.stars,
            "user.level": user.level,
        }

        return JsonResponse(response_data)





import cv2
import numpy as np
from tensorflow.keras.models import load_model, model_from_json
from tensorflow.keras.preprocessing.image import img_to_array
from django.http import JsonResponse

model = model_from_json(open("reading/model.json", "r").read())
model.load_weights('reading/weights_min_loss.hdf5')
face_haar_cascade = cv2.CascadeClassifier('reading/haarcascade_frontalface_default.xml')
cap = cv2.VideoCapture(0)
from django.views.decorators.csrf import csrf_exempt
import collections

from PIL import Image
import io
import base64

@csrf_exempt
def detect_emotion(request):
    if request.method == 'POST':
        # Récupérer l'image base64 depuis la requête
        image_base64 = request.POST.get('image')
        image_data = base64.b64decode(image_base64.split(',')[1])

        # Convertir l'image en PIL Image et ensuite en numpy array
        image = Image.open(io.BytesIO(image_data))
        frame = np.array(image)

        emotion_prediction = None
        print("la def detect de views est appelée")
        
        emotion_list = []

        height, width, _ = frame.shape
        gray_image = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_haar_cascade.detectMultiScale(gray_image)
        most_common_emotion = None 
        try:
            for (x, y, w, h) in faces:
                roi_gray = gray_image[y - 5:y + h + 5, x - 5:x + w + 5]
                roi_gray = cv2.resize(roi_gray, (48, 48))
                image_pixels = img_to_array(roi_gray)
                image_pixels = np.expand_dims(image_pixels, axis=0)
                image_pixels /= 255
                predictions = model.predict(image_pixels)
                max_index = np.argmax(predictions[0])
                emotion_detection = ('en colère', 'dégoût', 'peur', 'heureux', 'triste', 'surprise', 'neutre')
                emotion_prediction = emotion_detection[max_index]
                
                emotion_list.append(emotion_prediction)
                
                
                counter = collections.Counter(emotion_list)
                
                most_common_emotion = counter.most_common(1)[0][0]
                print( most_common_emotion)
        except:
            pass

        response_data = {'emotion': most_common_emotion}
        return JsonResponse(response_data)
        
    else:
        return JsonResponse({'error': 'Méthode non autorisée.'})





@login_required(login_url='/login/')
def get_random_word(request):
    user = request.user
    level = user.level
    if level == 1:
        word_list = LEVEL_1_SOUNDS
    elif level == 2:
        word_list = LEVEL_2_SOUNDS
    elif level == 3:
        word_list = LEVEL_3_SOUNDS
    else:
        word_list = []

    chosen_word = random.choice(word_list) if word_list else ''
    return JsonResponse({'chosen_word': chosen_word})


from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from .forms import LoginForm



# vue du formulaire d'inscription/authentification
from django.shortcuts import render, redirect
from reading.forms import SignUpForm, SignInForm, LoginForm
from reading.models import CustomUser


# vue d'authentification qui utilise le formulaire d'authentification pour vérifier les informations d'identification de l'utilisateur et redirige l'utilisateur vers une page de confirmation de connexion
from django.contrib.auth import authenticate, login


def signin(request):
    if request.method == 'POST':
        form = SigninForm(request, request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('signin_done')
    else:
        form = SigninForm()

    return render(request, 'compte.html', {'form': form})


# Vue de confirmation d'inscription et de connexion pour rediriger les utilisateurs vers une page de bienvenue après une inscription ou une connexion réussie
def signup_done(request):
    return render(request, 'reading/signup_done.html')

def signin_done(request):
    return render(request, 'reading/signin_done.html')

from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import SignUpForm

from django.urls import reverse
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login

from django.contrib.auth.backends import ModelBackend
from .forms import CustomUserCreationForm
ModelBackend = 'django.contrib.auth.backends.ModelBackend'



from django.contrib.auth.decorators import login_required

@login_required
def login_view(request):
    username = request.user.username
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(request, email=email, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Invalid email or password!')
    return render(request, 'reading/login_view.html', {'username': username})

def logout_view(request):
    logout(request)
    return redirect('home')



from django.shortcuts import render
from django.contrib.auth.decorators import login_required


@login_required
def user_profile(request):
    user = request.user
    
    context = {'username':user.username, 'level': user.level, 'stars' :user.stars}
    return render(request, 'reading/user_profile.html', context)


from django.urls import reverse_lazy
from django.views.generic import RedirectView
from django.contrib.auth.views import LoginView


class CustomLoginView(LoginView):
    template_name = 'account/login.html'
    success_url = reverse_lazy('reading:game')

    def form_valid(self, form):
        response = super().form_valid(form)
        if self.request.user.is_authenticated:
            return RedirectView.as_view(url=self.success_url)(self.request)
        else:
            return response


def signup(request):
    return redirect(reverse('singin_done'))


from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
import json



@login_required
def update_stars(request):
    print ('update_stars appelé________________________')
    if request.method == 'POST':
        print ('dans le if ok °°°°°°°°°°°°°°°°°°')
        #data = json.loads(request.user)
        #print ('dans le data ok °°°°°°°°°°°°°°°°°°')
        user = request.user
        user.stars = request.user.stars +1
        print ('dans le user star ok °°°°°°°°°°°°°°°°°°',  )
        user.level = request.user.level
        ('dans le user level ok °°°°°°°°°°°°°°°°°°',  )
        user.save()
        print ('user sauvé________________________', user.stars, user.level)
        return JsonResponse({'status': 'success'})
    else:
        return JsonResponse({'status': 'error', 'message': 'Invalid request method'})
        #return redirect('reading:stars_updated')
    #else:
        #return HttpResponseNotAllowed(['POST'])


@login_required
@csrf_exempt
def update_user_stars(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        user = request.user
        user.stars = data['stars']
        user.level = data['level']
        user.save()
        return JsonResponse({'status': 'success'})
    else:
        return JsonResponse({'status': 'error', 'message': 'Invalid request method'})


