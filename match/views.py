from .models import Match
from django.shortcuts import render, get_object_or_404, redirect
from django.views.decorators.http import require_POST
from .forms import  SearchForm, CommentForm
from django.contrib.postgres.search import SearchVector, SearchQuery, SearchRank
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from accounts.models import Profile
from datetime import date


def match_list(request):
    now = timezone.now()
    matches = Match.objects.filter(date__gt=now)
    return render(request,
                  'match/match/list.html',
                  {'matches': matches})


def match_detail(request, id):
    match = get_object_or_404(Match,
                              id=id)
    players = match.players.all()
    comments = match.comments.filter(active=True)
    form = CommentForm()
    return render(request,
                  'match/match/detail.html',
                  {'match': match,
                   'players': players,
                   'comments': comments,
                   'form': form})


@require_POST
def match_comment(request, match_id):
   match = get_object_or_404(Match,
                             id=match_id,)
   comment = None
   form = CommentForm(data=request.POST)
   if form.is_valid():
        comment = form.save(commit=False)
        comment.match = match
        comment.save()
   return render(request, 'match/match/comment.html',
                   {'match': match,
                     'form': form,
                     'comment': comment})


def match_search(request):
    form = SearchForm()
    query = None
    results = []

    if 'query' in request.GET:
        form = SearchForm(request.GET)
        if form.is_valid():
            query = form.cleaned_data['query']
            search_vector = SearchVector('title', 'date', config='russian')
            search_query = SearchQuery(query, config='russian')
            results = Match.objects.annotate(
                search=search_vector,
                rank=SearchRank(search_vector, search_query)
            ).filter(search=search_query).order_by('-rank')

    return render(request,
                  'match/match/search.html',
                  {'form': form,
                   'query': query,
                   'results': results})


@login_required
def join_match(request, match_id):
    match = get_object_or_404(Match, id=match_id)
    profile = request.user.profile

    if profile in match.players.all():
        messages.warning(request, 'Вы уже присоединились к этому матчу.')
        return redirect('match:match_detail', id=match_id)
    else:
        match.players.add(profile)
        messages.success(request, 'Вы успешно присоединились к матчу.')
        return redirect('match:match_detail', id=match_id)


def past_matches(request):
    now = timezone.now()
    past_matches = Match.objects.filter(date__lt=now).order_by('-date')
    return render(request, 'match/match/past_matches.html', {'matches': past_matches})


def profile_list(request):
    profiles = Profile.objects.all().order_by('-goals')
    return render(request, 'match/match/profile_list.html', {'profiles': profiles})
