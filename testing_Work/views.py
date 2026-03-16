from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from .models import TestingJob
from .forms import EngineerRegisterForm, ProgressForm
from django.db.models import Sum,Count
import pandas as pd
from django.http import HttpResponse
from .models import ActivityLog
from .forms import JobAssignForm
   
def register(request):

    if request.method == 'POST':

        form = EngineerRegisterForm(request.POST)

        if form.is_valid():

            user = form.save(commit=False)

            user.is_staff = False   # ensure engineer is not admin

            user.save()

            return redirect('login')

    else:

        form = EngineerRegisterForm()

    return render(
        request,
        'register.html',
        {'form':form}
    )

from django.contrib.auth import authenticate, login
from django.shortcuts import redirect


def login_view(request):

    if request.method == 'POST':

        username = request.POST.get('username')
        password = request.POST.get('password')
        role = request.POST.get('role')

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user is not None:

            login(request, user)

            if role == "admin":

                if user.is_staff:
                    return redirect('admin_dashboard')
                else:
                    return render(
                        request,
                        'login.html',
                        {'error': 'You are not an admin user'}
                    )

            else:
                return redirect('dashboard')

        else:

            return render(
                request,
                'login.html',
                {'error': 'Invalid Username or Password'}
            )

    return render(request, 'login.html')


@login_required
def dashboard(request):

    query = request.GET.get('search')

    jobs = TestingJob.objects.filter(
        assigned_to=request.user
    )

    total_jobs = TestingJob.objects.count()

    completed = TestingJob.objects.filter(
        status='Completed'
    ).count()

    pending = TestingJob.objects.filter(
        status='Pending'
    ).count()

    revenue = TestingJob.objects.aggregate(
        Sum('amount')
    )

    if query:

        jobs = jobs.filter(
            job_no__icontains=query
        ) | jobs.filter(
            SRF__icontains=query
        )

    return render(
        request,
        'dashboard.html',
        {'jobs':jobs,
         'total': total_jobs,
         'completed': completed,
         'pending': pending,
         'revenue': revenue}
    )


@login_required
def update_progress(request, job_id):

    job = TestingJob.objects.get(id=job_id)

    if request.method == 'POST':

        form = ProgressForm(
            request.POST,
            instance=job
        )

        if form.is_valid():
            form.save()
            ActivityLog.objects.create(
                user=request.user,
                action=f"Updated job {job.job_no}"
            )
            return redirect('dashboard')

    else:

        form = ProgressForm(instance=job)

    return render(
        request,
        'job_update.html',
        {'form':form}
    )


from django.http import HttpResponseForbidden

@login_required
def admin_dashboard(request):

    if not request.user.is_staff:
        return HttpResponseForbidden("Access Denied")

    completed = TestingJob.objects.filter(status='Completed').count()
    pending = TestingJob.objects.filter(status='Pending').count()
    testing = TestingJob.objects.filter(status='Testing').count()

    return render(
        request,
        'admin_dashboard.html',
        {
            'completed': completed,
            'pending': pending,
            'testing': testing
        }
    )

def export_excel(request):

    jobs = TestingJob.objects.all().values()

    df = pd.DataFrame(jobs)

    response = HttpResponse(
        content_type='application/ms-excel'
    )

    response['Content-Disposition'] = 'attachment; filename="testing_report.xlsx"'

    df.to_excel(response,index=False)

    return response

from django.http import HttpResponseForbidden


@login_required
def assign_job(request):

    if not request.user.is_staff:
        return HttpResponseForbidden("Access Denied")

    if request.method == 'POST':

        form = JobAssignForm(request.POST)

        if form.is_valid():

            job = form.save()

            ActivityLog.objects.create(
                user=request.user,
                action=f"Assigned job {job.job_no} to {job.assigned_to}"
            )

            return redirect('admin_dashboard')

    else:

        form = JobAssignForm()

    return render(
        request,
        'assign_job.html',
        {'form':form}
    )