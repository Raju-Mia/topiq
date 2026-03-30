from django.shortcuts import render


def home(request):
    """Render the homepage."""
    return render(request, "website/index.html")
