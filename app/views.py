from django.shortcuts import render, redirect
import bcrypt
from django.contrib import messages
from .models import *

def index(request):
    return render(request, 'index.html')

def register_user(request):
    print(request.POST)
    errors = User.objects.register_validator(request.POST)

    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/')
    else:
        user = User.objects.create(
            first_name = request.POST['first_name'],
            last_name = request.POST['last_name'],
            email = request.POST['email'],
            password = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt()).decode()
        )
        request.session['uuid'] = user.id

        return redirect('/dashboard')

def login_user(request):
    errors = User.objects.login_validator(request.POST)

    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/')
    else:
        user = User.objects.get(email=request.POST['email'])
        request.session['uuid'] = user.id
        return redirect('/dashboard')

def create_job(request):
    # TODO add validation
    errors = Job.objects.job_validator(request.POST)
    print('*'*100)
    print(print(request.POST))
    # print(request.POST['category'])
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/jobs/new')
    else:
        
        logged_in_user = User.objects.get(id=request.session['uuid'])
        Job.objects.create(
            title=request.POST['title'],
            description=request.POST['description'],
            location=request.POST['location'],
            category=request.POST['category'],
            uploaded_by=logged_in_user
        )
        print('Created a Job!')
        return redirect('/dashboard')

def show_job(request):
    if 'uuid' not in request.session:
        return redirect('/')
    context = {
        'user_logged_in': User.objects.get(id=request.session['uuid']),
        'all_jobs_on_add': Job.objects.filter(on_add=True),
        'all_jobs_not_on_add': Job.objects.filter(on_add=False),
        'jobs': User.objects.get(id=request.session['uuid']).jobs_uploaded.all(),
        'granted_jobss': Job.objects.all()
    }
    return render(request, 'dashboard.html', context)

def shows(request, id):
    if 'uuid' not in request.session:
        return redirect('/')
    context = {
        'user_logged_in': User.objects.get(id=request.session['uuid']),
        'jobs': Job.objects.get(id=id)
    }
    return render(request, 'show_job.html', context)

def detaile(request):
    if 'uuid' not in request.session:
        return redirect('/')
    
    context = {
        'user_logged_in': User.objects.get(id=request.session['uuid']),
        'all_jobs_on_add': Job.objects.filter(on_add=True),
        'all_jobs_not_on_add': Job.objects.filter(on_add=False),
    }
    return render(request, 'new_job.html', context)


def grant(request, id):
    job = Job.objects.get(id=id)
    user = User.objects.get(id=request.session['uuid'])
    # add
    user.adedd_jobs.add(job)
    job.on_add = True
    job.save()
    return redirect('/dashboard')
    
def ungrant(request, id):
    job = Job.objects.get(id=id)
    user = User.objects.get(id=request.session['uuid'])
    # add
    user.adedd_jobs.remove(job)
    job.on_add = False
    job.save()
    return redirect('/dashboard')

def grant_show(request, id):
    job = Job.objects.get(id=id)
    user = User.objects.get(id=request.session['uuid'])
    # add
    user.adedd_jobs.add(job)
    job.on_add = True
    job.save()
    return redirect(f'/jobs/{id}')
    
def ungrant_show(request, id):
    job = Job.objects.get(id=id)
    user = User.objects.get(id=request.session['uuid'])
    # add
    user.adedd_jobs.remove(job)
    job.on_add = False
    job.save()
    return redirect(f'/jobs/{id}')

def job_destroy(request, id):
    job = Job.objects.get(id=id)
    job.delete()
    return redirect('/dashboard')

def edit(request, id):
    if 'uuid' not in request.session:
        return redirect('/')
    else:
        context = {
            'user_logged_in': User.objects.get(id=request.session['uuid']),
            'job': Job.objects.get(id=id),
        }
        return render(request, 'edit_job.html', context)

def job_update(request, id):
    errors = Job.objects.job_validator(request.POST)

    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect(f'/jobs/edit/{id}')
    else:
        print("Request", request)
        print(request.POST)
        job = Job.objects.get(id=id)
        job.title = request.POST['title']
        job.description = request.POST['description']
        job.location = request.POST['location']
        job.save()
        return redirect('/dashboard')

def logout_user(request):
    del request.session['uuid']
    # request.session.flush()
    return redirect('/')