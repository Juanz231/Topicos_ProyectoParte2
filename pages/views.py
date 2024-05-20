#programado por: Juan Pavas, Andres Rua, Jose Valencia
from django.contrib.auth.models import User
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import TemplateView, ListView
from django.views import View
from django.http import HttpResponseRedirect, HttpResponseNotFound
from django.urls import reverse
from django import forms
from django.core.exceptions import ValidationError, ObjectDoesNotExist
from .models import Ropa, Regalo, Review, CustomUser
from django .contrib import messages
from django.http import JsonResponse
from django.urls import reverse_lazy
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader
from django.conf import settings
from abc import ABC, abstractmethod
import requests
from random import choice
from django.urls import reverse
from django.contrib.auth import authenticate, login

#verificación de admin
from django.contrib.auth.decorators import user_passes_test
from django.http import HttpResponse
from django.contrib.auth.views import LogoutView
#signup
from django.contrib.auth import authenticate, login
from .forms import CustomUserCreationForm, LoginForm, RopaForm, RegaloForm
from django.contrib.auth.forms import AuthenticationForm

#translation
from django.conf import settings
from django.utils.translation import gettext_lazy as _

from django.http import FileResponse
from django.conf import settings
import os
from django.template.loader import get_template


class HomePageView(TemplateView):
    template_name = 'home.html'




class AboutPageView(TemplateView):
    template_name = 'about.html'

    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({    
            "title": _("En TechnoStyleFashion nos preocupamos por no solo se ve la gente, sino también por cómo se sienten."),
            "subtitle": _("¿Quienes están detras de todo esto?"),
            "description": _("Somos un grupo de estudiantes de la Universidad EAFIT que se preocupan por la moda y la tecnología. Nos esforzamos por ofrecer productos de alta calidad a precios asequibles. ¡Gracias por visitar nuestra tienda en línea!"),
        })

        return context

class LogOutView(LogoutView):
    next_page = reverse_lazy('home')
    
    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)
    
class RopaShowView(View):
    template_name = 'ropa/show.html'
    
    def get(self, request, id):
        try:
            ropa_id = int(id)
            if ropa_id < 1:
                raise ValueError(_("El id de la prenda debe ser mayor a 1"))
            ropa = get_object_or_404(Ropa, pk=ropa_id)
        except (ValueError, IndexError):
            return HttpResponseRedirect(reverse('home'))

        viewData = {
            "title": _("Tienda de Prendas - {}").format(ropa.Titulo),
            "subtitle": _("Informacion de la prenda - {}").format(ropa.Titulo),
            "ropa": ropa,
        }

        return render(request, self.template_name, viewData)
    

class RopaCreateView(View):
    template_name = 'ropa/create.html'

    def get(self, request):
        form = RopaForm()
        viewData = {}
        viewData["title"] = _("Crear Ropa")
        viewData["form"] = form
        return render(request, self.template_name, viewData)
    
    def post(self, request):
        form = RopaForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('ropa_index')
        else:
            viewData = {}
            viewData["title"] = _("Crear Ropa")
            print(form.errors)
            viewData["form"] = form
        return render(request, self.template_name, viewData)
            

class RopaListView(ListView):
    model = Ropa
    template_name = 'ropa/index.html'
    context_object_name = 'ropas'  # This will allow you to loop through 'products' in your template

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = _('Ropa - Tienda en línea')
        context['subtitle'] = _('Lista de prendas')
        return context   

class RopaDeleteView(View):
    def get(self, request, id):
        ropa = get_object_or_404(Ropa, pk=id)
        ropa.delete()
        return redirect('ropa_index') 
    

class RegaloIndexView(View):
    template_name = 'regalos/index.html'

    def get(self, request):
        viewData = {}
        viewData["title"] = _("Regalos")
        viewData["subtitle"] = _("Algunos Regalos")
        viewData["regalos"] = Regalo.objects.all()

        return render(request, self.template_name, viewData)

class RegaloShowView(View):
    template_name = 'regalos/show.html'

    def get(self, request, id):
        try:
            regalo_id = int(id)
            if regalo_id < 1:
                raise ValueError(_("El id del regalo debe ser mayor a 1"))
            regalo = get_object_or_404(Regalo, pk=regalo_id)
        except (ValueError, IndexError):
            return HttpResponseRedirect(reverse('home'))
        
        viewData = {}
        regalo = get_object_or_404(Regalo, pk=regalo_id)
        viewData["title"] = _("Algunos regalos - ") + regalo.titulo_regalo
        viewData["subtitle"] = _("Regalos - ") + regalo.titulo_regalo
        viewData["regalo"] = regalo

        return render(request, self.template_name, viewData)
    
    

class RegaloCreateView(View):
    template_name = 'regalos/create.html'

    def get(self, request):
        form = RegaloForm()
        viewData = {}
        viewData["title"] = _("Subir Regalo")
        viewData["form"] = form
        return render(request, self.template_name, viewData)

    def post(self, request):
        form = RegaloForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('regalos')

        else:
            viewData = {}
            viewData["title"] = _("Subir Regalo")
            viewData["form"] = form
        return render(request, self.template_name, viewData)
"""    
class RegaloListView(ListView):
    model = Regalo
    template_name = 'regalo_list.html'
    context_object_name = 'regalos'  # This will allow you to loop through 'products' in your template

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = _('Nota - Tienda en línea')
        context['subtitle'] = _('Lista de notitas')
        # Revisar esta clase !!!
        return context
"""




class RegaloDeleteView(View):
    def get(self, request, id):
        regalo = get_object_or_404(Regalo, pk=id)
        regalo.delete()
        return redirect('regalos') 
    

class ReviewIndexView(View):
    template_name = 'reviews/index.html'

    def get(self, request):
        viewData = {}
        viewData["title"] = _("Mis Reviews")
        viewData["subtitle"] = _("Reviews")
        viewData["reviews"] = Review.objects.all()

        return render (request, self.template_name, viewData)

class ReviewShowView(View):
    template_name = 'reviews/show.html'

    def get(self, request, id):
        try:
            review_id = int(id)
            if review_id < 1:
                raise ValueError(_("El id de la review debe ser mayor a 1"))
            review = get_object_or_404(Review, pk=review_id)
        except (ValueError, IndexError):
            return HttpResponseRedirect (reverse('home'))
        
        viewData = {}
        review = get_object_or_404(Review, pk=review_id)
        viewData["title"] = _("Mis reviews - ") + review.Titulo_Review
        viewData["subtitle"] = _("Reviews - ") + review.Titulo_Review
        viewData["review"] = review

        return render (request, self.template_name, viewData)

    
class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['Titulo_Review','Contenido_Review', 'Fecha_Review']


class ReviewCreateView(View):
    template_name = 'reviews/create.html'

    def get(self, request):
        form = ReviewForm()
        viewData = {}
        viewData["title"] = _("Crear Review")
        viewData["form"] = form
        return render(request, self.template_name, viewData)

    def post(self, request):
        form = ReviewForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('misreviews')

        else:
            viewData = {}
            viewData["title"] = _("Crear Review")
            viewData["form"] = form
        return render(request, self.template_name, viewData)
    
class ReviewListView(ListView):
    model = Review
    template_name = 'review_list.html'
    context_object_name = 'reviews'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = _('Review - Tienda en línea')
        context['subtitle'] = _('Lista de Reviews')
        return context  

class ReviewDeleteView(View):
    def get(self, request, id):
        review = get_object_or_404(Review, pk=id)
        review.delete()
        return redirect('misreviews')


class CartView(View):
    template_name = 'cart/index.html'
    
    def get(self, request):
        # Obtener los libros del carrito desde la sesión
        ropa_ids = request.session.get('ropa_ids', [])
        # Obtener los libros de la base de datos basados en los IDs en el carrito
        cart_ropa = Ropa.objects.filter(id__in=ropa_ids)

        avaliable_ropa = Ropa.objects.exclude(id__in=ropa_ids)

        # Preparar los datos para la vista
        view_data = {
            'title': _('Carrito - Tienda en línea'),
            'subtitle': _('Carrito de Compras'),
            'cart_ropa': cart_ropa,
            'avaliable_ropa': avaliable_ropa,
        }
        print(view_data['avaliable_ropa'], view_data['cart_ropa'])

        return render(request, self.template_name, view_data)

    def post(self, request, ropa_id):
        # Obtener los libros del carrito desde la sesión y agregar el nuevo libro
        ropa_ids = request.session.get('ropa_ids', [])
        ropa_ids.append(ropa_id)
        request.session['ropa_ids'] = ropa_ids

        return redirect('cart_index')

class CartRemoveAllView(View):
    def post(self, request):
        # Eliminar todos los libros del carrito en la sesión
        if 'cart_libro_ids' in request.session:
            del request.session['cart_libro_ids']

        return redirect('cart_index')

class Payment(ABC):
    @abstractmethod
    def check(self, data):
        pass

class PDF (ABC):
    @abstractmethod
    def pdf (self, data):
        pass


class checkPayment(Payment):
    def check(self, data):
        Ropa_Titulo = data.get('Ropa_Titulo')
        try:
            ropa = Ropa.objects.get(Titulo=Ropa_Titulo)
            Titulo = ropa.Titulo
            Precio = ropa.precio
            check_text = f"Cheque para: {Titulo} \nPrecio + {(Precio)}"
            return check_text
        except ObjectDoesNotExist:
            return f"El libro con el título '{Ropa_Titulo}' no fue encontrado."
    
class PDFGenerator:
    def pdf(self, data):
        pdf_filename = "cart_payment.pdf"
        c = canvas.Canvas(pdf_filename, pagesize=letter)

        y_position = 750  # Bajar todo un poco
        total_precio = 0  # Para calcular el precio total
        for ropa in data['ropa']:
            Titulo = ropa.Titulo
            Precio = ropa.precio
            total_precio += Precio  # Sumar el precio al total
            imagen_url = ropa.image_url  # Asegúrate de tener una URL de imagen en tu modelo de ropa

            # Dibujar la imagen
            try:
                image = ImageReader(imagen_url)
                c.drawImage(image, 70, y_position - 40, width=50, height=50)  # Ajusta la posición y el tamaño según sea necesario
            except IOError:
                print(f"No se pudo cargar la imagen desde {imagen_url}")
            
            
            
            
                
            # Dibujar el texto
            texto1 = f"Prenda: {Titulo}"
            texto2 = f"Precio: {Precio:,}$"
            c.drawString(130, y_position, texto1)  # Mover el texto a la derecha
            y_position -= 20  # Mover hacia abajo para la siguiente línea
            c.drawString(130, y_position, texto2)  # Mover el texto a la derecha
            y_position -= 60  # Mover hacia abajo para la siguiente prenda (ajusta según el tamaño de la imagen)

            # Dibujar un rectángulo alrededor de la imagen y el texto
            c.rect(50, y_position + 20, 500, 80)  # Ajusta la posición y el tamaño según sea necesario

        import requests
        from requests.auth import HTTPBasicAuth

        url = "https://xecdapi.xe.com/v1/convert_from.json/"
        params = {
                'from': 'COP',
                'to': 'USD,EUR',
                'amount': 1,
                'decimal_places': 10,
        }   
        response = requests.get(url, auth=HTTPBasicAuth('universidadeafit264812278', 'opsa8lrhl8v73an28jg771jvop'), params=params)

        data = response.json()
        from_currency = data['from']
        to_currencies = data['to']
        USD_conversion = data['to'][1]['mid']
        EUR_conversion = data['to'][0]['mid']

        # Dibujar el precio total en la esquina inferior izquierda
        c.drawString(50, 50, f"Precio total: {total_precio:,}$")
        
        # Calcular precios en USD y EUR
        total_precio_usd = total_precio * USD_conversion
        total_precio_eur = total_precio * EUR_conversion
        print(total_precio_usd, total_precio_eur, USD_conversion, EUR_conversion)
        # Agregar líneas con los precios en USD y EUR
        c.drawString(50, 80, f"En dólares hubieras pagado: {total_precio_usd:.2f}$ USD")
        c.drawString(50, 110, f"En euros hubieras pagado: {total_precio_eur:.2f}€ EUR")

        username = choice(["Pikachu, ", "Charmander, ", "Bulbasaur, ", "Squirtle", "Jigglypuff", "Meowth", "Psyduck", "Snorlax", "Mewtwo", "Mew"])
        # Información adicional al final
        c.drawString(50, 140, f"Recibo a nombre de: {username}")
        metodo_pago = choice(["PSE", "Tarjeta de Crédito", "Tarjeta Débito", "Efecty", "PayValida"])
        c.drawString(50, 170, f"Método de pago: {metodo_pago}")
        c.drawString(50, 200, "Cuidado con la DIAN, platudo.")  # Mensaje gracioso

        c.save()
        return pdf_filename


def mostrar_cheque(request, Ropa_Titulo=None):
    check_service = checkPayment()
    pdf_service = PDFGenerator()

    ropa = ModuleNotFoundError
    try:
        ropa = Ropa.objects.get(Titulo=Ropa_Titulo)
    except Ropa.DoesNotExist:
        pass

    if ropa:

        check_text = check_service.check({
            'Ropa_Titulo': Ropa_Titulo
        })


        pdf_filename = pdf_service.pdf({
            'Titulo': ropa.Titulo,
            'precio': ropa.precio,
            'Numero_paginas': ropa.Numero_paginas
        })

        context = {
            'check_text': check_text,
            'pdf_filename': pdf_filename,
        }
    else:
        context = {
            'error': f'El libro "{Ropa_Titulo}" no fue encontrado.'
        }

    return render(request, 'check/index.html', context)

def download_pdf(request):
    pdf_filename = request.GET.get('pdf_filename', '')
    pdf_path = os.path.join(settings.MEDIA_ROOT, pdf_filename)
    if os.path.exists(pdf_path):
        with open(pdf_path, 'rb') as pdf_file:
            response = HttpResponse(pdf_file.read(), content_type='application/pdf')
            response['Content-Disposition'] = f'attachment; filename="{pdf_filename}"'
            return response
    else:
        return HttpResponseNotFound('El archivo PDF no fue encontrado.')
    
class FinalizarCompraView(View):
    def post(self, request):
        ropa_ids = request.session.get('ropa_ids', [])
        cart_ropa = Ropa.objects.filter(id__in=ropa_ids)
        payment_service = checkPayment()
        pdf_service = PDFGenerator()
        data = {
            'ropa': cart_ropa
        }

        check_text = payment_service.check(data)
        pdf_filename = pdf_service.pdf(data)
        request.session['ropa_ids'] = []



        return render(request,'check/index.html', {'pdf_filename':pdf_filename})


    

# Verificación de administrador
def admin_check(user):
    return user.tipo_usuario == 'admin'

@user_passes_test(admin_check)
def admin_only_view(request):
    return HttpResponse(_("Esta vista solo es accesible para administradores."))

# Registro de usuario

class SignupView(View):
    def get(self, request):
        form = CustomUserCreationForm()
        return render(request, 'registration/SignUp.html', {'form': form})

    def post(self, request):
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Usuario creado exitosamente. Ahora puedes iniciar sesión.")
            return redirect('login1')
        else:
            print(form.errors)  # Agregamos esta línea para imprimir los errores en la consola
            messages.error(request, "Hubo un error al crear el usuario. Por favor, revisa los campos e inténtalo nuevamente.")
        return render(request, 'registration/SignUp.html', {'form': form})


class LoginView(View):
    def get(self, request):
        form = LoginForm()
        return render(request, 'registration/login.html', {'form': form})

    def post(self, request):
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username'] 
            password = form.cleaned_data['password']
            print("Debuging: ", username, password)
            user = authenticate(request, username=username, password=password)
            print("Debuging: ", user)
            if user is not None:
                login(request, user)
                return redirect('home')  # Redirige a la página principal después del inicio de sesión exitoso
        else:
            print("Debuging: ", form.errors)# Si el inicio de sesión falla o el formulario no es válido, muestra el formulario de inicio de sesión nuevamente con un mensaje de error
        return render(request, 'registration/login.html', {'form': form, 'error': 'Nombre de usuario o contraseña incorrectos.'})

def lista_productos (request):
    productos = Ropa.objects.all()
    data = []
    for producto in productos:
        data.append({
            'titulo': producto.Titulo,
            'marca': producto.Marca,
            'fecha_publicacion': producto.Fecha_publicacion.strftime('%Y-%m-%d'),
            'precio': producto.precio,
            'link_visualizacion': request.build_absolute_uri(reverse('show', kwargs={'id': producto.id})),
            'image' : producto.image_url,
        })    
    return JsonResponse (data, safe=False)