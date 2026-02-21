from django.shortcuts import render, redirect

def home_redirect(request):
    if request.user.is_authenticated:
        if request.user.role == 'staff' or request.user.is_staff:
            return redirect('staff_dashboard')
        return redirect('client_dashboard')
    return redirect('login')
