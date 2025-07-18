from django.shortcuts import render, get_object_or_404

from pages.models import Quote


def quotes(request):
	quotes = Quote.objects.filter(make_public=True).order_by('-created_at')
	return render(request, 'pages/index.html', {'quotes': quotes})

def quote_list(request):
	quotes = Quote.objects.filter(make_public=True).order_by('-created_at')
	return render(request, 'pages/list.html', {'quotes': quotes})

def quote_detail(request, id):
	quote = get_object_or_404(Quote, id=id, make_public=True)
	quote.views += 1
	quote.save()
	return render(request, 'pages/detail.html', {'quote': quote})