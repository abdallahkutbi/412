from django.shortcuts import render, redirect
from django.http import HttpResponse,HttpRequest
import random
import datetime as dt

# Global variables
daily_specials = [
    ("Special Chicken Burger", 29.99),
    ("Family Meal Deal", 29.99),
    ("Chicken Combo", 15.99),
    ("Spicy Chicken Sandwich", 11.99)
]

MENU = [
    ("Chicken Burger", 14.99),
    ("Chicken Nuggets", 9.99),
    ("Chicken Wings", 9.99),
    ("Chicken Tenders", 12.99)
]

TOPPING_PRICE = 1.00

def main(request):
    template_name = 'restaurant/main.html'
    context = {
        'restaurant_name': 'Al-Baik',
        'location': '123 Main Street, Boston, MA 02215',
        'hours': [
            'Monday - Friday: 10:00 AM - 10:00 PM',
            'Saturday - Sunday: 10:00 AM - 10:00 PM'
        ]
    }
    return render(request, template_name, context)



def order(request):
    special = random.choice(daily_specials)
    context = {
        "menu": MENU,
        "special": special
    }   
    
    return render(request, "restaurant/order.html", context)

def confirmation(request):
    if request.method == "POST":
        items = request.POST.getlist('items')
        toppings = request.POST.getlist('burger_toppings')
        instructions = request.POST.get('instructions', '')
        name = request.POST.get('name', '')
        phone = request.POST.get('phone', '')
        email = request.POST.get('email', '')

        total = 0
        order_items = []
        
        special_name = request.POST.get('special_name')
        special_price = float(request.POST.get('special_price', 0))
        if special_name and special_name.lower() in [item.lower() for item in items]:
            total += special_price
            order_items.append((special_name, special_price))

        for item in items:
            if special_name and item.lower() == special_name.lower():
                continue
            for menu_item, price in MENU:
                if menu_item.lower() == item:
                    total += price
                    order_items.append((menu_item, price))
                    break

        total += len(toppings) * TOPPING_PRICE
        random_minutes = random.randint(30, 60)
        ready_time = dt.datetime.now() + dt.timedelta(minutes=random_minutes)
        
        context = {
            'order_items': order_items,
            'toppings': toppings,
            'instructions': instructions,
            'customer_name': name,
            'customer_phone': phone,
            'customer_email': email,
            'total': total,
            'ready_time': ready_time
        }
        return render(request, "restaurant/confirmation.html", context)
    return redirect("order")

