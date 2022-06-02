# from django.shortcuts import get_object_or_404, redirect, render
# from django.urls import reverse
# from django.http import Http404
# from django.http import HttpResponse, HttpResponseRedirect
# from django.shortcuts import get_object_or_404
# from django.views.generic.edit import CreateView, UpdateView, DeleteView
# from django.urls import reverse_lazy, reverse


# # from django.contrib.auth import get_user_model
# # User = get_user_model()

# from django.contrib.auth.views import LoginView
# from django.contrib.auth.mixins import LoginRequiredMixin
# # from django.contrib.auth.forms import UserCreationForm
# from django.views.generic import FormView
# from django.contrib.auth import login
# from decrees.forms import CustomUserCreationForm, TestUserForm


# from .models import Formats, Document


# """ООП"""

# from django.views.generic.list import ListView
# from django.views.generic.base import TemplateView, RedirectView
# from django.views.generic.detail import DetailView

# class MyLogin(LoginView):
#     fields = ['__all__'] 
#     template_name = 'converter/log-in-form.html'
#     redirect_authenticated_user = True

#     def get_success_url(self): 
#         return reverse_lazy('converter:show_all_docs')


# class MyRedirect(RedirectView):
    
#     pattern_name = 'converter:show_all_docs'
#     query_string = True

#     def get_redirect_url(self, *args, **kwargs):
#         print('перенаправляем!')
#         # print('kwargs---', kwargs)
#         # kwargs = {'mykwargs': kwargs['arg']}
#         return reverse('converter:show_all_docs')

# class MyTemplateView(TemplateView):
#     template_name = 'converter/template.html'

#     """    
#     в оригинале так:
#     def get(self, request, *args, **kwargs):
#          context = self.get_context_data(**kwargs)
#          return self.render_to_response(context)
    
#     и можно переписать
#     """

#     def get(self, *args, **kwargs):
#         r = locals()['args'][0]
#         return render(r, self.template_name, kwargs)

#     # получить контекст (параметры)
#     # def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:con
#         # return super().get_context_data(**kwargs)


# # def authenticate(r):
# #     from django.contrib.auth import authenticate
# #     user = authenticate(username='john', password='secret')
# #     if user is not None:
# #         pass
# #         # A backend authenticated the credentials
# #     else:
# #         # No backend authenticated the credentials
# #         pass

# # def login_form(r):
# #     # МНЕ НАДО
# #     return render(r, 'converter/log-in-form.html')


# # моя логин форма содержит какой то кал
# '''            {% with messages = get_flashed_messages(with_categories=true) %}

#             {% endwith %}
# '''


# class Created(TemplateView):
#     template_name = 'converter/docs/doc_created.html'
    
#     def get(self, *args, **kwargs):
#         r = locals()['args'][0]
#         return render(r, self.template_name, kwargs)


# class AddDoc(CreateView):
#     template_name = 'converter/docs/doc_created.html'
#     model = Document
#     fields = ['doc_name', 'doc_format', 'size']
#     success_url = reverse_lazy('converter:created')


# class UpdateDoc(UpdateView):
#     context_object_name = 'doc'
#     template_name = 'converter/docs/update_doc.html'
#     model = Document
#     fields = ['doc_name']
#     # fields = '__all__'
#     success_url = reverse_lazy('converter:created')


# class DeleteDoc(DeleteView):
#     context_object_name = 'doc'
#     model = Document
#     template_name = 'converter/docs/cofirm_delete.html'
#     success_url = reverse_lazy('converter:show_all_docs')


# class DocItem(LoginRequiredMixin, DetailView):
#     model = Document
#     template_name = 'converter/docs/show_one_doc.html'


# class DocsList(LoginRequiredMixin, ListView):
#     model = Document
#     template_name = 'converter/docs/show_docs_oop.html'
#     context_object_name = 'docs'
#     paginate = 2

#     def get_queryset(self):
#         user = self.request.user
#         query_format = self.kwargs.get('format')
#         # breakpoint()
#         if not query_format:
#             docs = Document.objects.filter(user=user).order_by('-size')
#         else:
#             format = Formats.objects.filter(formatname=query_format)[0].id 
#             docs = Document.objects.filter(user=user, doc_format=format).order_by('-size')
#         return docs

#     def get_context_data(self, **kwargs):
#         query_format = self.kwargs.get('format')

#         if not query_format:
#             query_format = 'Формат'
        
#         context = super().get_context_data(**kwargs)
#         context.update({
#             'formats_list':Formats.objects.all(),
#             'chosen_format':query_format
#         })
#         return context
    
#     def get(self, *args, **kwargs):
#         query_format = kwargs.get('format')

#         from django.http import Http404
#         if query_format == 'txt':
#             raise Http404('очко')
#         # переадресация с аргументом
#         # if query_format == 'txt':
#         #     return redirect('converter:show_all_docs', 'pdf')
        
#         return super(DocsList, self).get(*args, **kwargs)


#     # можно еще так фильтровать
#     # def get_context_data(self, **kwargs):
#     #     context = super().get_context_data(**kwargs)
#     #     docs = context['docs'].filter(user=self.request.user)
#     #     return docs

# class MyRegisterForm(FormView):
#     template_name = 'converter/register-form.html' 
#     form_class = CustomUserCreationForm
#     success_url = reverse_lazy('converter:show_all_docs')
#     redirect_authenticated_user = True

#     def form_valid(self, form):
#         """If the form is valid, redirect to the supplied URL."""
#         user = form.save()
#         if user is not None:
#             login(self.request, user)
#         return super(MyRegisterForm, self).form_valid(form)

#     def get(self, *args, **kwargs):
#         if self.request.user.is_authenticated:
#             print('перенаправили зареганого юзера')
#             return redirect('converter:show_all_docs')
#         return super(MyRegisterForm, self).get(*args, **kwargs)


# class TestForm(FormView):
#     template_name = 'converter/test_form.html'
#     form_class = TestUserForm
#     success_url = reverse_lazy('converter:show_all_docs')
#     redirect_authenticated_user = True


# """функциональный подход"""

# def error_404(request, exception):
#     return render(request,'converter/404.html', exception)


# def upload_form(r):
#     if r.method ==  'POST':
#         return HttpResponse('отправили файлы))')
#     formats = {"formats": Formats.objects.all()}
#     return render(r, 'converter/show_upload_form.html', formats)


# def test_upload_form(request):
#     print(request)
#     print(request.POST)
#     formats = Formats.objects.all()
#     data = {"formats": formats}
#     # print('data--', data['formats'])

#     # data = {"formats": [{"formatname": e} for e in ['zip', 'rogue']]}

#     return render(request, 'converter/upload_form.html', data)


# def test_redirect(r, format):
#     return HttpResponse(format)
#     # return render(r, 'converter/show_choosen_format.html', data)


# def choose_format(r, choosen_format):
#     all_formats = Formats.objects.all()
#     if not choosen_format:
#         formats_objects = Formats.objects.all()

#     else:
#         formats_objects = Formats.objects.filter(formatname=choosen_format)

#     documents = [e.document_set.all() for e in formats_objects]

#     data = {"formats": formats_objects, 'documents': documents,
#             'choosen_format': choosen_format, 'all_formats': all_formats}

#     return render(r, 'converter/show_docs.html', data)


# def show_choosen_format(r, format):
#     print('show_choosen_format r ::::', r)
#     print('show_choosen_format format ::::', format)

#     # тут чет нет choice в посте

#     choosen_format = r.POST['choice']
#     format = Formats.objects.filter(formatname=choosen_format)
#     # format = get_object_or_404(Formats, formatname=choosen_format)

#     if format:
#         print('format---', format[0])
#         format_docs = format[0].document_set.all()
#         data = {"format": choosen_format, "docs": [
#             e.doc_name for e in format_docs]}

#         # TODO: в html можно обращаться к объектам из БД {{ format.docs_set.all() }}
#         print('data---', data)

#         return render(r, 'converter/show_choosen_format.html', data)
#         # return HttpResponseRedirect(reverse('converter:test_redirect',
#         #                                     kwargs={'format': 'val'}))

#     else:
#         formats = Formats.objects.all()
#         my_error = 'выбран rogue format!'
#         data = {"formats": formats, 'errors': my_error}
#         return render(r, 'converter/upload_form.html', data)


# def test_base(r):
#     return render(r, 'converter/base.html')
