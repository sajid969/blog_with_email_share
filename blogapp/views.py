from django.shortcuts import render,get_object_or_404
from blogapp.models import Post
from django.core.paginator import Paginator,EmptyPage,PageNotAnInteger
from django.views.generic import ListView
from django.core.mail import send_mail
from blogapp.forms import emailsendform


# Create your views here.

def postlistview(request):
    post_list=Post.objects.all()
    paginator=Paginator(post_list,1)
    page_number=request.GET.get('page')
    try:
        post_list=paginator.page(page_number)
    except PageNotAnInteger:
        post_list=paginator.page(1)
    except EmptyPage:
        post_list=paginator.page(paginator.num_pages)
    return render(request,'blogapp/post_list.html',{'post_list':post_list})

def postdetailview(request,year,month,day,post):
    post=get_object_or_404(Post,slug=post,status='published',publish__year=year,publish__month=month,publish__day=day)
    return render(request,'blogapp/post_detail.html',{'post':post})

def mailsendview(request,id):
    post=get_object_or_404(Post,id=id,status='published')
    form=emailsendform
    sent=False
    if request.method=='POST':
        form=emailsendform(request.POST)
        if form.is_valid():
            cd=form.cleaned_data
            post_url=request.build_absolute_uri(post.get_absolute_url())
            subject='{}({}) recommends to u read "{}"'.format(cd['name'],cd['email'],post.title)
            message='read post at:\n{}\n\n{}\ncomments:\n{}'.format(post_url,cd['name'],cd['comments'])
            send_mail(subject,message,'tonybabai81@blog.com',[cd['to']])
            sent=True
        else:
            form=emailsendform()
    return render(request,'blogapp/sharebyemail.html',{'form':form,'post':post,'sent':sent})
