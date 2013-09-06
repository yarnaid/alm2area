import os
from django.contrib import admin
from alm2area.models import Alm, Mask, CalculatedMap


def validate_maps(model_admin, request, query_set):
    for obj in query_set:
        if not os.path.exists(obj.calculated_map_path):
            obj.calc()
validate_maps.short_description = 'Make sure, that maps exist'

class CalculatedMapInLine(admin.TabularInline):
    model = CalculatedMap


class AlmInLine(admin.TabularInline):
    model = Alm


class AlmAdmin(admin.ModelAdmin):
    model = Alm
    inlines = [
        CalculatedMapInLine,
    ]
    list_display = ('alm_name', 'alm_lmin', 'alm_lmax')
    list_filter = ['alm_lmax']
    # fieldssets = [
    #     ('ALM', {'fields': ['name_ref', 'lmax', 'lmin']})
    # ]


class MaskAdmin(admin.ModelAdmin):
    model = Mask
    list_display = ('mask_name', )


class CalculatedMapAdmin(admin.ModelAdmin):
    model = CalculatedMap

    list_display = (
        'calculated_map_name',
        'calculated_map_lmax',
        'calculated_map_lmin',
        'calculated_map_nx',
        'calculated_map_np',
        'calculated_map_alm',
    )

    list_display_links = list_display

    list_filter = [
        'calculated_map_lmax',
        'calculated_map_np',
        'calculated_map_alm__alm_name',
    ]

    readonly_fields = ['calculated_map_path']
    # exclude = ['calculated_map_path']

    actions = [validate_maps]




admin.site.register(Alm, AlmAdmin)
admin.site.register(Mask, MaskAdmin)
admin.site.register(CalculatedMap, CalculatedMapAdmin)
