from pyexpat import model
from random import choices
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.forms import ModelForm
from decrees.models import MyUser
from django import forms

from decrees.models import Event, Person, Position


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = MyUser
        fields = ['username']


class CustomUserChangeForm(UserChangeForm):

    class Meta:
        model = MyUser
        # fields = ['username']

        # fields = UserChangeForm.Meta.fields# + ('location_2',)
        fields = '__all__'


class TestUserForm(ModelForm):
    class Meta:
        model = MyUser
        fields = ('username','password', 'email')



from django import forms
from django.template import loader
from django.utils.safestring import mark_safe



class MyWidget(forms.Widget):
    template_name = "django/my_forms/my_text_area.html"

    def get_context(self, name, value, attrs=None):
        return {'widget': {
            'name': name,
            'value': value,
        }}

    def render(self, name, value, attrs=None, renderer=None): 
        context = self.get_context(name, value, attrs)

        template = loader.get_template(self.template_name).render(context)
        return mark_safe(template)


# class MyTextArea(forms.Textarea):
#     template_name = "django/my_forms/my_text_area.html"

    # def get_context(self, name, value, attrs=None):
    #     # breakpoint()
    #     return {'widget': {
    #         'name': name,
    #         'value': value,
    #         'placeholder':'aaaaaaa'
    #     }}

    # def render(self, name, value, attrs=None, renderer=None):
    #     context = self.get_context(name, value, attrs)
    #     # return self._render(self.template_name, context, renderer)

    #     template = loader.get_template(self.template_name).render(context)
    #     return mark_safe(template)

    # def __init__(self, attrs):
    #     # Use slightly better defaults than HTML's 20x2 box
    #     # breakpoint()
    #     default_attrs = {'cols': '40', 'rows': '10'}
    #     # if attrs:
    #     #     default_attrs.update(attrs)
    #     super().__init__(attrs)

class CustomDatePicker(forms.DateInput):
    r"""
    сделан с помощью FengyuanChenDatePickerInput. подключен через cdn. 
    сам скрипт лежит в C:\Users\ironb\прогр\LEARN_PYTHON\my_django\mysite\converter\templates
    
    """
    template_name = 'date_picker.html'

    # person = forms.CharField(widget=MyWidget)
    # person = forms.CharField(widget=MyTextArea(label='лейбл', attrs={'placeholder':'my_val', 'size': 10, 'title': 'Your name'}))
    
    # action = forms.ChoiceField(choices=Event.event_choices, widget=forms.Select(attrs=select_atrs), label='Тип события')

#    line = forms.CharField(widget=forms.Textarea(attrs=form_control))



class EventForm(forms.ModelForm):
    form_control = {'class':"form-control",'rows':5}
    select_atrs = {"class":"form-select form-select-lg mb-3", 'aria-label':".form-select-lg example"}
    action = forms.ChoiceField(choices=Event.event_choices, widget=forms.RadioSelect(attrs=select_atrs), label='Тип события')
    person = forms.CharField(widget=forms.TextInput(attrs=form_control))
    position = forms.CharField(widget=forms.Textarea(attrs=form_control))

    line = forms.CharField(widget=forms.Textarea())
    full_text = forms.CharField(widget=forms.Textarea())
    
    date = forms.DateTimeField(
        input_formats=['%d/%m/%Y %H:%M'], 
        widget=CustomDatePicker(attrs={'class':'form-control'})
    )

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({'placeholder':f'вводить тут {field}'})
            

    class Meta:
        model = Event
        fields = '__all__'


class MyTextArea(forms.Textarea):
    pass
    # def get_context(self, name, value, attrs=None):
    #     pers_name = Person.objects.filter(pk=value)[0].name
        
    #     return {'widget': {
    #         'name': name,
    #         'value': pers_name,
    #     }}
# get a way to log the errors:
import logging
log = logging.getLogger(__name__)
# convert the errors to text
from django.utils.encoding import force_str

class Event_form_for_Admin(forms.ModelForm):
    # person = forms.ModelChoiceField(label='ФИО', queryset=None)
    # position = forms.ModelChoiceField(label='должность', queryset=None)
    
    def is_valid(self):
        breakpoint()
        log.warning(force_str(self.errors))
        return super(Event_form_for_Admin, self).is_valid()

    class Meta:
        model = Event
        fields = ['person','position']



# 'full_text', 
# full_text = forms.CharField(widget=forms.Textarea, label='полный текст')

    # action = forms.ChoiceField(choices=Event.event_choices, label='Тип события')
    # person = forms.CharField()
    # position = forms.CharField() 

'''
когда связи -- кастомная МОДЕЛЬ ФОРМ не подходит
а обычная -- подходит
редактирование
'''


class EditName():
    pass


class NewEventForm(forms.Form):
    
    form_control = {'class':"form-control",'rows':5}
    big_form_control = {'class':"form-control",'rows':15}
    
    select_atrs = {"class":"form-select form-select-lg mb-3", 'aria-label':".form-select-lg example"}
 
    person = forms.CharField(widget=forms.TextInput(attrs=form_control))
 
    date = forms.DateTimeField(required=False,
    input_formats=['%d/%m/%Y %H:%M'], 
    widget=CustomDatePicker(attrs={'class':'form-control', 'placeholder':'дата'})
        )

    action = forms.ChoiceField(choices=Event.event_choices, widget=forms.RadioSelect(attrs=select_atrs), label='Тип события')
    position = forms.CharField(widget=forms.Textarea(attrs=form_control))
    full_text = forms.CharField(widget=forms.Textarea(attrs=big_form_control))
    link = forms.CharField()

    region = forms.ChoiceField(widget=forms.Select, choices=Event.event_choices)

class NewEventForm_DisabledFields(NewEventForm): 
    # выключаем все формы
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for e in self.fields:
            try:
                self.fields[e].widget.attrs["readonly"] = True        
            except Exception as ex:
                print(ex)


# from django.forms import formset_factory
# EventFormSet = formset_factory(EventForm, extra=3)