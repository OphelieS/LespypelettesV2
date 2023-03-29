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

LEVEL_1_SOUNDS = ['ta', 'me', 'la', 'te', 'ma', 'tu', 'il', 'si', 'lu', 'ou', 'ça','do','fa','ré']
LEVEL_2_SOUNDS = ['les', 'ton', 'tes', 'rat', 'son', 'cri', 'bal', 'ses', 'moi', 'don']
LEVEL_3_SOUNDS = ['balle', 'chat', 'mois', 'dans', 'donc', 'très', 'mais', 'belle', 'mars', 'lire']

@login_required(login_url='/login/')
def game(request):
    result = request.POST.get("result")

    # # Détection d'émotions
    # cap = cv2.VideoCapture(0)
    # model = model_from_json(open("reading/model.json", "r").read())
    # model.load_weights('reading/weights_min_loss.hdf5')
    # face_haar_cascade = cv2.CascadeClassifier('reading/haarcascade_frontalface_default.xml')

    # predictions = []
    # while True:
    #     ret, frame = cap.read()
    #     gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    #     faces = face_haar_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5)
    #     for (x, y, w, h) in faces:
    #         roi_gray = gray[y:y+h, x:x+w]
    #         roi_gray = cv2.resize(roi_gray, (48, 48), interpolation=cv2.INTER_AREA)
    #         if np.sum([roi_gray]) != 0:
    #             roi = roi_gray.astype('float')/255.0
    #             roi = img_to_array(roi)
    #             roi = np.expand_dims(roi, axis=0)
    #             # Make predictions on the ROI
    #             preds = model.predict(roi)[0]
    #             emotion_detection = ('angry', 'disgust', 'fear', 'happy', 'sad', 'surprise', 'neutral')
    #             emotion_prediction = emotion_detection[np.argmax(preds)]
    #             predictions.append(emotion_prediction)

    #     # Affichage de la vidéo en temps réel
    #     ret, buffer = cv2.imencode('.jpg', frame)
    #     frame = buffer.tobytes()
    #     yield (b'--frame\r\n'
    #             b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

    # cap.release()
    # cv2.destroyAllWindows()

    # Get the current user's progress in this level
    user = request.user
    level = user.level
    
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
            # Use PyAudio and SpeechRecognition pour reconnaitre la voix
            r = sr.Recognizer()
            with sr.Microphone() as source:
                audio = r.listen(source)
            try:
                # Use Google Speech Recognition to transcribe the user's voice
                text = r.recognize_google(audio)
                if text.lower() == chosen_word:
                    # If the user read the sound correctly, give them a star
                    user.stars += 1
                    user.save()
                    if user.stars >= 10 and user.level < 10:
                        user.level += 1
                        user.stars = 0
                        user.save()
                        # Unlock the next level by adding a progress object
                    else:
                        user.save()
                else:
                    pass 
                return render(request, 'reading/game.html',  {'user': user, 'result': result,'chosen_word': chosen_word, 'correct': True, 'can_unlock_next_level': can_unlock_next_level})
            except sr.UnknownValueError:
                pass

    return render(request, 'reading/game.html', {'user': user, 'result': result,'chosen_word': chosen_word,  'can_unlock_next_level': can_unlock_next_level})

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages


@login_required
def update_stars(request):
    if request.method == 'POST':
        new_stars = request.POST.get('new_stars')
        user_id = request.user.id
        user = CustomUser.objects.get(id=user_id)
        user.update_stars(int(new_stars))
        return redirect('reading:game')
    else:
        return HttpResponseNotAllowed(['POST'])


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

@csrf_exempt
def detect_emotion():
    cap = cv2.VideoCapture(1)
    while cap.isOpened():
        res, frame = cap.read()
        height, width , channel = frame.shape#---------------------------------------------------------------------------
        # Creating an Overlay window to write prediction and cofidencesub_img = frame[0:int(height/6),0:int(width)]black_rect = np.ones(sub_img.shape, dtype=np.uint8)*0
        sub_img = frame[0:int(height / 6), 0:int(width)]
        black_rect = np.zeros(sub_img.shape, dtype=np.uint8)
        res = cv2.addWeighted(sub_img, 0.77, black_rect,0.23, 0)
        FONT = cv2.FONT_HERSHEY_SIMPLEX
        FONT_SCALE = 0.8
        FONT_THICKNESS = 2
        lable_color = (10, 10, 255)
        lable = "Emotion Detection "
        lable_dimension = cv2.getTextSize(lable,FONT ,FONT_SCALE,FONT_THICKNESS)[0]
        textX = int((res.shape[1] - lable_dimension[0]) / 2)
        textY = int((res.shape[0] + lable_dimension[1]) / 2)
        cv2.putText(res, lable, (textX,textY), FONT, FONT_SCALE, (0,0,0), FONT_THICKNESS)# prediction part --------------------------------------------------------------------------gray_image= cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_haar_cascade.detectMultiScale(gray_image )
        try:
            for (x,y, w, h) in faces:
                cv2.rectangle(frame, pt1 = (x,y),pt2 = (x+w, y+h), color = (255,0,0),thickness =  2)
                roi_gray = gray_image[y-5:y+h+5,x-5:x+w+5]
                roi_gray=cv2.resize(roi_gray,(48,48))
                image_pixels = img_to_array(roi_gray)
                image_pixels = np.expand_dims(image_pixels, axis = 0)
                image_pixels /= 255
                predictions = model.predict(image_pixels)
                max_index = np.argmax(predictions[0])
                emotion_detection = ('angry', 'disgust', 'fear', 'happy', 'sad', 'surprise', 'neutral')
                emotion_prediction = emotion_detection[max_index]
                cv2.putText(res, "Sentiment: {}".format(emotion_prediction), (0,textY+22+5), FONT,0.7, lable_color,2)
                lable_violation = 'Confidence: {}'.format(str(np.round(np.max(predictions[0])*100,1))+ "%")
                violation_text_dimension = cv2.getTextSize(lable_violation,FONT,FONT_SCALE,FONT_THICKNESS )[0]
                violation_x_axis = int(res.shape[1]- violation_text_dimension[0])
                cv2.putText(res, lable_violation, (violation_x_axis,textY+22+5), FONT,0.7, lable_color,2)
        except :
            pass
        frame[0:int(height/6),0:int(width)] = res
        cv2.imshow('frame', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            breakcap.release()
    cv2.destroyAllWindows
    response_data = {'emotion': emotion_prediction}
    return JsonResponse(response_data)


    # _,frame=cap.read()
    # height, width , channel = frame.shape
    # sub_img = frame[0:int(height/6),0:int(width)]

    # black_rect = np.ones(sub_img.shape, dtype=np.uint8)*0
    # res = cv2.addWeighted(sub_img, 0.77, black_rect,0.23, 0)
    # gray_image= cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    # faces = face_haar_cascade.detectMultiScale(gray_image )
    # try:
    #     for (x,y, w, h) in faces:
    #         cv2.rectangle(frame, pt1 = (x,y),pt2 = (x+w, y+h), color = (255,0,0),thickness =  2)
    #         roi_gray = gray_image[y-5:y+h+5,x-5:x+w+5]
    #         roi_gray=cv2.resize(roi_gray,(48,48))
    #         image_pixels = img_to_array(roi_gray)
    #         image_pixels = np.expand_dims(image_pixels, axis = 0)
    #         image_pixels /= 255
    #         predictions = model.predict(image_pixels)
    #         max_index = np.argmax(predictions[0])
    #         emotion_detection = ('angry', 'disgust', 'fear', 'happy', 'sad', 'surprise', 'neutral')
    #         emotion_prediction = emotion_detection[max_index]
    #         cv2.putText(res, "Sentiment: {}".format(emotion_prediction), (0,50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
    #         lable_violation = 'Confidence: {}'.format(str(np.round(np.max(predictions[0])*100,1))+ "%")
    #         violation_text_dimension = cv2.getTextSize(lable_violation,cv2.FONT_HERSHEY_SIMPLEX, 0.5, 2)[0]
    #         violation_x_axis = int(res.shape[1]- violation_text_dimension[0])
    #         cv2.putText(res, lable_violation, (violation_x_axis, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
    # except :
    #     pass
    # frame[0:int(height/6),0:int(width)] = res
    # _, jpeg_frame = cv2.imencode('.jpg', frame)
    # response = jpeg_frame.tobytes()
    # return response


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

"""def accounts_signup((request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)

        if form.is_valid():  # vérifie si le formulaire est valide 

            form.save()  # enregistre les données dans la base de données db.sqlite3

            username = form.cleaned_data['username']  # récupère le username du formulaire 
            password = form.cleaned_data['password1']  # récupère le password du formulaire

            user = authenticate(username=username, password=password)   # authentifie l'utilisateur avec les données entrées dans le formulaire

            login(request, user)   # connecte l'utilisateur à son compte

            return redirect('home')   # redirige l'utilisateur vers la page d'accueil

    else:    # si la méthode n'est pas POST alors affiche le formulaire de création de compte 

        form = UserCreationForm()

    context = {'form':form}   # envoie le formulaire à la page html pour l'afficher 

    return render(request, 'signup.html', context) """  # affiche la page signup avec le formulaire de création de compte 
    
#def login_view(request):   # fonction pour se connecter à son compte si celui-ci est déjà crée 

    #if request.method == 'POST':   # si la méthode est POST alors récupère les données entrés par l'utilisateur (email et password) et vérifie si ces données sont correctes et existent bien dans la base de donnée db.sqlite3

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



def user_profile(request):
    user = User.objects.get(pk=request.user.pk)
    return render(request, 'user_profile.html', {'user': user})

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