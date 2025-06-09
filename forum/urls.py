from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from forum import views as forum_views

urlpatterns = [
    path('', views.home, name='home'),
    path('forum_home/', views.forum_home, name='forum_home'),

    path('category/<int:category_id>/', views.category_detail, name='category_detail'),
    path('thread/<int:thread_id>/', views.thread_detail, name='thread_detail'),
    path('category/<int:category_id>/new_thread/', views.new_thread, name='new_thread'),
    path('thread/<int:thread_id>/new_post/', views.new_post, name='new_post'),

    path('discussions/', views.discussion_list, name='discussion_list'),
    path('discussion/new/', views.discussion_create, name='discussion_create'),
    path('discussion/<int:pk>/', views.discussion_detail, name='discussion_detail'),

    path('signup/', views.signup_view, name='signup'),
    path('login/', views.login_view, name='login'),
    path('accounts/login/', auth_views.LoginView.as_view(template_name='forum/login.html'), name='login'),

    path('logout/', views.logout_view, name='logout'),

    path('review/', views.user_review, name='user_review'),

    path('about/', views.about_us, name='about_us'),
]
