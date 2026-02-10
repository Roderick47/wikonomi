from .models import HowToHistory

def create_howto_snapshot(howto, user, summary=""):
    """
    Creates a snapshot of the current state of a HowTo and its steps.
    """
    steps = howto.steps.all().order_by('order')
    steps_data = []
    
    for step in steps:
        steps_data.append({
            'title': step.title,
            'content': step.content,
            'image_url': step.image.url if step.image else None,
            'order': step.order
        })
    
    snapshot = HowToHistory.objects.create(
        how_to=howto,
        version=howto.version,
        editor=user,
        title=howto.title,
        description=howto.description,
        change_summary=summary,
        steps_snapshot=steps_data
    )
    return snapshot
