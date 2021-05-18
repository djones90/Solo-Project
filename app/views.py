from django.shortcuts import render, redirect
from . models import *
from django.contrib import messages
import bcrypt

def home(request):
    return render(request, 'login.html')

def register(request):
    if request.method == 'POST':
        # validate input 
        errors = User.objects.user_validator(request.POST)
        if len(errors) != 0:
            for key, value in errors.items():
                messages.error(request, value)
            return redirect('/')
        hashed_pw = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt()).decode()
        new_user = User.objects.create(
            first_name = request.POST['first_name'],
            last_name = request.POST['last_name'],
            email = request.POST['email'],
            password = hashed_pw,
        )
        request.session['logged_user'] = new_user.id
        return redirect('/success')
    return redirect('/')

def login(request):
    if request.method == 'POST':
        errors = User.objects.log_validator(request.POST)
        if len(errors) != 0:
            for key, value in errors.items():
                messages.error(request, value)
            return redirect('/')
        this_user = User.objects.get(email = request.POST['email'])
        request.session['logged_user'] = this_user.id
        return redirect('/success')
    return redirect('/')

def success(request):
    user = User.objects.get(id=request.session['logged_user'])
    context = {
        'logged_user' : User.objects.get(id=request.session['logged_user']),
        'all_posts' : Post.objects.all(),
        #'user_posts': Post.objects.all()
        #'recent_posts' : post.objects.order_by('-created_at')
    }
    return render(request, 'dashboard.html', context)

def logout(request):
    request.session.flush()
    return redirect('/')

def new(request):
    if 'logged_user' not in request.session:
        return redirect('/')

    user = User.objects.get(id=request.session['logged_user'])
    context = {
        'logged_user' : User.objects.get(id=request.session['logged_user']),
        'all_posts' : Post.objects.all(),
        #'recent_posts' : post.objects.order_by('-created_at') # change to recent_posts
    }
    
    return render(request, 'new_post.html', context)

def create(request):
#    if request.method == 'POST':
    if 'logged_user' not in request.session:
        messages.error(request, 'Please register or log in first!')
        return redirect('/')
    
    if request.method == 'POST':
        errors = Post.objects.post_validator(request.POST)
    
    if errors:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/new')
    
    user = User.objects.get(id=request.session['logged_user'])
    Post.objects.create(
        user = user,
        title = request.POST['title'],
        description = request.POST['description']
    )
    
    return redirect('/success')

def delete(request, post_id):
    to_delete = Post.objects.get(id=post_id)
    to_delete.delete()
    return redirect('/success')

def post_details(request, post_id):
    if 'logged_user' not in request.session:
        return redirect('/')
    
    user = User.objects.get(id=request.session['logged_user'])
    one_post = Post.objects.get(id=post_id)
    context = {
        'post': one_post,
        'user': user
    }
    
    return render(request, 'post_details.html', context)

def comment(request, post_id):
    if 'logged_user' not in request.session:
        return redirect('/')
    
    if request.method == "POST":
        errors = Comment.objects.comment_validator(request.POST)
        if len(errors) > 0:
            for key, value in errors.items():
                messages.error(request, value)
        
    else:
        poster = User.objects.get(id=request.session['user_id'])
        Comment.objects.create(comment=request.POST['comment'], poster=poster)
            
    user = User.objects.get(id=request.session['logged_user'])
    one_post = Post.objects.get(id=post_id)
    context = {
    'user': user,
    'post': one_post
}    
    return render(request, 'post_details.html', context)

def edit(request, post_id):
    if 'logged_user' not in request.session:
        return redirect('/')

    user = User.objects.get(id=request.session['logged_user'])
    one_post = Post.objects.get(id=post_id)
    context = {
        'user': user,
        'post': one_post
    }
    return render(request, 'edit_post.html', context)

def update(request, post_id):
    if 'logged_user' not in request.session:
        return redirect('/')
    
    errors = Post.objects.post_validator(request.POST) # post
    
    if errors:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect(f'/{post_id}/update')
    #if request.method == "POST":
    else:
        user = User.objects.get(id=request.session['logged_user'])
        to_update = Post.objects.get(id=post_id)
        to_update.title = request.POST['title']
        to_update.description = request.POST['description']
        to_update.save()

        return redirect('/success')