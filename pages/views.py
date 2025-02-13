from django.shortcuts import render, redirect
from django.views.generic import TemplateView
from django.views import View 
from django.http import HttpResponseRedirect
from django.urls import reverse
from django import forms
from django.core.exceptions import ValidationError
import re


# Create your views here.

class HomePageView(TemplateView):
    template_name = 'pages/home.html' 

class AboutPageView(TemplateView):
    template_name = 'pages/about.html' 
 
     
    def get_context_data(self, **kwargs): 
        context = super().get_context_data(**kwargs) 
        context.update({ 
            "title": "About us - Online Store", 
            "subtitle": "About us", 
            "description": "This is an about page ...", 
            "author": "Developed by: Your Name", 
        }) 
 
        return context 

class ContactPageView(TemplateView):
    template_name = 'pages/contact.html'

    def get_context_data(self, **kwargs): 
        context = super().get_context_data(**kwargs) 
        context.update({ 
            "subtitle": "Contact", 
            "email": "example@email.com", 
            "adress": "Example adress", 
            "phone_number": "123456789" 
        }) 
 
        return context
    
 
class Product: 
    products = [ 
        {"id":"1", "name":"TV", "description":"Best TV", "price": 600}, 
        {"id":"2", "name":"iPhone", "description":"Best iPhone", "price": 500}, 
        {"id":"3", "name":"Chromecast", "description":"Best Chromecast", "price": 50}, 
        {"id":"4", "name":"Glasses", "description":"Best Glasses", "price": 30} 
    ] 
 
class ProductIndexView(View): 
    template_name = 'products/index.html' 
 
    def get(self, request): 
        viewData = {} 
        viewData["title"] = "Products - Online Store" 
        viewData["subtitle"] =  "List of products" 
        viewData["products"] = Product.products 
 
        return render(request, self.template_name, viewData) 
 
class ProductShowView(View): 
    template_name = 'products/show.html' 
 
 
    def get(self, request, id): 
        viewData = {}
        if len(Product.products) < int(id) : 
            return HttpResponseRedirect(reverse('home'))

        product = Product.products[int(id)-1]
        viewData["title"] = product["name"] + " - Online Store" 
        viewData["subtitle"] =  product["name"] + " - Product information" 
        viewData["product"] = product 
 
        return render(request, self.template_name, viewData)
 
class ProductForm(forms.Form): 
    name = forms.CharField(required=True) 
    price = forms.FloatField(required=True) 

    def clean_price(self):  # Django ejecuta este método automáticamente
        price = self.cleaned_data.get("price")  # ✅ Obtener "price" correctamente

        if price < 0:  # ✅ Verificar si el precio es negativo
            raise ValidationError("El precio no debe ser negativo.")

        return price
 
 
class ProductCreateView(View): 
    template_name = 'products/create.html' 
 
    def get(self, request): 
        form = ProductForm() 
        viewData = {} 
        viewData["title"] = "Create product" 
        viewData["form"] = form 
        return render(request, self.template_name, viewData) 
 
    def post(self, request): 
        form = ProductForm(request.POST) 
        if form.is_valid():
            return redirect('success')  
        else: 
            viewData = {} 
            viewData["title"] = "Create product" 
            viewData["form"] = form 
            return render(request, self.template_name, viewData)
        
class SuccessView(View):
    template_name = 'pages/success.html'
    
    def get(self, request):
        return render(request, self.template_name)
        
        