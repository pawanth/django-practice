
# Class based views are more pawerful

[Refer to django docs](https://docs.djangoproject.com/en/3.2/ref/class-based-views/)

## code to handle HTTP GET in a view function 
```python
from django.http import HttpResponse
from django.views import View

class MyView(View):
    greeting = "Good Day"
    def get(self, request):
        # <view logic>
        return HttpResponse('result')
```

Because Django’s URL resolver expects to send the request and associated arguments to a callable function, not a class, class-based views have an as_view() class method which returns a function that can be called when a request arrives for a URL matching the associated pattern. The function creates an instance of the class, calls setup() to initialize its attributes, and then calls its dispatch() method. dispatch looks at the request to determine whether it is a GET, POST, etc, and relays the request to a matching method if one is defined, or raises HttpResponseNotAllowed if not:

class attributes are useful in many class-based designs, and there are two ways to configure or set class attributes.
1. ```python
    class MorningGreetingView(GreetingView):
        greeting = "Morning to ya"
    ```
2. ```python
    urlpatterns = [
        path('about/', GreetingView.as_view(greeting="G'day")),
    ]
    ```

Handle form
```python
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views import View

from .forms import MyForm

class MyFormView(View):
    form_class = MyForm
    initial = {'key': 'value'}
    template_name = 'form_template.html'

    def get(self, request, *args, **kwargs):
        form = self.form_class(initial=self.initial)
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            # <process form cleaned data>
            return HttpResponseRedirect('/success/')

        return render(request, self.template_name, {'form': form})
```
ListView generic
```python
# views.py
from django.views.generic import ListView
from books.models import Publisher

class PublisherListView(ListView):
    model = Publisher
    queryset = Book.objects.order_by('-publication_date')
    context_object_name = 'book_list'  # default object_list
    template_name = 'books/acme_list.html'
```
We could explicitly tell the view which template to use by adding a template_name attribute to the view, but in the absence of an explicit template Django will infer one from the object’s name. In this case, the inferred template will be "books/publisher_list.html" – the “books” part comes from the name of the app that defines the model, while the “publisher” bit is the lowercased version of the model’s name

# DetailView
```python
from django.views.generic import DetailView
from books.models import Book, Publisher

class PublisherDetailView(DetailView):

    model = Publisher

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        # Add in a QuerySet of all the books
        context['book_list'] = Book.objects.all()
        return context

    def get_object(self):
        obj = super().get_object()
        # Record the last accessed date
        obj.last_accessed = timezone.now()
        obj.save()
        return obj
```

# Generic Form View
```python
from django.views.generic.edit import FormView
class ContactFormView(FormView):
    template_name = 'contact.html'
    form_class = ContactForm
    success_url = '/thanks/'

    def form_valid(self, form):
        # This method is called when valid form data has been POSTed.
        # It should return an HttpResponse.
        form.send_email()
        return super().form_valid(form)
```

# Other views
```python
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from myapp.models import Author

class AuthorCreateView(CreateView):
    model = Author
    fields = ['name']

class AuthorUpdateView(UpdateView):
    model = Author
    fields = ['name']

class AuthorDeleteView(DeleteView):
    model = Author
    success_url = reverse_lazy('author-list')
```