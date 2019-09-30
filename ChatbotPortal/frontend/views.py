from django.shortcuts import render

# Create your views here.
def index(request):
    return render(request, 'webpack/index.html')

def resources(request):
    # TODO: Implement static resource fetching here, or elsewhere
    return render(request, 'webpack/index.html')