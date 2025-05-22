from django.shortcuts import render
from django.http import HttpResponse,HttpRequest
import random

all_quotes = [
    "Fear is the path to the dark side. Fear leads to anger. Anger leads to hate. Hate leads to suffering.",
    "Always pass on what you have learned.",
    "Once you start down the dark path, forever will it dominate your destiny. Consume you, it will.",
    "In the end, cowards are those who follow the dark side.",
    "Many of the truths that we cling to depend on our point of view.",
]

all_images = [
    "images/th-3651807705.jpg",
    "images/th-3383381882.jpg",
    "images/th-3190052294.jpg",
]

def home(request):
    '''This is the home page of the Quote App.'''
    template_name = 'quotes/quote.html'
    random_quote = random.choice(all_quotes)
    random_image = random.choice(all_images)
    context = {
        'random_quote': random_quote,
        'random_image': random_image,
    }
    return render(request, template_name, context)


def show_all(request):
    '''This is the show all page of the Quote App.'''
    context = {
        'all_quotes': all_quotes,
        'all_images': all_images,
    }
    return render(request, 'quotes/show_all.html', context)



def about(request):
    '''This is the about page of the Quote App.'''
    template_name = 'quotes/about.html'
    return render(request, template_name)

