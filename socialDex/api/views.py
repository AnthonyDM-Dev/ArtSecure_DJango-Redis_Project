from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.db.models import Q
from django.utils import timezone
from django.core.cache import cache
from datetime import timedelta
from .models import Post
from .forms import PostForm


# Create your views here.
@login_required()
def posts_list_view(request):
	posts = Post.objects.filter().order_by('-datetime')
	counting = 0
	search = False
	query = request.GET.get('q')
	if query:
		posts = Post.objects.filter(Q(user__username__icontains=query)|
									Q(user__first_name__icontains=query)|
									Q(user__last_name__icontains=query) |
									Q(datetime__icontains=query)|
									Q(title__icontains=query)|
									Q(composition__icontains=query) |
									Q(address__icontains=query)|
									Q(hash__icontains=query)|
									Q(txId__icontains=query)
									).distinct()
		search = True
		counting = posts.count()
	context = {'posts': posts,
			   'counting': counting,
			   'search': search,
			   }
	return render(request, 'api/api_list_post.html', context)

@staff_member_required()
def posts_json_all_view(request):
	response = []
	posts = Post.objects.filter().order_by('-datetime')
	for post in posts:
		response.append(
			{'datetime': post.datetime,
			 'title': post.title,
			 'composition': post.composition,
			 'author': f'{post.user}',
			 'address':f'{post.address}',
			 'hash': post.hash,
			 'txId': post.txId,
			 }
		)
	return JsonResponse(response, safe=False)

@staff_member_required()
def posts_json_24h_view(request):
	past_24h_date = timezone.now() - timedelta(hours=24)
	response = []
	posts = Post.objects.filter().order_by('-datetime')
	for post in posts:
		if post.datetime >= past_24h_date:
			response.append(
				{'datetime': post.datetime,
				 'title': post.title,
				 'composition': post.composition,
				 'author': f'{post.user}',
				 'hash': post.hash,
				 'txId': post.txId,
				 }
			)
	return JsonResponse(response, safe=False)

@login_required()
def new_post_view(request):
	message = ''
	alert = ''
	success = ''
	user = request.user
	initial_data = {
		'user': user,
	}
	if cache.get(f'{user}_not_allowed'):
		print(cache.get(f'{user}_not_allowed'), f'ATTEMPTS FROM {user}')
		pass
	else:
		cache.set(f'{user}_not_allowed',0,600)
	if request.method == 'POST':
		form = PostForm(request.POST or None)
		if cache.get(f'{user}_not_allowed') >= 3:
			message = 'The content you are posting is not allowed. Your account is blocked for 10 minutes.'
		else:
			if form.is_valid():
				title = form.cleaned_data.get('title')
				composition = form.cleaned_data.get('composition')
				try:
					post = Post.objects.create(user=request.user, datetime=timezone.now(), title=title, composition=composition)
					post.writeOnChain()
				except ValueError:
					post.delete()
					alert = 'Per motivi di spamming, non è consentito postare troppo velocemente. Riprova tra qualche secondo.'
				else:
					post.save()
					success = 'Content created!'
	else:
		form = PostForm(initial=initial_data)
	return render(request, 'api/api_new_post.html', {'form': form,
													 'alert': alert,
													 'success': success,
													 'message': message,})

@login_required()
def detail_post_view(request, id):
	post = get_object_or_404(Post, id=id)
	context = {'post': post}
	return render(request, 'api/api_detail_post.html', context)
