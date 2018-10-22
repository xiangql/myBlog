from .models import *
import re
from django.db.models import Count
import datetime
def get_typelist():
    blogs = Blog.objects.filter(isDelete=False)
    btypes = blogs.values_list('btype').distinct()
    typelist = []
    for btype in btypes:
        typelist.append(btype[0])
    return typelist

def get_typenums():
    blogs = Blog.objects.filter(isDelete=False)
    infos = blogs.values('btype').annotate(count=Count('btype')).values_list('btype', 'count')
    data = {}
    for info in infos:
        data[info[0]] = info[1]
    return data

def get_makedown_text(context,num=150):
    #https://www.jianshu.com/p/55b5bfe96feb
    #https://www.jianshu.com/p/0650f7eeef3e
    pattern = '[\\\`\*\_\[\]\#\+\-\!\>]'
    context1 = re.sub(pattern, '', context)
    if len(context1) > num:
        return context1[0:num]+" ..."
    else:
        return context1

def get_bloglist(num=150):
    bloglist = []
    blogs = Blog.objects.filter(isDelete=False).values_list('bid', 'title', 'btype', 'cDate', 'context').order_by('cDate')
    for blog in blogs:
        info = []
        info.append(blog[0])
        info.append(blog[1])
        info.append(blog[2])
        info.append(blog[3].strftime("%Y-%m-%d %H:%M:%S"))
        info.append(get_makedown_text(blog[4], num))
        bloglist.append(info)
    return bloglist

def get_person_bloglist(num=150,author=0):
    bloglist = []
    blogs = Blog.objects.filter(isDelete=False).filter(author=author).values_list('bid', 'title', 'btype', 'cDate', 'context').order_by(
        'cDate')
    for blog in blogs:
        info = []
        info.append(blog[0])
        info.append(blog[1])
        info.append(blog[2])
        info.append(blog[3].strftime("%Y-%m-%d %H:%M:%S"))
        info.append(get_makedown_text(blog[4], num))
        bloglist.append(info)
    return bloglist
def get_collect_blog(uid):
    bids = Collect.objects.filter(isDelete=False).filter(uid=uid).values_list('bid')
    cblogs = []
    for bid in bids:
        cblog = Blog.objects.get(bid=bid[0])
        cblogs.append(cblog)
    return cblogs