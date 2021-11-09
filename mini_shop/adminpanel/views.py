from django.shortcuts import render
from loginpage.models import CustomUser, Profile
from .forms import EditUserRole


def get_users_list(request):
    usernames = [user.username for user in CustomUser.objects.all()]
    roles = [user.role for user in CustomUser.objects.all()]

    users = [(username, role) for username, role in zip(usernames, roles)]
    print(users)
    context = {"users": users}
    return render(request=request, template_name='adminpanel/admin_main.html', context=context)


def user_info_request(request, username):
    user = CustomUser.objects.get(username=username)
    user_profile = Profile.objects.get(user=user)
    form = EditUserRole(initial={'is_admin': user.role})
    context = {'user_profile': user_profile,
               'edit_form': form}
    if request.method == 'GET':
        return render(request=request, template_name='adminpanel/admin_edit.html', context=context)
    else:
        filled_form = EditUserRole(request.POST)
        if filled_form.is_valid():
            role = filled_form.cleaned_data.get('is_admin')
            user.role = role
            user.save()
            context['edit_form'] = filled_form
            return render(request=request, template_name='adminpanel/admin_edit.html', context=context)
