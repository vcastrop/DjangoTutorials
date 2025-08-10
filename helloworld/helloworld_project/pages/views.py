from django.http import HttpResponseRedirect
from django.urls import reverse
from django.shortcuts import render
from django.views.generic import TemplateView
from django.views import View
from django import forms
from django.shortcuts import render, redirect

class HomePageView(TemplateView):
    template_name = 'pages/home.html'

class AboutPageView(TemplateView):
    # This defines a Django class-based view (CBV) that inherits from TemplateView.
    # TemplateView is used to render a template without needing a form or model.

    template_name = 'pages/about.html'
    # Specifies the path to the template file that should be rendered
    # when this view is requested.

    def get_context_data(self, **kwargs):
        # This method is used to pass extra context (variables) to the template.
        # **kwargs allows for any extra keyword arguments to be included.

        context = super().get_context_data(**kwargs)
        # Calls the parent class's get_context_data method to get the default context.

        context.update({
            # Adds or updates the context dictionary with our custom variables.
            "title": "About us - Online Store",  # Page title variable for the <title> block.
            "subtitle": "About us",              # Subtitle for the header block.
            "description": "This is an about page ...",  # Text shown in the page content.
            "author": "Developed by: Your Name", # Author info to display.
        })

        return context
        # Returns the updated context dictionary to be used by the template.

class ContactPageView(TemplateView):
    # CBV for Contact Us page
    template_name = 'pages/contact.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context.update({
            "title": "Contact - Online Store",
            "subtitle": "Contact Us",
            "email": "site@gmail.com",
            "address": "Street 1,2,3 New York City",
            "phone": "+1 234 567 890",
        })
        return context
class Product:
    # This class holds a static list of products.
    # fake "database" for demonstration purposes.
    products = [
        {"id": "1", "name": "TV", "description": "Best TV", "price": 50},
        {"id": "2", "name": "iPhone", "description": "Best iPhone", "price": 100},
        {"id": "3", "name": "Chromecast", "description": "Best Chromecast", "price": 150},
        {"id": "4", "name": "Glasses", "description": "Best Glasses", "price": 500},
    ]
class ProductIndexView(View):
    # This is a Django class-based view (CBV) for listing all products.
    # It inherits from the generic View class.

    template_name = 'products/index.html'
    # Specifies the HTML template that should be used to render the product list.

    def get(self, request):
        # Handles GET requests for the product list page.

        viewData = {}
        # Creates an empty dictionary to hold variables that will be passed to the template.

        viewData["title"] = "Products - Online Store"
        # Title of the page (used in <title> tag or header in the template).

        viewData["subtitle"] = "List of products"
        # Subtitle for the page.

        viewData["products"] = Product.products
        # Adds the list of products from the Product class to the template context.

        return render(request, self.template_name, viewData)
        # Renders the 'products/index.html' template with the provided viewData dictionary.
class ProductShowView(View):
    # This is a Django class-based view for showing details of a single product.
    # It also inherits from the generic View class.

    template_name = 'products/show.html'
    # Specifies the HTML template that should be used to render the product detail page.

    def get(self, request, id):
        # Handles GET requests for a single product detail page.
        # The 'id' parameter comes from the URL.

        viewData = {}
        # Creates a dictionary to hold variables for the template.

        # Validates that the id is in the numbers range
        try:
            id_int = int(id)  # tries to convert id to int
        except ValueError:
            return HttpResponseRedirect(reverse('home'))  # if it is not a number redirects

        if id_int < 1 or id_int > len(Product.products):
            return HttpResponseRedirect(reverse('home'))  # Si it is out of range redirects
        product = Product.products[int(id) - 1]
        # Retrieves the product from the Product list using its ID (converted to integer).
        # Subtracts 1 because Python lists are zero-indexed.

        viewData["title"] = product["name"] + " - Online Store"
        # Sets the page title to the product name plus " - Online Store".

        viewData["subtitle"] = product["name"] + " - Product information"
        # Sets the subtitle to indicate product information.

        viewData["product"] = product
        # Passes the selected product's data to the template.

        return render(request, self.template_name, viewData)
        # Renders the 'products/show.html' template with the product's data.

# Formulario para crear un producto
class ProductForm(forms.Form):
    # Campo de texto para el nombre del producto (obligatorio)
    name = forms.CharField(required=True)
    # Campo numérico (decimal) para el precio del producto (obligatorio)
    price = forms.FloatField(required=True)

# Vista para crear un producto
class ProductCreateView(View):
    # Nombre del template que renderizará la vista
    template_name = 'products/create.html'

    # Método GET: se ejecuta cuando se accede a la página por primera vez
    def get(self, request):
        form = ProductForm()  # Crea una instancia vacía del formulario
        viewData = {}
        viewData["title"] = "Create product"  # Título de la página
        viewData["form"] = form  # Pasa el formulario al contexto
        return render(request, self.template_name, viewData)  # Renderiza el template con los datos

    # Método POST: se ejecuta cuando se envía el formulario
    def post(self, request):
        form = ProductForm(request.POST)  # Crea una instancia del formulario con los datos enviados
        if form.is_valid():  # Valida que el formulario cumpla las reglas definidas
            return redirect(form)  # Si es válido, redirige (aquí deberías poner una URL o nombre de ruta)
        else:
            # Si el formulario no es válido, se vuelve a mostrar con los errores
            viewData = {}
            viewData["title"] = "Create product"
            viewData["form"] = form
            return render(request, self.template_name, viewData)