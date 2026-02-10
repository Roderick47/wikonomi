from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import BugReportForm

def report_bug(request):
    """View to handle bug report submission"""
    if request.method == 'POST':
        form = BugReportForm(request.POST, request.FILES)
        if form.is_valid():
            report = form.save(commit=False)
            if request.user.is_authenticated:
                report.user = request.user
            report.save()
            
            messages.success(request, 'Thank you for your report! We will investigate the issue.')
            return redirect('Report:success')
    else:
        # Pre-fill URL if available in referrer
        initial_data = {}
        referrer = request.META.get('HTTP_REFERER')
        if referrer and 'report' not in referrer:
            initial_data['url_route'] = referrer
            
        form = BugReportForm(initial=initial_data)
    
    return render(request, 'Report/report_bug.html', {'form': form})

def report_success(request):
    """Simple success page after reporting"""
    return render(request, 'Report/report_success.html')
