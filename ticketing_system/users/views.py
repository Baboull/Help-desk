from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, update_session_auth_hash
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import CustomUserCreationForm, ProfileUpdateForm, CustomPasswordChangeForm, AdminUserEditForm, DepartmentForm
from departments.models import Department
from .models import User

def register_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            if user.role == 'staff':
                return redirect('staff_dashboard')
            return redirect('client_dashboard')
    else:
        form = CustomUserCreationForm()
    return render(request, 'registration/register.html', {'form': form})


@login_required
def profile_settings(request):
    profile_form = ProfileUpdateForm(instance=request.user)
    password_form = CustomPasswordChangeForm(user=request.user)

    if request.method == 'POST':
        if 'update_profile' in request.POST:
            profile_form = ProfileUpdateForm(request.POST, instance=request.user)
            if profile_form.is_valid():
                profile_form.save()
                messages.success(request, 'Profile updated successfully.')
                return redirect('profile_settings')

        elif 'change_password' in request.POST:
            password_form = CustomPasswordChangeForm(user=request.user, data=request.POST)
            if password_form.is_valid():
                password_form.save()
                update_session_auth_hash(request, request.user)
                messages.success(request, 'Password changed successfully.')
                return redirect('profile_settings')

    return render(request, 'users/profile_settings.html', {
        'profile_form': profile_form,
        'password_form': password_form,
    })

@login_required
def admin_management(request):
    if request.user.role != 'admin' and not request.user.is_superuser:
        messages.error(request, 'Access denied.')
        return redirect('home')
        
    users = User.objects.all().order_by('username')
    departments = Department.objects.all().order_by('name')
    dept_form = DepartmentForm()
    
    if request.method == 'POST' and 'create_department' in request.POST:
        dept_form = DepartmentForm(request.POST)
        if dept_form.is_valid():
            dept_form.save()
            messages.success(request, 'Department created successfully.')
            return redirect('admin_management')
            
    return render(request, 'users/admin_management.html', {
        'users': users,
        'departments': departments,
        'dept_form': dept_form,
    })

@login_required
def admin_user_edit(request, user_id):
    if request.user.role != 'admin' and not request.user.is_superuser:
        messages.error(request, 'Access denied.')
        return redirect('home')
        
    user_obj = get_object_or_404(User, id=user_id)
    if request.method == 'POST':
        form = AdminUserEditForm(request.POST, instance=user_obj)
        if form.is_valid():
            form.save()
            messages.success(request, f'User {user_obj.username} updated.')
            return redirect('admin_management')
    else:
        form = AdminUserEditForm(instance=user_obj)
        
    return render(request, 'users/admin_user_edit.html', {
        'user_form': form,
        'target_user': user_obj,
    })
