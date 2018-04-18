from django.shortcuts import render


# Create your views here.
def query_builder(request):
    return render(request,
                  'data_wrapper/query_builder.html'
                  )
