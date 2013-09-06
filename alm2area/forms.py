from django import forms
from alm2area.models import Alm, Mask
from django.forms.util import ErrorList


class AlmForm(forms.ModelForm):
    label = 'Map Parameters'
    class Meta:
        model = Alm
        fields = ('alm_form_names', 'alm_lmax', 'alm_lmin')

    alm_form_names = forms.ModelChoiceField(
        label='Alm file',
        queryset=Alm.objects.all(),
    )
    alm_nx = forms.IntegerField(label='nx', initial=101)
    alm_np = forms.IntegerField(label='np', initial=202)


class MaskForm(forms.ModelForm):
    label = 'Mask File'
    class Meta:
        model = Mask
        fields = ('mask_names',)

    mask_names = forms.ModelChoiceField(
        label='Mask name',
        queryset=Mask.objects.all(),
        )


class MapImageForm(forms.Form):
    label = 'Map View Values Limits'
    map_image_maxv = forms.FloatField(label='Max value')
    map_image_minv = forms.FloatField(label='Min value')


class PointSourceForm(forms.Form):
    label = 'Point Source Data'
    point_source_file = forms.FileField(label='Point source file')
    ps_mult = forms.FloatField(
        initial=1.0,
        label='Point sources multiplier',
    )


class MapZoneCutFrom(forms.Form):
    label = 'Zone Cut Parameters'
    map_zone_cut_lat1 = forms.FloatField(label='Min lat')
    map_zone_cut_lon1 = forms.FloatField(label='Min lon')
    map_zone_cut_lat2 = forms.FloatField(label='Max lat')
    map_zone_cut_lon2 = forms.FloatField(label='Max lon')


class HiddenErrorList(ErrorList):
    def __unicode__(self):
        return u''
    def as_text(self):
        return u''
    def as_ul(self):
        return u''

class SmoothForm(forms.Form):
    label = 'Smoothing Parameters'
    smooth_value = forms.FloatField(label='Smooth window', min_value=0.0)
