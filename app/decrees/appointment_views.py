
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.http import Http404
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy, reverse
import json
from django.contrib.auth.mixins import LoginRequiredMixin

from typing import *

# from django.contrib.auth import get_user_model
# User = get_user_model()

from django.contrib.auth.views import LoginView
from django.contrib.auth.mixins import LoginRequiredMixin
# from django.contrib.auth.forms import UserCreationForm
from django.views.generic import FormView, ListView, DetailView
from django.contrib.auth import login
from decrees.models import Event, Person, Position
from decrees.forms import EventForm, NewEventForm, NewEventForm_DisabledFields
from django.contrib.auth import authenticate


class MyLogin(LoginView):
    template_name = 'decrees/decrees/login.html'
    
    def get_success_url(self): 
        return reverse_lazy('decrees:show-all-events')


class EventView(FormView):
    template_name = 'decrees/event_form.html'
    form_class = EventForm
    # form_class = EventFormSet
    success_url = reverse_lazy('decrees:show_all_docs')


class AddEvent(CreateView):
    template_name = 'decrees/event_form.html'
    model = Event
    form_class = EventForm
    success_url = reverse_lazy('decrees:show_all_docs')
    

    def post(self, request, *args, **kwargs):
        form_data = request.POST.dict()

        position_from_user = form_data.get('position')
        position_obj, _ = Position.objects.get_or_create(name=position_from_user)

        person_from_user = form_data.get('person')
        person_obj, _ = Person.objects.get_or_create(name=person_from_user)
        
        form_data.update({'person':person_obj, 'position':position_obj})
        my_dic = {k:v for k,v in form_data.items() if k in dir(Event)}
        ev = Event(**my_dic)
        ev.save()
        return HttpResponse('ok')

class EditEvent(LoginRequiredMixin,UpdateView):

    def __init__(self, *args, **kwargs):
        if 'model_form' in kwargs.keys():
            self.form_class = kwargs['model_form']
        super().__init__(*args, **kwargs)

    template_name = 'decrees/decrees/update_event_form.html'
    model = Event
    form_class = NewEventForm
    

    def get(self, request, *args, **kwargs) -> HttpResponse:
        
        # disable_fields = ''
        # if 'update' not in self.request.get_full_path():
        #     disable_fields = 'disabled'

        event_id = self.kwargs.get('pk')
        event_obj = Event.objects.filter(pk=event_id)
        if not event_obj.exists():
            return HttpResponse('нет такого айди ивента')
        event_obj = event_obj[0]
        person = event_obj.person.name
        position = event_obj.position
        date = event_obj.date
        action = event_obj.action
        full_text = event_obj.full_text
        link = event_obj.link

        data = {
            'person':person,
            'position':position,
            'date':date,
            'action':action,
            'full_text':full_text,
            
        }

        form = self.form_class(data)
        return render(request, 'decrees/decrees/update_event_form.html', {'form':form, 'download_link':link})
        

    def post(self, request, *args, **kwargs) -> HttpResponse:
        
        form_data = request.POST.dict()

        event_id = self.kwargs.get('pk')
        event_obj = Event.objects.filter(pk=event_id)
        if not event_obj.exists():
            return HttpResponse('нет такого айди ивента')
        
        event_obj = event_obj[0]
        
        person_obj = event_obj.person
        person_obj.name = form_data['person']
        person_obj.save()
    
        position_obj = event_obj.position
        position_obj.name = form_data['position']
        position_obj.save()
        

        return redirect('decrees:update-event', pk=event_id) 

class ShowOneEvent(EditEvent):

    def __init__(self, *args, **kwargs):
        print('args---', args, kwargs)
        super().__init__(model_form=NewEventForm_DisabledFields,*args, **kwargs)



# class ShowOneEvent(DetailView):
#     template_name = 'decrees/decrees/show_one_event.html'
#     model = Event
#     context_object_name = 'event'
        
#     def get_queryset(self, *args, **kwargs):
#         pk = self.kwargs['pk']
#         ev = Event.objects.filter(pk=pk)
#         return ev
    

# 
class ShowAllEvents(LoginRequiredMixin, ListView):
    '''    ЛОГИРОВАНИЕ СЮДА НАПРАВЛЯЕТ ВСЕ ОК, НО ТУТ ПОЧЕМУ-ТО ЮЗЕР НЕ ЗАЛОГИНЕН
        вот эти два надо настроитьы
    '''
    login_url = 'decrees:login'

    model = Event
    template_name = 'decrees/decrees/test_menu.html'
    fields = '__all__'
    context_object_name = 'events'
    paginate_by = 5
    
    def get_queryset(self):
        region_query = self.request.GET.get('region-search','')
        user_name_query = self.request.GET.get('name-search','')
        user_name_query = user_name_query.capitalize()
        action_query = self.request.GET.get('action_option')
        position_query = self.request.GET.get('position-search')
        date_from = self.request.GET.get('date_from')
        date_to = self.request.GET.get('date_to')

        filtered_events = Event.objects.all()
        # breakpoint()
        if user_name_query:
            filtered_events = filtered_events.filter(
                person__name__contains=user_name_query)

        if region_query:
            filtered_events = filtered_events.filter(region=region_query)

        if action_query:
            filtered_events = filtered_events.filter(action=action_query)
        
        if position_query:
            filtered_events = filtered_events.filter(line__contains=position_query)
        
        if date_from:
            filtered_events = filtered_events.filter(date__gte=date_from)
        if date_to:
            filtered_events = filtered_events.filter(date__lte=date_to)
        
        if filtered_events:
            for i, e in enumerate(filtered_events):
                e.__setattr__('row_number',i+1)

        return filtered_events 


    def get_context_data(self, **kwargs):
        # добавляет контекста, который можно юзать в темплейтах
        context = super().get_context_data(**kwargs)
        regions = json.load(open('decrees/regions.json', 'r'))
        regions += ['Федеральный уровень']
        context.update({'regions':regions})

        region_query = self.request.GET.get('region-search','')
        user_name_query = self.request.GET.get('name-search','')
        user_name_query = user_name_query.capitalize()
        action_query = self.request.GET.get('action_option')
        date_from = self.request.GET.get('date_from')
        date_to = self.request.GET.get('date_to')

        context.update({
            'region_query':region_query, 
            'user_name_query':user_name_query,
            'action_query':action_query,
            'date_from':date_from,
            'date_to':date_to,

        })
        return context

def test(r):
    return render(r, 'decrees/decrees/show_all_events_test.html')


    # def __get_context_data(self, **kwargs):
    #     regions = json.load(open('decrees/regions.json', 'r'))
    #     regions += ['Федеральный уровень']
        
    #     context = super().get_context_data(**kwargs)
    #     context.update({'regions':regions})

    #     region_query = self.request.GET.get('region-search','')
    #     user_name_query = self.request.GET.get('name-search','')
    #     user_name_query = user_name_query.capitalize()
        
    #     filtered_events = Event.objects.all()

    #     if user_name_query:
    #         filtered_events = filtered_events.filter(
    #             person__name__contains=user_name_query)

    #     if region_query:
    #         filtered_events = filtered_events.filter(region=region_query)

    #     # if filtered_events.exists():
    #     context['events'] = filtered_events 

    #     # breakpoint()

    #     return context
        
    # def get_queryset(self):
    #     events = Event.objects.all()
    #     # breakpoint()
    #     return events
    #     breakpoint()
    #     user_name_query = self.request.args['']
    #     event = Event.objects.filter(pk=5)
    #     return event
    #     # return super().get_queryset()
