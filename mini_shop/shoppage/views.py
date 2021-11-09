from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from loginpage.views import login_required

# Create your views here.
@login_required
def pricing(request):
    return render(request, 'shoppage/pricing.html')
