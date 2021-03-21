from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, get_user_model, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.db.models import Q
from django.utils import timezone
from django.core.cache import cache
from .forms import LoginForm, RegisterForm, PasswordForm
from .utils import get_ip_address
from .models import UserInfo
from api.models import Post


User = get_user_model()
# Create your views here.
@login_required()
def change_password_view(request):
	if request.method == 'POST':
		form = PasswordForm(request.POST or None)
		if form.is_valid():
			username = form.cleaned_data.get('username')
			password = form.cleaned_data.get('password')
			new_password = form.cleaned_data.get('new_password')
			user = authenticate(request, username=username, password=password)
			if user != None:
				user_update = User.objects.get(username=username)
				user_update.set_password(new_password)
				user_update.save()
				return redirect('/password_changed')
	else:
		form = PasswordForm()
	return render(request, 'accounts/accounts_password_form.html', {'form': form})

def homepage_view(request):
	context ={}
	return render(request, 'accounts/accounts_homepage_view.html', context)

@login_required()
def ip_check_view(request):
	context = {}
	return render(request, 'accounts/accounts_ipcheck_view.html', context)

def login_view(request):
	message = ''
	ip_address = get_ip_address(request)
	initial_data = {
		'ip_address': ip_address,
	}
	if cache.get(f'{ip_address}_attempt'):
		print(cache.get(f'{ip_address}_attempt'), f'ATTEMPTS FROM {ip_address}')
		pass
	else:
		cache.set(f'{ip_address}_attempt',0,60)
	if request.method == 'POST':
		if request.POST.get('next'):
			next = request.POST.get('next')
		else:
			next = ''
		form = LoginForm(request.POST or None)
		if cache.get(f'{ip_address}_attempt') >= 5:
			message = 'Too many attempt! Retry in few seconds.'
		else:
			if form.is_valid():
				username = form.cleaned_data.get('username')
				password = form.cleaned_data.get('password')
				user = authenticate(request, username=username, password=password)
				if user != None:
					login(request, user)
					try:
						user_info = UserInfo.objects.get(user=user)
					except:
						user_info = UserInfo.objects.create(user=user)
					user_info.last_login = timezone.now()
					user_info.save()
					ip_address = get_ip_address(request)
					if ip_address != user_info.ip_address:
						user_info.ip_address = ip_address
						user_info.save()
						return redirect(f"/ip_check/?next={ next }")
					elif next != '':
						return redirect(next)
					else:
						return redirect('/')
	else:
		form = LoginForm(initial=initial_data)
	return render(request, 'accounts/accounts_login_form.html', {'form': form,
																 'message': message,
														})

def logout_view(request):
	logout(request)
	return redirect('/login')

def password_changed_view(request):
	context = {}
	return render(request, 'accounts/accounts_password_changed.html', context)

def permission_denied_view(request):
	return render(request, 'accounts/accounts_permission_denied.html', {})

def register_view(request):
	message = ''
	ip_address = get_ip_address(request)
	initial_data = {
		'ip_address': ip_address,
	}
	if cache.get(f'{ip_address}_hacking'):
		print(cache.get(f'{ip_address}_hacking'), f'ATTEMPTS FROM {ip_address}')
		pass
	else:
		cache.set(f'{ip_address}_hacking',0,999999999)
	if request.method == 'POST':
		form = RegisterForm(request.POST or None)
		if cache.get(f'{ip_address}_hacking') >= 3:
			message = 'It seems you are trying to hack the system. You cannot register anymore.'
		else:
			if form.is_valid():
				username = form.cleaned_data.get('username')
				first_name = form.cleaned_data.get('first_name')
				last_name = form.cleaned_data.get('last_name')
				email = form.cleaned_data.get('email')
				password = form.cleaned_data.get('password')
				try:
					user = User.objects.create_user(username, email, password, first_name=first_name, last_name=last_name)
				except:
					user = None
				if user != None:
					ip_address = get_ip_address(request)
					last_login = timezone.now()
					user_info = UserInfo.objects.create(user=user, last_login=last_login, ip_address=ip_address)
					login(request, user)
					return redirect('/')
	else:
		form = RegisterForm(initial=initial_data)
	return render(request, 'accounts/accounts_register_form.html', {'form': form,
																	'message': message,
																	})

@staff_member_required()
def user_list_view(request):
	users = User.objects.all().filter().order_by('username')
	queryset_n_posts = []
	counting = 0
	search = False
	query = request.GET.get('q')
	if query:
		users = User.objects.filter(Q(username__icontains=query)|
									Q(id__icontains=query)|
									Q(first_name__icontains=query)|
									Q(last_name__icontains=query)|
									Q(email__icontains=query)
									).distinct()
		search = True
		counting = users.count()
	for x in users:
		n_posts = len(Post.objects.all().filter(user=x))
		queryset_n_posts.append(n_posts)
	table = dict(zip(users, queryset_n_posts))
	return render(request, 'accounts/accounts_user_list.html', {'table': table,
																'counting': counting,
																'search': search})

@login_required()
def user_profile_view(request, id):
	user_obj = get_object_or_404(User, id=id)
	if request.user.is_staff:
		user_info = UserInfo.objects.get(user=user_obj)
		user_posts = Post.objects.filter(user=user_obj)
	else:
		if request.user.id == user_obj.id:
			user_info = UserInfo.objects.get(user=user_obj)
			user_posts = Post.objects.filter(user=user_obj)
		else:
			return redirect('/permission_denied')
	return render(request, 'accounts/accounts_user_profile.html', {'user_obj': user_obj,
																   'user_info': user_info,
																   'user_posts': user_posts,})