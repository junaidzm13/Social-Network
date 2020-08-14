from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
import time
import json
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.core.paginator import Paginator

from .models import User, Comment, Follower, Post, Like


def index(request):
    
    if request.method == "POST":
        content = request.POST["content"]
        user = request.user
        timestamp = time.strftime("%b %d %Y, %I:%M %p")
        post = Post(user=user, content=content,
                    timestamp=timestamp, num_likes=0)
        post.save()
        
    # if not logged in
    if not request.user.is_authenticated:
        paginator = Paginator(Post.objects.all().order_by('-timestamp'), 10)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        
        post_to_liked = {}
        for item in page_obj:
            post_to_liked[item] = False
        return render(request, "network/index.html", {
            "user": None, "liked": post_to_liked, "page_obj": page_obj
        })
    paginator = Paginator(Post.objects.all().order_by('-timestamp'), 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    post_to_liked = {}
    for item in page_obj:
        if item.likes.filter(user=request.user):
            #print("if")
            post_to_liked[item]=True
        else:
            #print("else")
            post_to_liked[item] = False
    return render(request, "network/index.html", {"user": request.user, "liked": post_to_liked, 'page_obj': page_obj
                                                  })


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
        username = request.POST.get("username")
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

    
def profile(request, username):
    
    if request.method == "POST":
        follower = request.user
        user = User.objects.get(username=username)                
        if "follow" in request.POST:
            new_follower = Follower(user=user, follower=follower)
            new_follower.save()
            for post in user.posts.all():
                followed_post = Fpost(user=follower, post=post)
                followed_post.save()
        elif "unfollow" in request.POST:
            follower_ = Follower.objects.get(user=user, follower=follower)
            follower.delete()
        elif 'content' in request.POST:
            content = request.POST["content"]
            user = request.user
            timestamp = time.strftime("%b %d %Y, %I:%M %p")
            post = Post(user=user, content=content,
                        timestamp=timestamp, num_likes=0)
            post.save()            

    user = User.objects.get(username=username)
    post = user.posts.all().order_by('-timestamp')

    no_of_followers = user.followers.all().count()
    no_of_followings = user.following.all().count()
    if not request.user.is_authenticated:
        paginator = Paginator(post.order_by('-timestamp'), 10)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)        
        post_to_liked = {}
        for item in page_obj:
            post_to_liked[item] = False
            
        return render(request, "network/profile.html", {
            "profile": user, "liked": post_to_liked, "ownProfile": False,
            "followers": no_of_followers, "following": no_of_followings,
            "isfollowing": False, "page_obj": page_obj
        })
    
    isfollowing = True
    if request.user.username == username:
        ownprofile = True
    else:
        ownprofile = False
        if request.user.following.filter(user=user):
            isfollowing = True
        else:
            isfollowing = False
    paginator = Paginator(post.order_by('-timestamp'), 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    post_to_liked = {}
    for item in page_obj:
        if item.likes.filter(user=request.user):
            #print("if")
            post_to_liked[item] = True
        else:
            #print("else")
            post_to_liked[item] = False
            
    return render(request, "network/profile.html", {
        "profile": user, "liked": post_to_liked, "ownProfile": ownprofile,
        "followers": no_of_followers, "following": no_of_followings,
        "isfollowing": isfollowing, "page_obj": page_obj
    })


@login_required
def following(request):
    user = request.user
    following = user.following.all()
    all_followed = []
    for f_user in following:
        for post in f_user.user.posts.all():
            all_followed.append(post)
    
    all_followed.sort(key=lambda post: post.timestamp, reverse=True)
    
    paginator = Paginator(all_followed, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    post_to_liked = {}
    for item in page_obj:
        if item.likes.filter(user=request.user):
            post_to_liked[item] = True
        else:
            post_to_liked[item] = False

    return render(request, "network/following.html", {
        "liked": post_to_liked, "page_obj": page_obj
    })

@csrf_exempt
@login_required
def edit(request):

    # Editing a post must be via POST
    if request.method != "POST":
        return JsonResponse({"error": "POST request required."}, status=400)
    print("edit")
    data = json.loads(request.body)
    print(data)
    content = data.get("new_content", "")
    post_id = data.get("id")
    post = Post.objects.get(id=post_id)
    post.content = content
    post.save()
    return HttpResponse(status=204)
    #return JsonResponse({"message": "Post edited successfully."}, status=201)


@csrf_exempt
@login_required
def post(request, post_id):

    try:
        post = Post.objects.get(pk=post_id)
    except Post.DoesNotExist:
        return JsonResponse({"error": "Post not found"}, status=404)

    if request.method == "GET":
        return JsonResponse(post.serialize())
    
    elif request.method == "PUT":
        data = json.loads(request.body)
        if data.get("color") == 'red':
            like = Like(post=post, user=request.user)
            print("liked saved")
            post.num_likes = post.num_likes + 1
            like.save()
        if data.get("color") == 'white':
            like = Like.objects.get(user=request.user, post=post)
            like.delete()
            post.num_likes = post.num_likes - 1
        post.save()
        return HttpResponse(status=204)
    else:
        return JsonResponse({
            "error": "GET or PUT request required."
        }, status=400)