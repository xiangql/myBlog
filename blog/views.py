from django.shortcuts import render, redirect, reverse
import json
from .models import *
from django.http import HttpResponse, JsonResponse
import time
from .methods import *
# Create your views here.

def login(request):
    if request.method == "POST":
        sendMsg = {}
        recvMsg = request.body.decode()
        userData = json.loads(recvMsg)
        u = User.objects.filter(account=userData['account'])
        if u.exists():
            if userData['password'] == u[0].password:
                request.session['id'] = u[0].account
                request.session['name'] = u[0].petname
                request.session.set_expiry(0)
                sendMsg['state'] = "success"
                sendMsg['reason'] = "success"
                return JsonResponse(sendMsg)
        sendMsg['state'] = "failed"
        sendMsg['reason'] = "login faile,account or password error !!!"
        return JsonResponse(sendMsg)
    return render(request, 'blog/login.html')

def regist(request):
    if request.method == "POST":
        sendMsg = {}
        recvMsg = request.body.decode()
        userData = json.loads(recvMsg)
        account = userData['account']
        qAcc = User.objects.filter(account=account)
        if qAcc.exists():
            sendMsg['state'] = "failed"
            sendMsg['reason'] = "account repeat"
            return JsonResponse(sendMsg)
        password = userData['password']
        petname = userData['petname']
        email = userData['email']
        qEmail = User.objects.filter(email=email)
        if qEmail.exists():
            sendMsg['state'] = "failed"
            sendMsg['reason'] = "email repeat"
            return JsonResponse(sendMsg)
        phone = userData['phone']
        qPhone = User.objects.filter(phone=phone)
        if qPhone.exists():
            sendMsg['state'] = "failed"
            sendMsg['reason'] = "phone repeat"
            return JsonResponse(sendMsg)
        user = User(account=account, password=password, petname=petname, email=email, phone=phone, isDelete=False)
        user.save()
        request.session['id'] = account
        request.session['name'] = petname
        request.session.set_expiry(0)
        sendMsg['state'] = "success"
        sendMsg['reason'] = "success"
        return JsonResponse(sendMsg)
    return render(request, 'blog/regist.html')

def index(request):
    nums = get_typenums()
    typelist = get_typelist()
    bloglist = get_bloglist()
    return render(request, 'blog/index.html', {'typelist': typelist, 'bloglist': bloglist, 'nums': nums})

def logout(request):
    request.session.clear()
    request.session.delete('session_key')
    return redirect(reverse('blog:login'))

def writeBlog(request):
    id = request.session.get('id', None)
    if id == None:
        return redirect(reverse('blog:login'))
    if request.method == "POST":
        sendMsg = {}
        recvMsg = request.body.decode()
        data = json.loads(recvMsg)
        bid = str(int(time.time()))+'id'+request.session['id']#以用户名和时间戳形成的字符串设为id
        title = data['title']
        btype = data['btype']
        context = data['context']
        author = User.objects.get(account=request.session.get('id', None))
        blog = Blog(bid=bid, title=title, btype=btype, context=context, author=author, isDelete=False)
        blog.save()
        sendMsg['state'] = "success"
        sendMsg['reason'] = "success"
        return JsonResponse(sendMsg)
    return render(request, 'blog/write.html')


def readBlog(request):
    bid = request.GET.get('id')
    blog = Blog.objects.get(bid=bid)
    typelist = get_typelist()
    bloglist = get_bloglist()
    nums = get_typenums()
    author = blog.author.petname
    return render(request, 'blog/read.html', {'blog': blog, 'typelist': typelist, 'author': author, 'bloglist': bloglist, 'nums': nums})

def collect(request):
    uid = request.session.get('id', None)
    if uid == None:
        sendMsg = {'state': 'unlogin', 'reason': "请先登录博客再添加收藏！！！"}
        return JsonResponse(sendMsg)
    if request.method == "POST":
        sendMsg = {}
        recvMsg = request.body.decode()
        data = json.loads(recvMsg)
        bid = data['bid']
        c = Collect.objects.get_or_create(uid=uid, bid=bid, isDelete=False)
        if c[1]:
            sendMsg['state'] = "success"
            sendMsg['reason'] = "success"
        else:
            sendMsg['state'] = "failed"
            sendMsg['reason'] = "此条博客已被收藏，不能重复收藏"
        print(sendMsg)
        return JsonResponse(sendMsg)
    return render(request, 'blog/read.html')

def person(request):
    uid = request.session.get('id', None)
    if uid == None:
        return redirect(reverse('blog:login'))
    user = User.objects.get(account=uid)
    bloglist = get_person_bloglist(num=30,author=user)
    bnum = Blog.objects.filter(isDelete=False).filter(author=user).count()
    cnum = Collect.objects.filter(isDelete=False).filter(uid=uid).count()
    cblogs = get_collect_blog(uid=uid)
    if request.method == "POST":
        recvMsg = request.body.decode()
        data = json.loads(recvMsg)
        sendMsg = {}
        if data['itype'] == "info":
            user = User.objects.filter(isDelete=False).get(account=uid)
            user.petname = data['petname']
            user.phone = data['phone']
            user.email = data['email']
            user.save()
            sendMsg['state'] = "success"
            sendMsg['reason'] = "修改信息成功!!!"
            return JsonResponse(sendMsg)
        elif data['itype'] == "pwd":
            user = User.objects.filter(isDelete=False).get(account=uid)
            if user.password != data['oldpassword']:
                sendMsg['state'] = "failed"
                sendMsg['reason'] = "旧密码错误!!!"
                return JsonResponse(sendMsg)
            user.password = data['newpassword']
            user.save()
            sendMsg['state'] = "success"
            sendMsg['reason'] = "密码修改成功,注销后旧密码失效!!!"
            return JsonResponse(sendMsg)
        elif data['itype'] == "rblog":
            blog = Blog.objects.filter(isDelete=False).get(bid=data['bid'])
            sendMsg['state'] = "success"
            sendMsg['reason'] = blog.context
            return JsonResponse(sendMsg)
        elif data['itype'] == "cblog":
            blog = Blog.objects.filter(isDelete=False).get(bid=data['bid'])
            blog.title = data['title']
            blog.btype = data['btype']
            blog.context = data['context']
            blog.save()
            sendMsg['state'] = "success"
            sendMsg['reason'] = "博客修改成功!!!"
            return JsonResponse(sendMsg)
        elif data['itype'] == "delblog":
            blog = Blog.objects.filter(isDelete=False).get(bid=data['bid'])
            blog.isDelete = True
            blog.save()
            col = Collect.objects.filter(isDelete=False).get(bid=data['bid'])
            col.isDelete = True
            col.save()
            sendMsg['state'] = "success"
            sendMsg['reason'] = "博客删除成功!!!"
            return JsonResponse(sendMsg)
        elif data['itype'] == "delcblog":
            col = Collect.objects.filter(isDelete=False).get(bid=data['bid'])
            col.isDelete = True
            col.save()
            sendMsg['state'] = "success"
            sendMsg['reason'] = "此条收藏已删除!!!"
    return render(request, 'blog/person.html', {'bloglist': bloglist, 'user': user, 'bnum': bnum, 'cnum': cnum, 'cblogs': cblogs})


def comment(request):
    comments = Comment.objects.filter(isDelete=False).order_by('-cid')#倒序
    talk = "人生苦短，我学Python !"
    uid = request.session.get('id', None)
    if request.method == "POST":
        if uid == None:
            sendMsg = {'state':"failed", 'reason':"发表评论前，请先登录！！！"}
            return JsonResponse(sendMsg)
        recvMsg = request.body.decode()
        data = json.loads(recvMsg)
        user = User.objects.get(account=uid)
        com = Comment(fUser=user, content=data['comment'], isDelete=False)
        com.save()
        sendMsg = {'state': "success", 'reason': "评论已发表!!!"}
        return JsonResponse(sendMsg)
    return render(request, 'blog/comment.html', {'comments': comments, "talk": talk})

def about(request):
    if request.method == "POST":
        recvMsg = request.body.decode()
        data = json.loads(recvMsg)
        info = RecvMsg(name=data['name'], email=data['email'], msg=data['msg'])
        info.save()
        sendMsg = {'state': "success", 'reason': "你的发送信息已被接收！！！"}
        return JsonResponse(sendMsg)
    return render(request, 'blog/about.html')



