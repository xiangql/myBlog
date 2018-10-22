from django.urls import path
from .views import *

app_name = 'blog'

urlpatterns = [
    path('login/', login, name='login'),
    path('regist/', regist, name='regist'),
    path('index/', index, name='index'),
    path('logout/', logout, name='logout'),
    path('write/', writeBlog, name='write'),
    path('read/', readBlog, name='read'),
    path('collect/', collect, name='collect'),
    path('person/', person, name='person'),
    path('comment/', comment, name='comment'),
    path('about/', about, name='about'),

]