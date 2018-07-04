from django.shortcuts import render,get_object_or_404
from django.http import HttpResponse
from django.core.paginator import Paginator
from movie_s import pa
from .models import Movie
# Create your views here.

def base(request,objets_list):
    paginator =Paginator(objets_list,15) #每页10篇
    page_num = request.GET.get('page',1) #获取Url的页面参数(GET请求)
    page_of_movie = paginator.get_page(page_num) #获取当前页数的内容
    #获取当前页面前后各2页的页码范围
    current_page_num = page_of_movie.number #获取当前页数
    page_range = list(range(max(current_page_num - 2,1),current_page_num)) + \
                 list(range(current_page_num, min(current_page_num + 2 , paginator.num_pages)+1))
    # 加上省页面标记
    if page_range[0] - 1 >= 2:
        page_range.insert(0,'...')
    if paginator.num_pages - page_range[-1] >= 2:
        page_range.append('...')

    # 加上首页和尾页
    if page_range[0] != 1:
        page_range.insert(0,1)
    if page_range[-1] != paginator.num_pages:
        page_range.append(paginator.num_pages)

    context = {}
    context['movie_list'] = page_of_movie.object_list
    context['page_range'] = page_range
    context['page_of_blogs'] = page_of_movie
    return context


def movie_list(request):
    content = {}
    movie_list = Movie.objects.all()
    content = base(request, movie_list)
    return render(request,'index.html',content)


def movie_datail(request,movie_pk):
    movie = get_object_or_404(Movie, pk=movie_pk)
    context = {}
    context['movie'] = movie
    return render(request,'movie_datail.html',context)

def movie_delete(request):
     Movie.objects.all().delete()
     return render(request,'ok.html',context = {'ok':'ok'})

def find_movie(request):
    context = {}
    error_msg = ''
    movie_name = request.GET.get('q')

    #判断是否为空
    if not movie_name:
        error_msg = '请输入关键词'
        context['error_msg'] = error_msg
        return render(request, 'find_movie.html',context)

    movie_list = Movie.objects.filter(title__icontains=movie_name)
    context = base(request, movie_list)
    context['movie_list'] = movie_list
    return render(request,'find_movie.html',context)