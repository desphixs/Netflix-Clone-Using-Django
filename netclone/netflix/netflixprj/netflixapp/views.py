import imp
from django.shortcuts import redirect, render
from django.views import View
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from . forms import ProfileForm
from . models import Profile, Movie

class Home(View):
    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('netflixapp:profile-list')
        return render(request, 'index.html')

method_decorator(login_required, name='dispatch')
class ProfileList(View):
    def get(self, request, *args, **kwargs):
        
        profiles = request.user.profiles.all()

        context = {
            'profiles':profiles
        }
        return render(request, 'profilelist.html', context)

method_decorator(login_required, name='dispatch')
class ProfileCreate(View):
    def get(self, request, *args, **kwargs):
        form = ProfileForm()
        context = {
            'form':form
        }
        return render(request, 'profilecreate.html', context)

    def post(self, request, *args, **kwargs):
        form = ProfileForm(request.POST or None)
        if form.is_valid():
            profile = Profile.objects.create(**form.cleaned_data)
            if profile:
                request.user.profiles.add(profile)
                return redirect('netflixapp:profile-list')
        context = {
            'form':form
        }
        return render(request, 'profilecreate.html', context)

method_decorator(login_required, name='dispatch')
class MovieList(View):
    def get(self, request, profile_id, *args, **kwargs):
        try:
            profile = Profile.objects.get(uuid=profile_id)
            movies = Movie.objects.filter(age_limit=profile.age_limit)
            if profile not in request.user.profiles.all():
                return redirect('netflixapp:profile-list')

            context = {
            'movies':movies
            }

            return render(request, 'movielist.html', context)
        except Profile.DoesNotExist:
            return redirect('netflixapp:profile-list')

method_decorator(login_required, name='dispatch')
class MovieDetail(View):
    def get(self, request, movie_id, *args, **kwargs):
        try:
            movie = Movie.objects.get(uuid=movie_id)
            
            context = {
                'movie':movie
            }

            return render(request, 'moviedetail.html', context)
        except Movie.DoesNotExist:
            return redirect('netflixapp:profile-list')

method_decorator(login_required, name='dispatch')
class PlayMovie(View):
    def get(self, request, movie_id, *args, **kwargs):
        try:
            movie = Movie.objects.get(uuid=movie_id)
            movie = movie.video.values()
            
            context = {
                'movie':list(movie)
            }

            return render(request, 'playmovie.html', context)
        except Movie.DoesNotExist:
            return redirect('netflixapp:profile-list')