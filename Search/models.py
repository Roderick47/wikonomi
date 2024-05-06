from django.db import models
from django.core.paginator import Paginator,EmptyPage,PageNotAnInteger
# Create your models here.


# for use in paginating querysets.DRY.
def pager(request,qlist,number):
    page = request.GET.get('page')
    paginator = Paginator(qlist,number)
    try:
        qname = paginator.page(page)
    except PageNotAnInteger:
        qname = paginator.page(1)
    except EmptyPage:
        qname = paginator.page(paginator.num_pages)    
    return qname

def combine_query_sets(qs,combined_qs):
    for i in qs:
        if combined_qs:
            if i in combined_qs:
                pass
            else:
                combined_qs.append(i) 
        else: pass
    return combined_qs
