from django.http import HttpResponse
from django.shortcuts import render,redirect
from team.models import team
# Create your views here.
def index(request):
    team_data = team.objects.all()
    context = {
        'team_data': team_data,
    }
    return HttpResponse(render(request,'team/team_form.html'))
def add_team(request):
    if request.method == "POST":
        f_name = request.POST.get("f_name")
        l_name = request.POST.get("l_name")
        email = request.POST.get("l_name")
        job_title = request.POST.get("job_title")
        fb_link = request.POST.get("fb")
        twitter_link = request.POST.get("twitter")
        g_scholar = request.POST.get("g_scholar")
        team_add = team(
            first_name = f_name,
            last_name = l_name,
            email = email,
            job_title = job_title,
            fb_link = fb_link,
            twitter_link = twitter_link,
            g_scholar_link  = g_scholar,
        )
        team_add.save()
        return redirect('add_team')