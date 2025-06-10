from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import get_object_or_404
from .models import Thread, Post
from .forms import SignupForm
from .models import Category
from .models import UserProfile
from .models import Discussion
from .forms import DiscussionForm, ReplyForm
from django.contrib.auth.forms import UserCreationForm
from .models import ImagePost
from .models import UserReview

def signup_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        role = request.POST['role']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']

        if password != confirm_password:
            messages.error(request, "Passwords do not match.")
            return redirect('signup')

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists.")
            return redirect('signup')

        if User.objects.filter(email=email).exists():
            messages.error(request, "Email already registered.")
            return redirect('signup')

        user = User.objects.create_user(username=username, email=email, password=password)
        user.save()

        messages.success(request, "Your Account has been created, Welcome!")
        return redirect('login')  # make sure this URL name exists
    return render(request, 'forum/signup.html')


def login_view(request):
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user:
            login(request, user)
            return redirect('home')
        else:
            return render(request, 'forum/login.html', {'error': 'Invalid credentials'})

    return render(request, 'forum/login.html')

def logout_view(request):
    logout(request)
    return redirect('home')

def forum_home(request):
     categories = Category.objects.all()
     return render(request, 'forum/home.html',{'categories': categories})

def category_detail(request, category_id):
     category = get_object_or_404(Category, id=category_id)
     threads = Thread.objects.filter(category=category).order_by('-created_at')
     return render(request,'forum/category_detail.html',{'category': category, 'threads': threads})

def thread_detail(request, thread_id):
     thread = get_object_or_404(Thread, id = thread_id)
     posts =  Post.objects.filter(thread=thread).order_by('created_at')
     return render(request, 'forum/thread_detail.html',{'thread': thread, 'posts': posts})


@login_required
def new_thread(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    if request.method == 'POST':
        title = request.POST['title']
        content = request.POST['content']
        thread = Thread.objects.create(title=title, category=category, author=request.user)
        Post.objects.create(thread=thread, author=request.user, content=content)
        return redirect('thread_detail', thread_id=thread.id)
    return render(request, 'forum/new_thread.html', {'category': category})

@login_required
def new_post(request, thread_id):
     thread = get_object_or_404(Thread, id = thread_id)
     if request.method == 'POST':
          content = request.POST['content']
          Post.objects.create(thread = thread, author = request.user, content = content)
          return redirect('thread_detail', thread_id=thread.id)
     return render(request, 'forum/new_post.html',{'thread': thread})


def discussion_list(request):
    sort_option = request.GET.get('sort', 'latest')
    date = request.GET.get('date')

    discussions = Discussion.objects.all()

    if date:
        discussions = discussions.filter(created_at__date=date)

    if sort_option == 'oldest':
        discussions = discussions.order_by('created_at')
    else:  # default is 'latest'
        discussions = discussions.order_by('-created_at')

    return render(request, 'forum/discussion_list.html', {
        'discussions': discussions
    })


@login_required
def discussion_create(request):
    if request.method == 'POST':
        form = DiscussionForm(request.POST, request.FILES)  # Must include request.FILES
        if form.is_valid():
            discussion = form.save(commit=False)
            discussion.author = request.user
            discussion.save()
            return redirect('discussion_detail', pk=discussion.pk)
    else:
        form = DiscussionForm()
    
    return render(request, 'forum/discussion_form.html', {'form': form})

     

def discussion_detail(request, pk):
     discussion = get_object_or_404(Discussion, pk=pk)
     replies = discussion.replies.all()

     if request.method == 'POST':
          form = ReplyForm(request.POST)
          if form.is_valid():
               reply = form.save(commit=False)
               reply.discussion = discussion
               reply.author = request.user
               reply.save()
               return redirect('discussion_detail', pk=discussion.pk)
     else:
        form = ReplyForm()

     return render(request, 'forum/discussion_detail.html',{
                 'discussion': discussion,
                 'replies' : replies,
                 'form' : form
            })

def home(request):
    if request.user.is_authenticated:
        return render(request, 'forum/home.html')
    return render(request, 'forum/home.html')

def discussions(request):
    discussions = Discussion.objects.all().order_by('-created_at')
    return render(request, 'forum/discussion_list.html', {'discussions': discussions})


def user_reviews(request):
    image_files = [
        'images/review1.jpg',
        'images/review2.png',
        'images/review3.jpeg',
    ]
    return render(request, 'forum/user_reviews.html', {'images': image_files})


def about_us(request):
    return render(request, 'forum/about_us.html')