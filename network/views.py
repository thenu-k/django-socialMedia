from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from .models import *
import json
from django.core import serializers
from .helpers import *

def index(request):
    #Finding which posts the user needs
    firstPostCount = int(request.GET.get('first', '0'))
    lastPostCount = int(request.GET.get('last', '10'))
    #Getting the required posts
    postObjects = Post.objects.filter().order_by('-dateCreated')[firstPostCount:lastPostCount]
    # Getting like data
    likeExtrapolator(request, postObjects)
    payload = {
        'postObjects': postObjects
    }
    return render(request, "network/index.html", payload)


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "network/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "network/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")


def test(request):
    userObject = User.objects.get(username='admin')
    posts = userObject.postCreatedByUser.all()
    print(posts)
    return JsonResponse({'result': ''})

# Rendering create post
def renderCreatePost(request):
    return render(request, 'network/CreatePost/createpost.html')

# Submit post
@csrf_exempt
def submitPost(request):
    if request.user.is_authenticated:
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)
        createdByUserObject = User.objects.get(id=request.user.id)
        Post(content=body['content'], userKey=createdByUserObject).save()
        return JsonResponse({'success': 'true'})
    
# Rendering account page
def renderAccountPage(request, userID):
    #Finding which posts the user needs
    firstPostCount = int(request.GET.get('first', '0'))
    lastPostCount = int(request.GET.get('last', '10'))
    #Getting the required posts
    requestedUser = User.objects.get(id=userID)
    postObjects = requestedUser.postCreatedByUser.all().order_by('-dateCreated')[firstPostCount:lastPostCount]
    # Checking auth level
    if(request.user.is_authenticated):
        # Request created by
        currentUserObject = User.objects.get(id=request.user.id)
        #Check whether user follows account
        userFollows = False
        if Follow.objects.filter(createdByUserKey=currentUserObject, followingUserKey=requestedUser).exists():
            userFollows = True
        payload = {
            'postObjects': postObjects,
            'requestedUser': requestedUser,
            'usersEqual': True if (requestedUser.id==currentUserObject.id) else False,
            'userFollows': userFollows
        }
    else:
        payload = {
            'postObjects': postObjects,
            'requestedUser': requestedUser
        }
    return render(request, 'network/Account/account.html', payload)

# Create new follow
@csrf_exempt
def newFollow(request):
    if request.user.is_authenticated:   
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)
        currentUserObject = User.objects.get(id=request.user.id)
        requestedUserObject = User.objects.get(id=body['requestedUserID'])
        # check whether a follow exists
        if Follow.objects.filter(createdByUserKey=currentUserObject, followingUserKey=requestedUserObject).exists():
            payload = {'created': False}
        else: 
            newFollowObject = Follow(createdByUserKey=currentUserObject, followingUserKey=requestedUserObject)
            newFollowObject.save()
            payload = {'created': True}
        return JsonResponse(payload)

# Remove follow
@csrf_exempt
def removeFollow(request):
    if request.user.is_authenticated:   
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)
        currentUserObject = User.objects.get(id=request.user.id)
        requestedUserObject = User.objects.get(id=body['requestedUserID'])
        # check whether a follow exists
        if Follow.objects.filter(createdByUserKey=currentUserObject, followingUserKey=requestedUserObject).exists():
            followObject = Follow.objects.get(createdByUserKey=currentUserObject, followingUserKey=requestedUserObject)
            followObject.delete()
            payload = {'removed': True}
        else: 
            payload = {'removed': False}
        return JsonResponse(payload)
    
# Render following user's post page
def renderFollowingUserPosts(request):
    if(request.user.is_authenticated):
        # Getting posts
        userObject = User.objects.get(id = request.user.id)
        followingUserObjects  = userObject.followCreatedByUser.all()
        postObjects = Post.objects.filter(userKey__in=followingUserObjects.values('followingUserKey')).order_by('-dateCreated')
        payload = {
            'postObjects': postObjects
        }
        return render(request, 'network/Following/following.html', payload)