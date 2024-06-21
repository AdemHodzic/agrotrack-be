from django.contrib import admin
from .models import Plot
import uuid

class PlotAdmin(admin.ModelAdmin):
    list_display = ('plot_name', 'plot_heatmap_url')
    filter_horizontal = ('users',)

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        form.base_fields['plot_center_coordinates'].widget.attrs.update({'placeholder': 'Format: [lat, lng]'})
        return form

    def save_model(self, request, obj, form, change):
        if not change:
            obj.plot_id = uuid.uuid4()
        super().save_model(request, obj, form, change)

admin.site.register(Plot, PlotAdmin)