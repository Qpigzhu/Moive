from django.urls import path
from .views import movie_datail,movie_delete,find_movie
urlpatterns = [
    #path('delete',movie_delete,name='pa_moive'),  #删除
    path('<int:movie_pk>',movie_datail,name = 'movie_datail'),
    path('find_movie',find_movie,name = 'find_movie'),
]
