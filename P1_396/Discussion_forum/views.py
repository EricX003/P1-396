from django.shortcuts import render, redirect
from .models import * 
from .forms import * 
from django.shortcuts import HttpResponse
from django.contrib.auth.models import User, auth
from django.contrib import messages
from django.forms.models import model_to_dict

'''
from django.shortcuts import redirect, render, get_object_or_404
from .models import Author, Category, Post, Comment, Reply
from .utils import update_views
from .forms import PostForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
'''

def logout(request):
    auth.logout(request)
    return redirect(home)

def goMedia(request):
    allFiles = Media.objects.all()
    context = {"allFiles" : allFiles}
    return render(request,'./media.html', context)

def uploadFiles(request):
    user = request.user

    if request.method == 'POST':
        data = request.POST['description']
        files = request.FILES.getlist('files')

        for curfile in files:
            file = Media.objects.create(
                description = data,
                file = curfile
            )
            file.save()

        return redirect(goMedia)

    return render(request, './addFile.html')

def home(request):
    if request.user.is_authenticated:
        visitor = NewIndicator.objects.get(user_ID = request.user)
        new = visitor.newPost
        context = {'newPost':new}       
        return render(request,'./home.html', context)
    context = {'newPost':False}  
    return render(request,'./home.html', context)

def goForum(request):
    visitor = NewIndicator.objects.get(user_ID = request.user)
    visitor.newPost = False
    visitor.save()

    forums=forum.objects.all()
    count=forums.count()
    discussions=[]
    for i in forums:
        discussions.append(i.discussion_set.all())
 
    context={'forums':forums,
              'count':count,}
    return render(request,'forum.html',context)

def toPost(request, postID):
    post = forum.objects.get(id = postID)
    post.views = post.views + 1
    post.save()

    forums=forum.objects.all()
    count=forums.count()
    discussions=[]
    for i in forums:
        discussions.append(i.discussion_set.all())
 
    context={'forum':post,
              'discussions':discussions}
    return render(request, 'viewPost.html', context)

def makePost(request):
    form = CreateInForum()
    if request.method == 'POST':
        form = CreateInForum(request.POST)
        if form.is_valid():
            form.save()
            unreads = NewIndicator.objects.all()
            for unread in unreads:
                unread.newPost = True
                unread.save()
            return redirect(goForum)

    context ={'form':form}
    return render(request,'./makePost.html',context)

def replyPost(request, postID):
    form = CreateInDiscussion()
    if request.method == 'POST':
        form = CreateInDiscussion(request.POST)
        if form.is_valid():
            form.save()
            return redirect(goForum)
    context ={'form':form, 'id':postID}
    return render(request,'./replyPost.html',context)

def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = auth.authenticate(username=username, password=password)

        if user is not None:
            auth.login(request, user)
            return redirect(home)
        else:
            messages.info(request, 'Incorrect Username or Password')
            return redirect(login)
    else:
        return render(request, './login.html')

def register(request):
    if request.method == 'POST':
        fname = request.POST['FName']
        lname = request.POST['LName']
        username = request.POST['username']
        password = request.POST['password']
        confirm = request.POST['confirm']

        if password==confirm:

            if User.objects.filter(first_name=fname).exists() and User.objects.filter(last_name=lname).exists() and \
                User.objects.filter(first_name=fname) == User.objects.filter(last_name=lname):

                messages.info(request, 'You Already Have an Account!')
                return redirect(login)
            else:
                if User.objects.filter(username=username).exists():
                    messages.info(request, 'Username is Taken, Select Another')
                    return redirect(register)
                else:
                    user = User.objects.create_user(username=username, password=password, first_name=fname, last_name=lname)
                    user.save()
                    visited = NewIndicator(user_ID = user, newPost = False)
                    visited.save()
                    
                    return redirect(home)
            

        else:
            messages.info(request, 'Passwords Do Not Match!')
            return redirect(register)
            

    else:
        return render(request, './newAccount.html')
'''

def logout(request):
    auth.logout(request)
    return redirect(home)

def home(request):
    forums = Category.objects.all()
    num_posts = Post.objects.all().count()
    num_users = User.objects.all().count()
    num_categories = forums.count()

    context = {
        "forums":forums,
        "num_posts":num_posts,
        "num_users":num_users,
        "num_categories":num_categories,
        "title": "Forum"
    }
    return render(request, "forums.html", context)

def detail(request, slug):
    post = get_object_or_404(Post, slug=slug)
    if request.user.is_authenticated:
        author = Author.objects.get(user=request.user)
    
    if "comment-form" in request.POST:
        comment = request.POST.get("comment")
        new_comment, created = Comment.objects.get_or_create(user=author, content=comment)
        post.comments.add(new_comment.id)

    if "reply-form" in request.POST:
        reply = request.POST.get("reply")
        commenr_id = request.POST.get("comment-id")
        comment_obj = Comment.objects.get(id=commenr_id)
        new_reply, created = Reply.objects.get_or_create(user=author, content=reply)
        comment_obj.replies.add(new_reply.id)


    context = {
        "post":post,
        "title": post.title,
    }
    update_views(request, post)

    return render(request, "detail.html", context)

def posts(request, slug):
    category = get_object_or_404(Category, slug=slug)
    posts = Post.objects.filter(approved=True, categories=category)
    paginator = Paginator(posts, 5)
    page = request.GET.get("page")
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages) 

    context = {
        "posts":posts,
        "forum": category,
        "title": "OZONE: Posts"
    }

    return render(request, "posts.html", context)


@login_required
def create_post(request):
    context = {}
    form = PostForm(request.POST or None)
    if request.method == "POST":
        if form.is_valid():
            author = Author.objects.get(user=request.user)
            new_post = form.save(commit=False)
            new_post.user = author
            new_post.save()
            form.save_m2m()
            return redirect("home")
    context.update({
        "form": form,
        "title": "Create New Post"
    })
    return render(request, "create_post.html", context)

def latest_posts(request):
    posts = Post.objects.all()
    context = {
        "posts":posts,
        "title": "All Posts"
    }

    return render(request, "latest-posts.html", context)
'''