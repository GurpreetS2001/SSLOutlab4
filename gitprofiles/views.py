from django.http import response
from .models import Profile, Repository
from django.contrib.auth.models import User
from django.shortcuts import render

# Create your views here.

from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.views import generic
from .signup import SignUpForm
import requests


class SignUpView(generic.CreateView):
    form_class = SignUpForm
    success_url = reverse_lazy('login')
    template_name = 'registration/signup.html'

def getUserDetails(request):
    if(User.is_authenticated):
        if request.method=="POST":
            if request.POST.get("selected_user")=="Refresh Data":
                pageHead=str(request.user.first_name)+' '+str(request.user.last_name)+'(@'+str(request.user.username)+')'
                data1=requests.get(f'https://api.github.com/users/{request.user.username}')
                data2=requests.get(f'https://api.github.com/users/{request.user.username}/repos')
                json_data1=data1.json()
                json_data2=data2.json()
                getProfile=Profile.objects.filter(user_id=request.user.pk)
                getProfile[0].followers=json_data1['followers']
                getProfile[0].last_updated=json_data1['updated_at']
                getProfile[0].save()
                repos=Repository.objects.filter(profile_id=Profile.objects.filter(user_id=request.user.pk)[0].pk)
                for i in range(0,repos.count()):
                    repos[0].delete()
                for repos in json_data2:
                    repo=Repository(profile=getProfile[0],repo_name=repos['name'],stars=repos['stargazers_count'])
                    repo.save()
                # if len(json_data2)>=repos.count():
                #     for i in range(0,repos.count()):
                #         repos[i].repo_name=json_data2[i]['name']
                #         repos[i].stars=json_data2[i]['stargazers_count']
                #         repos[i].save()
                #     for i in range(repos.count(),len(json_data2)):
                #         repo=Repository(profile=getProfile[0],repo_name=json_data2[i]['name'],stars=json_data2[i]['stargazers_count'])
                #         repo.save()
                # else:
                #     for i in range(0,len(json_data2)):
                #         repos[i].repo_name=json_data2[i]['name']
                #         repos[i].stars=json_data2[i]['stargazers_count']
                #         repos[i].save()
                #     for i in range(len(json_data2),repos.count):
                #         repos[i].delete()
                refresh=True
                repos=Repository.objects.filter(profile_id=Profile.objects.filter(user_id=request.user.pk)[0].pk)
                return render(request,'userprofile.html',{'pageHead':pageHead,'followers':getProfile[0].followers,'repos':repos,'last_updated':getProfile[0].last_updated,'refresh':refresh})
            else:
                user_name=request.POST.get("selected_user")
                user=User.objects.filter(username=user_name)
                getProfile=Profile.objects.filter(user_id=user[0].pk)
                followers=getProfile[0].followers
                last_updated=getProfile[0].last_updated
                repos=Repository.objects.filter(profile_id=Profile.objects.filter(user_id=user[0].pk)[0].pk)
                pageHead=str(user[0].first_name)+' '+str(user[0].last_name)+'(@'+str(user[0].username)+')'
                refresh=False
                return render(request,'userprofile.html',{'pageHead':pageHead,'followers':followers,'repos':repos,'last_updated':last_updated,'refresh':refresh})
        else:
            pageHead=str(request.user.first_name)+' '+str(request.user.last_name)+'(@'+str(request.user.username)+')'
            if(Profile.objects.filter(user_id=request.user.pk).exists()):
                getProfile=Profile.objects.filter(user_id=request.user.pk)
                followers=getProfile[0].followers
                last_updated=getProfile[0].last_updated
                repos=Repository.objects.filter(profile_id=Profile.objects.filter(user_id=request.user.pk)[0].pk)
                refresh=True
                return render(request,'userprofile.html',{'pageHead':pageHead,'followers':followers,'repos':repos,'last_updated':last_updated,'refresh':refresh})
            else:
                data1=requests.get(f'https://api.github.com/users/{request.user.username}')
                data2=requests.get(f'https://api.github.com/users/{request.user.username}/repos')
                if(data1.status_code==200 & data2.status_code==200):
                    json_data1=data1.json()
                    json_data2=data2.json()
                    newprofile=Profile.objects.create(user=request.user,followers=json_data1['followers'],last_updated=json_data1['updated_at'])
                    for repos in json_data2:
                        repo=Repository(profile=newprofile,repo_name=repos['name'],stars=repos['stargazers_count'])
                        repo.save()
                    getProfile=Profile.objects.filter(user_id=request.user.pk)
                    followers=getProfile[0].followers
                    last_updated=getProfile[0].last_updated
                    repos=Repository.objects.filter(profile_id=Profile.objects.filter(user_id=request.user.pk)[0].pk)
                    refresh=True
                    return render(request,'userprofile.html',{'pageHead':pageHead,'followers':followers,'repos':repos,'last_updated':last_updated,'refresh':refresh})
                else:
                    return response.HttpResponse('Bhaag Chutiye')
    else:
        return response.HttpResponse('Plz login first')

def explorePage(request):
    if(User.is_authenticated):
        people=Profile.objects.all()
        return render(request,'explore.html',{'users':people})
    else:
        return response.HttpResponse('Plz login first')