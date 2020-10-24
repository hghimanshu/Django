from django.urls import path, re_path
from .views import (ProductListView, 
                    # ProductDetailView, 
                    # ProductFeaturedDetailView, 
                    # ProductFeaturedListView, 
                    ProductDetailSlugView)

urlpatterns = [
    path('', ProductListView.as_view()),
    re_path(r'^(?P<slug>[\w-]+)/$', ProductDetailSlugView.as_view()),  ## path is depreceated for regular expressions

]