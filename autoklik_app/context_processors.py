from .forms import ReviewForm

def review_form_manager(request):
    return {
        'global_review_form': ReviewForm()
    }
