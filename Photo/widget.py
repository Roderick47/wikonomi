from django.forms import ClearableFileInput
from django.template.loader import render_to_string
from django.utils.safestring import mark_safe

class ImagePreviewWidget(ClearableFileInput):
    class Media:
        js = ('js/image_preview.js')

    def __init__(self, *args,**kwargs):
        super(ImagePreviewWidget,self).__init__(*args,**kwargs)

    def render(self,name,value,attrs=None):
        attrs.update({
            'multiple':False,
            'accept':u'image/jpg, image/jpeg, image/png' # For the browser upload dialogue to only show these files.
        })
        return mark_safe(render_to_string('image_upload.html',{
            'input':mark_safe(super(ImagePreviewWidget,self).render(name,value,attrs).replace(u'{t}:'.format(t=self.initial_text),u'').replace(u'{t}'.format(t=self.input_text),u'')),
            'value':value,
        }))