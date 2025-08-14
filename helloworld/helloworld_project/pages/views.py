from django.http import HttpResponseRedirect
from django.urls import reverse
from django.shortcuts import render
from django.views.generic import TemplateView, ListView
from django.views import View
from django import forms
from django.shortcuts import render, redirect, get_object_or_404
from django.core.exceptions import ValidationError
from .models import Product

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

        viewData["products"] = Product.objects.all()
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
            product_id = int(id)
            if product_id < 1:
                raise ValueError("Product ID must be 1 or greater.")
            product = get_object_or_404(Product, pk=product_id)
        except (ValueError, IndexError):
            return HttpResponseRedirect(reverse('home'))

        product = get_object_or_404(Product, pk=product_id)

        viewData["title"] = product.name + " - Online Store"
        # Sets the page title to the product name plus " - Online Store".

        viewData["subtitle"] = product.name + " - Product information"
        # Sets the subtitle to indicate product information.

        viewData["product"] = product
        # Passes the selected product's data to the template.

        return render(request, self.template_name, viewData)
        # Renders the 'products/show.html' template with the product's data.

# Form to create a new product
class ProductForm(forms.Form):
    class Meta:
        model = Product
        fields = ['name', 'price']

    def clean_price(self):
        price = self.cleaned_data.get['price']
        if price is None or price <= 0:
            raise ValidationError("Price must be greater than zero.")
        return price

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
        form = ProductForm(request.POST)
        if form.is_valid():
            form.save()
            return render(request, self.template_success, {
                "title": "Product created",
                "message": "Product created", })

        else:
            viewData = {}
            viewData["title"] = "Create product"
            viewData["form"] = form
            return render(request, self.template_name, viewData)

class ProductListView(ListView):
    # This is a Django class-based view for listing products.
    model = Product  # Specifies the model to use for this view.
    template_name = 'product_list.html'  # The template to render the product list.
    context_object_name = 'products'  # to loop through products in the template.

    def get_context_data(self, **kwargs):
        # This method allows us to add extra context variables to the template.
        context = super().get_context_data(**kwargs)
        context['title'] = 'Products - Online Store'
        context['subtitle'] = 'List of products'
        return context

class CartView(View):
    template_name = 'cart/index.html'

    def get(self, request):
        # Simulated database for products
        products = {}
        products[121] = {'name': 'Tv samsung', 'price': '1000'}
        products[11] = {'name': 'Iphone', 'price': '2000'}

        # Get cart products from session
        cart_products = {}
        cart_product_data = request.session.get('cart_product_data', {})

        for key, product in products.items():
            if str(key) in cart_product_data.keys():
                cart_products[key] = product

        # Prepare data for the view
        view_data = {
            'title': 'Cart - Online Store',
            'subtitle': 'Shopping Cart',
            'products': products,
            'cart_products': cart_products
        }

        return render(request, self.template_name, view_data)

    def post(self, request, product_id):
        # Get cart products from session and add the new product
        cart_product_data = request.session.get('cart_product_data', {})
        cart_product_data[product_id] = product_id
        request.session['cart_product_data'] = cart_product_data
        return redirect('cart_index')


class CartRemoveAllView(View):
    def post(self, request):
        # Remove all products from cart in session
        if 'cart_product_data' in request.session:
            del request.session['cart_product_data']
        return redirect('cart_index')


def ImageViewFactory(image_storage):
    class ImageView(View):
        template_name = 'image/index.html'

        def get(self, request):
            image_url = request.session.get('image_url', '')
            return render(request, self.template_name, {'image_url': image_url})

        def post(self, request):
            image_url = image_storage.store(request)
            request.session['image_url'] = image_url
            return redirect('image_index')

    return ImageView

class ImageViewNoDI(View):
    template_name = 'imagenotdi/index.html'

    def get(self, request):
        image_url = request.session.get('image_url', '')
        return render(request, self.template_name, {'image_url': image_url})

    def post(self, request):
        image_storage = ImageLocalStorage()
        image_url = image_storage.store(request)
        request.session['image_url'] = image_url
        return redirect('image_index')
