from django.shortcuts import render

# Create your views here.
from typing import Any, Dict
from django.shortcuts import render,redirect
# Create your views here.
from django import http
from django.http import HttpRequest,HttpResponse
from django.views.generic import TemplateView,UpdateView,DeleteView
from django.contrib.auth import authenticate,login,logout
from django.urls import reverse
from .forms import *
from django.urls import reverse_lazy
from django.core.paginator import Paginator
from django.http import Http404
from django.shortcuts import get_object_or_404
from django.db import DatabaseError
from django.contrib import messages
import logging
logger = logging.getLogger(__name__)
from django.http.response import JsonResponse



#loginrequiredmixin 
class LoginRequiredMixin(object):
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            pass
        else:
            return redirect(reverse('musicapp:admin_login'))

        return super(LoginRequiredMixin,self).dispatch(request, *args, **kwargs)
    

class RegisterView(TemplateView):
    template_name = 'user-register.html'
    success_url = reverse_lazy('musicapp:admin_login')  # Replace with your actual login URL pattern

    def get(self, request, *args, **kwargs):
        form = UserRegisterForm()
        return render(request, self.template_name, {'form': form})
    def post(self, request, *args, **kwargs):
        form = UserRegisterForm(request.POST)
        if form.is_valid():
        # Proceed with user creation
            user = User.objects.create(
                username=form.cleaned_data.get('username'),
                email=form.cleaned_data.get('email')  # Assuming you meant to use the username as email
            )
            user.set_password(form.cleaned_data.get('password'))
            user.save()
            login(self.request, user)
            messages.success(request, 'Your account has been created and you are logged in!')
            return redirect(self.success_url)
        else:
            # Log form errors to the console
            print(form.errors)  # Add this line
            return render(request, self.template_name, {'form': form})



#for loginView
class AdminLoginView(TemplateView):
    template_name = 'login.html'

    def post(self,request, *args, **kwargs):
        loginform =LoginForm(request.POST)
        if loginform.is_valid():

            username=loginform.cleaned_data.get('username')
            password=loginform.cleaned_data.get('password')
            user = authenticate(username = username, password = password)
            if user:
                login(request,user)
                return redirect("musicapp:songs_list")
            else:
                return render(request,self.template_name,{"errors":"invalid username"})
                
        else:
            print(loginform.errors)

            return render(request,self.template_name,{"errors":"invalid username"})



class AdminLogoutView(TemplateView):
    def get(self,request):
        logout(request)
        return redirect('musicapp:admin_login')


# class HomeView(TemplateView):
#     template_name ='home.html'


        #singer View
class SingerAddView(TemplateView):
    template_name = 'singeradd.html'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        context['forms'] = SingerForm()  # It's better to instantiate the form here
        return context

    def post(self, request, *args, **kwargs):
        form = SingerForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                # Try saving the form and catching database-related errors
                form.save()
                return redirect('musicapp:singer_list')
            except DatabaseError as e:
                # Handle database errors
                return render(
                    request, 
                    self.template_name, 
                    {'forms': form, 'msg_errors': f"Database error occurred: {str(e)}"}
                )
            except Exception as e:
                # Handle any other unexpected errors
                return render(
                    request, 
                    self.template_name, 
                    {'forms': form, 'msg_errors': f"An unexpected error occurred: {str(e)}"}
                )
        else:
            # Return form errors if the form is not valid
            return render(
                request, 
                self.template_name, 
                {'forms': form, 'msg_errors': 'Sorry! Please try again.'}
            )


            #for list
class SingerListView(LoginRequiredMixin,TemplateView):
    template_name = 'singerlist.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        try:
            singerlist = Singer.objects.all()  # Fetch all singers
            paginator = Paginator(singerlist, 2)  # Show 2 singers per page
            page_number = self.request.GET.get('page')  # Use self.request to access the request object
            singer_data_final = paginator.get_page(page_number)  # Get paginated results
            total_pages = singer_data_final.paginator.num_pages  # Get total number of pages

            # Add data to the context
            context['singerlist'] = singer_data_final  # Paginated singer list
            context['lastpage'] = total_pages
            context['totalpagelist'] = [n + 1 for n in range(total_pages)]  # List of total pages

        except Singer.DoesNotExist:
            context['singerlist'] = None
            context['error'] = "No singers found."
        except Exception as e:
            context['singerlist'] = None
            context['error'] = f"An error occurred: {str(e)}"

        return context


        #for detail
class SingerDetailView(TemplateView):
    template_name = 'singerdetail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        s_id = self.kwargs.get('id')
        
        try:
            # Fetch singer object
            singer_obj = Singer.objects.get(id=s_id)

            # Increment the view count
            singer_obj.view_count += 1
            singer_obj.save()

            # Add singer detail to context
            context['singer_detail'] = singer_obj




            # Fetch songs related to the singer
            songs = Songs.objects.filter(singer=singer_obj)
            paginator = Paginator(songs,2)
            page_number = self.request.GET.get('page')
            songs_data_final = paginator.get_page(page_number)
            total_page = songs_data_final.paginator.num_pages

            context['songs_detail'] = songs_data_final
            context['lastpage'] = total_page
            context['totalpagelist'] = [n+1 for n in range(total_page)]

        except Singer.DoesNotExist:
            raise Http404("Singer not found")
        
        except Songs.DoesNotExist:
            context['songs_detail'] = None  # Handle case where no songs are found
            context['error'] = "No songs found for this singer."

        except Exception as e:
            context['error'] = f"An error occurred: {str(e)}"
            context['singer_detail'] = None
            context['songs_detail'] = None

        return context

    

        ####singer update view
class SingerUpdateView(TemplateView):
    template_name = 'singeradd.html'  # Reusing the same template for add and update

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        s_id = self.kwargs.get('id')
        singer = get_object_or_404(Singer, id=s_id)  # Fetch the singer object or return 404
        context['forms'] = SingerForm(instance=singer)  # Pre-populate the form with the singer's data
        return context

    def post(self, request, *args, **kwargs):
        s_id = self.kwargs.get('id')
        singer = get_object_or_404(Singer, id=s_id)
        form = SingerForm(request.POST, request.FILES, instance=singer)  # Bind form with instance for update
        
        if form.is_valid():
            try:
                form.save()  # Save the updated singer data
                return redirect('musicapp:singer_list')  # Redirect to the list of singers after successful update
            except DatabaseError as e:
                return render(
                    request, 
                    self.template_name, 
                    {'forms': form, 'msg_errors': f"Database error occurred: {str(e)}"}
                )
            except Exception as e:
                return render(
                    request, 
                    self.template_name, 
                    {'forms': form, 'msg_errors': f"An unexpected error occurred: {str(e)}"}
                )
        else:
            # If form is not valid, return with errors
            return render(
                request, 
                self.template_name, 
                {'forms': form, 'msg_errors': 'Please correct the errors below.'}
            )


        #for delete
class SingerDeleteView(TemplateView):
    template_name = 'singerdelete.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        d_id = self.kwargs.get('id')
        singer = get_object_or_404(Singer, id=d_id)  # Fetch the singer object or return 404 if not found
        context['objects'] = singer
        return context

    def post(self, request, *args, **kwargs):
        a_id = self.kwargs.get('id')
        singer = get_object_or_404(Singer, id=a_id)  # Safely get the singer object
        try:
            singer.delete()  # Attempt to delete the singer
            return redirect('musicapp:singer_list')  # Redirect to singer list after successful deletion
        except DatabaseError as e:
            # Handle any database errors that occur during deletion
            return render(
                request, 
                self.template_name, 
                {'objects': singer, 'msg_errors': f"Database error occurred: {str(e)}"}
            )
        except Exception as e:
            # Handle any unexpected exceptions
            return render(
                request, 
                self.template_name, 
                {'objects': singer, 'msg_errors': f"An unexpected error occurred: {str(e)}"}
            )


                #for musicadd
class MusicianAddView(TemplateView):
    template_name = 'musicianadd.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = MusicianForm()  # Instantiate the form
        return context

    def post(self, request, *args, **kwargs):
        form = MusicianForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                form.save()  # Attempt to save the form data
                return redirect('musicapp:musician_list')  # Redirect upon successful save
            except DatabaseError as e:
                # Handle database errors
                return render(
                    request, 
                    self.template_name, 
                    {'form': form, 'msg_error': f"Database error occurred: {str(e)}"}
                )
            except Exception as e:
                # Handle any other unexpected errors
                return render(
                    request, 
                    self.template_name, 
                    {'form': form, 'msg_error': f"An unexpected error occurred: {str(e)}"}
                )
        else:
            # If the form is not valid, return the form with errors
            return render(
                request, 
                self.template_name, 
                {'form': form, 'msg_error': 'Sorry! Invalid form data.'}
            )


            #for list
class MusicianListView(LoginRequiredMixin, TemplateView):
    template_name = 'musicianlist.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        try:
            # Fetch all musicians, optionally order them
            musicians = Musician.objects.all().order_by('name')
            
            # Pagination with 10 musicians per page
            paginator = Paginator(musicians, 4)
            page_number = self.request.GET.get('page')
            musician_page = paginator.get_page(page_number)
            
            context['musicianlist'] = musician_page
            context['lastpage'] = paginator.num_pages
            context['totalpagelist'] = [n+1 for n in range(paginator.num_pages)]
        except DatabaseError as e:
            # Handle database errors gracefully
            context['error'] = f"Database error: {str(e)}"
            context['musicianlist'] = []
        
        return context



        #for detail
class MusicianDetailView(TemplateView):
    template_name = 'musiciandetail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        music_id = self.kwargs.get('id')

        try:
            # Fetch musician details
            detail = Musician.objects.get(id=music_id)
            context['musician_obj'] = detail
            
            # Fetch songs associated with the musician
            music = Songs.objects.filter(musician=detail)
            context['music_detail'] = music
            
        except Musician.DoesNotExist:
            context['musician_obj'] = None
            context['error'] = "Musician not found."
        
        except Songs.DoesNotExist:
            context['music_detail'] = None
            context['error'] = "No songs found for this musician."
        
        except Exception as e:
            context['error'] = f"An unexpected error occurred: {str(e)}"
            context['musician_obj'] = None
            context['music_detail'] = None

        return context


        #for update
class MusicianUpdateView(TemplateView):
    template_name = 'musicianadd.html'
     
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        music_id = self.kwargs.get('id')
        
        try:
            # Fetch the musician to be updated
            m_about = Musician.objects.get(id=music_id)
            context['form'] = MusicianForm(instance=m_about)
        except Musician.DoesNotExist:
            context['form'] = None
            context['error'] = "Musician not found."
        
        return context
    
    def post(self, request, *args, **kwargs):
        music_id = self.kwargs.get('id')
        
        try:
            # Fetch the musician to be updated
            m_about = Musician.objects.get(id=music_id)
            about = MusicianForm(request.POST, request.FILES, instance=m_about)
            
            if about.is_valid():
                about.save()
                return redirect('musicapp:musician_list')
            else:
                return render(request, self.template_name, {'form': about, 'msg_error': 'Form is not valid.'})
        
        except Musician.DoesNotExist:
            return render(request, self.template_name, {'form': request.POST, 'msg_error': 'Musician not found.'})
        
        except DatabaseError as e:
            return render(request, self.template_name, {'form': request.POST, 'msg_error': f"Database error occurred: {str(e)}"})
        
        except Exception as e:
            return render(request, self.template_name, {'form': request.POST, 'msg_error': f"An unexpected error occurred: {str(e)}"})


        #for delete
class MusicianDeleteView(TemplateView):
    template_name = 'musiciandelete.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        music_id = self.kwargs.get('id')

        try:
            # Fetch the musician to be deleted
            m_about = Musician.objects.get(id=music_id)
            context['sanju'] = m_about
        except Musician.DoesNotExist:
            context['sanju'] = None
            context['error'] = "Musician not found."
        
        return context
    
    def post(self, request, *args, **kwargs):
        music_id = self.kwargs.get('id')

        try:
            # Fetch and delete the musician
            music = Musician.objects.get(id=music_id)
            music.delete()
            return redirect('musicapp:musician_list')

        except Musician.DoesNotExist:
            return render(request, self.template_name, {'error': 'Musician not found.'})

        except DatabaseError as e:
            return render(request, self.template_name, {'error': f"Database error occurred: {str(e)}"})

        except Exception as e:
            return render(request, self.template_name, {'error': f"An unexpected error occurred: {str(e)}"})



        # for songs add
class SongsAddView(TemplateView):
    template_name = 'songsadd.html'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        a_id = self.kwargs.get('id')

        try:
            # Fetch the singer
            singer = Singer.objects.get(id=a_id)
            context['singer_name'] = singer
        except Singer.DoesNotExist:
            context['singer_name'] = None
            context['error'] = "Singer not found."
        
        context['forms'] = SongsForm

        return context
    
    def post(self, request, *args, **kwargs):
        form = SongsForm(request.POST)
        s_id = self.kwargs.get('id')

        try:
            # Fetch the singer and attach it to the form instance
            singer_obj = Singer.objects.get(id=s_id)
            form.instance.singer = singer_obj
            
            if form.is_valid():
                form.save()
                return redirect('musicapp:singer_detail', singer_obj.id)
            else:
                return render(request, self.template_name, {'forms': form, 'msg_errors': 'Sorry! Invalid form data.'})

        except Singer.DoesNotExist:
            return render(request, self.template_name, {'forms': form, 'msg_errors': 'Singer not found.'})

        except DatabaseError as e:
            return render(request, self.template_name, {'forms': form, 'msg_errors': f"Database error occurred: {str(e)}"})

        except Exception as e:
            return render(request, self.template_name, {'forms': form, 'msg_errors': f"An unexpected error occurred: {str(e)}"})


            #for songs add2
class  songsAdd2View(TemplateView):
    template_name = 'songsadd.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['forms'] = SongsForm

        return context
    
    def post(self,request,*args,**kwargs):
        form = SongsForm(request.POST,request.FILES)
        if form.is_valid():
            form.save()
        else:
            return render(request,self.template_name,{'forms':form,'msg_error':'sorry! invalid'})
        
        return redirect('musicapp:songs_list')
    


        #for list
class SongsListView(TemplateView):
    template_name = 'songslist.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        try:
            logger.debug("Fetching songs list.")

            songslist = Songs.objects.all()  # Fetch all singers
            paginator = Paginator(songslist, 6)  # Show 2 singers per page
            page_number = self.request.GET.get('page')  # Use self.request to access the request object
            songs_data_final = paginator.get_page(page_number)  # Get paginated results
            total_pages = songs_data_final.paginator.num_pages  # Get total number of pages

            # Add data to the context
            context['songs_list'] = songs_data_final  # Paginated singer list
            context['lastpage'] = total_pages
            context['totalpagelist'] = [n + 1 for n in range(total_pages)]  # List of total pages

        except Songs.DoesNotExist:
            context['songs_list'] = None
            context['error'] = "No songs found."
        except Exception as e:
            context['songs_list'] = None
            context['error'] = f"An error occurred: {str(e)}"

        return context


            #for update
class SongUpdateView(TemplateView):
    template_name = 'songsadd.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        s_id = self.kwargs.get('id')

        try:
            # Fetch the song to be updated
            song_obj = Songs.objects.get(id=s_id)
            context['forms'] = SongsForm(instance=song_obj)
        except Songs.DoesNotExist:
            context['forms'] = None
            context['error'] = "Song not found."

        return context
    
    def post(self, request, *args, **kwargs):
        s_id = self.kwargs.get('id')

        try:
            # Fetch the song to be updated
            song_form = Songs.objects.get(id=s_id)
            song = SongsForm(request.POST, request.FILES, instance=song_form)

            if song.is_valid():
                song.save()
                return redirect('musicapp:songs_list')
            else:
                return render(request, self.template_name, {'forms': song, 'msg_errors': 'Sorry! Invalid form data.'})

        except Songs.DoesNotExist:
            return render(request, self.template_name, {'forms': request.POST, 'msg_errors': 'Song not found.'})

        except DatabaseError as e:
            return render(request, self.template_name, {'forms': request.POST, 'msg_errors': f"Database error occurred: {str(e)}"})

        except Exception as e:
            return render(request, self.template_name, {'forms': request.POST, 'msg_errors': f"An unexpected error occurred: {str(e)}"})


            # for delete
class SongDeleteView(TemplateView):
    template_name = 'songsdelete.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        songs_id = self.kwargs.get('id')

        try:
            # Fetch the song to be deleted
            s_about = Songs.objects.get(id=songs_id)
            context['delete_songs'] = s_about
        except Songs.DoesNotExist:
            raise Http404("Song not found.")
        except Exception as e:
            context['error'] = f"An unexpected error occurred: {str(e)}"
            context['delete_songs'] = None
        
        return context

    def post(self, request, *args, **kwargs):
        delete_id = self.kwargs.get('id')

        try:
            # Fetch the song to be deleted
            song = Songs.objects.get(id=delete_id)
            song.delete()

            return redirect('musicapp:songs_list')
        
        except Songs.DoesNotExist:
            return render(request, self.template_name, {'msg_errors': 'Song not found.'})

        except DatabaseError as e:
            return render(request, self.template_name, {'msg_errors': f"Database error occurred: {str(e)}"})

        except Exception as e:
            return render(request, self.template_name, {'msg_errors': f"An unexpected error occurred: {str(e)}"})
