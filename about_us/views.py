
from django.shortcuts import render
from .forms import ContactForm
from django.shortcuts import render, get_object_or_404
from .models import Article

def contact_form_view(request):
    # Handle POST method (Form Submission)
    if request.method == 'POST':
        form = ContactForm(request.POST) # Bind the form with POST data
        if form.is_valid():
            # Extract the safely cleaned data
            name = form.cleaned_data.get('name')
            email = form.cleaned_data.get('email')
            message = form.cleaned_data.get('message')
            
            # This is where you would normally save to a database or send an email
            print(f"New submission from {name} - {email}")
            
            # Render a success page, passing the user's name to the template
            return render(request, 'success_form.html', {'name': name})
            
    # Handle GET method (Initial Page Load)
    else:
        form = ContactForm() # Create an empty, unbound form

    # Render the form page, passing the form context
    return render(request, 'form.html', {'form': form})


# 1. View to list all published articles
def article_list(request):
    # Fetch only published articles, ordered by newest first
    articles = Article.objects.filter(is_published=True).order_by('-created_at')
    return render(request, 'article_list.html', {'articles': articles})

# 2. View to display a single article based on its slug
def article_detail(request, slug):
    article = get_object_or_404(Article, slug=slug, is_published=True)
    return render(request, 'article_detail.html', {'article': article})