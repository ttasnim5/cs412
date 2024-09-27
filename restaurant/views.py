import random
from django.shortcuts import render, redirect
from decimal import Decimal
from datetime import datetime, timedelta

daily_specials = [
    "Chocolate Fudge",
    "Cookie Butter",
    "Oreo",
    "Cotton Candy",
    "Red Velvet",
    "Cheesecake",
    "Strawberry",
    "Blueberry",
]

sauces = [
    "Chocolate Syrup",
    "Vanilla Syrup",
    "Caramel Syrup",
    "Cookie Butter",
    "Pistachio Butter",
    "Strawberry Jam",
    "Blueberry Jam",
]

toppings = [
    "Chocolate Chunks",
    "Diced Strawberries",
    "Blueberries",
    "Sliced Banana",
    "Crushed Biscoff",
    "Crushed Pistachios",
    "Mini Mochis",
]

base_prices = {
    "waffle": Decimal("4.00"),
    "crepe": Decimal("4.00"),
    "pancake": Decimal("4.00"),
    "croissant": Decimal("3.00"),
    "biscuit": Decimal("3.00"),
}

def main(request):
    '''Show the main page of the restaurant.'''
    template_name = "restaurant/main.html"
    context = {
        'image': "/static/restaurant.jpg",
        'blurb': '''Welcome to Sweets Galore, where we believe every bite should be a little moment of 
        joy! Specializing in freshly made waffles, pancakes, crepes, biscuits, and croissants, we offer 
        an irresistible assortment of treats topped with an array of sauces and delightful toppings. Whether 
        you're craving something classic or feeling adventurous, we've got the perfect mix to sweeten your day. 
        Come in for a warm, delicious experience that’s sure to satisfy your sweet tooth!'''
    }
    return render(request, template_name, context)

def order(request):
    '''Show the order page of the restaurant.'''
    template_name = "restaurant/order.html"
    context = {
        'daily_special': random.choice(daily_specials),
        'sauces': sauces,
        'toppings': toppings,
    }
    return render(request, template_name, context)

def calculate_total(base, daily_special, sauces, toppings):
    total = base_prices[base]
    
    if daily_special:
        total += Decimal("1.00")

    total += len(sauces) * Decimal("0.30")
    total += len(toppings) * Decimal("0.30")
    
    return total

def confirmation(request):
    '''Handle form submission, read out data, generate response.'''
    template_name = "restaurant/confirmation.html"

    if request.method == 'POST':
        name = request.POST['name']
        phone = request.POST['phone']
        email = request.POST['email']
        base = request.POST['base']
        daily_special = request.POST.get('daily_special', '')
        sauces = request.POST.getlist('sauces')
        toppings = request.POST.getlist('toppings')
        total_price = calculate_total(base, daily_special, sauces, toppings)
        time = datetime.now() + timedelta(minutes=10)

        sauces_str = ", ".join(sauces) if sauces else "No sauces"
        toppings_str = ", ".join(toppings) if toppings else "No toppings"
        daily_special_str = daily_special if daily_special else "No daily special"

        total_price = calculate_total(base, daily_special, sauces, toppings)

        context = {
            'name': name,
            'phone': phone,
            'email': email,
            'base': base,
            'daily_special': daily_special_str,
            'sauces': sauces_str,
            'toppings': toppings_str,
            'total_price': total_price,
            'time': time,
        }
        return render(request, template_name, context)
    
    return redirect("main")