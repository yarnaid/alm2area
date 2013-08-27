# Create your views here.
import os

import time
from django.core.files.temp import NamedTemporaryFile
from django.shortcuts import render_to_response
from django.template import RequestContext
from glespy.alm import Alm as galm
from glespy.tools import convertion as conv
from glespy.pointsource import PointSource

from django.contrib.sessions.models import Session
from django.dispatch import receiver
from django.db.models.signals import pre_delete, pre_save

from cmb import settings

from alm2map.forms import AlmForm, MaskForm, MapImageForm, PointSourceForm, MapZoneCutFrom, HiddenErrorList, SmoothForm


def get_alm_form_data(alm_form):
    lmin = max(alm_form.cleaned_data['alm_lmin'], 0)
    lmax = max(alm_form.cleaned_data['alm_lmax'], lmin)
    nx = max(alm_form.cleaned_data['alm_nx'], lmax * 2 + 1)
    np = max(alm_form.cleaned_data['alm_np'], nx * 2)
    name = alm_form.cleaned_data['alm_form_names'].alm_file.path
    return {
        'lmax': lmax,
        'lmin': lmin,
        'np': np,
        'nx': nx,
        'name': name,
    }


def get_image_form_cuts(image_form):
    minv = image_form.cleaned_data['map_image_minv']
    maxv = image_form.cleaned_data['map_image_maxv']
    if (minv == None) or (maxv == None):
        res = 'native'
    else:
        res = '{},{}'.format(minv, maxv)
    return res


def get_forms(request=None):
    res = None
    args = {'data': None, 'files': None}
    if request:
        args = {'data': request.POST, 'files': request.FILES}
    res = {
        'alm_form': AlmForm(**args),
        'image_form': MapImageForm(error_class=HiddenErrorList, **args),
        'mask_form': MaskForm(error_class=HiddenErrorList, **args),
        'ps_form': PointSourceForm(error_class=HiddenErrorList, **args),
        'cut_form': MapZoneCutFrom(error_class=HiddenErrorList, **args),
        'smooth_form': SmoothForm(error_class=HiddenErrorList, **args),
    }
    return res


def get_zone_cuts(cut_form):
    res = False
    if None not in cut_form.cleaned_data.values():
        print('!!!!!!!!! {}'.format(cut_form.cleaned_data))
        res = '{map_zone_cut_lat1}d,{map_zone_cut_lon1}d,{map_zone_cut_lat2}d,{map_zone_cut_lon2}d'. \
            format(**cut_form.cleaned_data)
    return res


def get_name_in_media(dir, out_name=None, suffix=None, **kwargs):
    res = out_name
    if not res:
        out_name = NamedTemporaryFile(
            dir=os.path.join(settings.MEDIA_ROOT, dir),
            suffix='_'.join([str(int(time.time())), suffix]),
            **kwargs
        )
        res = out_name.name
    return res


def get_cut_gif_params(cuts, map_to_gif_params):
    cuts_gif_params = map_to_gif_params.copy()
    cuts_gif_params['K'] = None
    cuts_gif_params['keep'] = cuts
    cuts_gif_params['gif_name'] = get_name_in_media(dir=settings.MEDIA_ALM2MAP_IMAGE, suffix='map.gif')
    return cuts_gif_params


def map_to_gif_params_init(map_to_gif_params, my_map):
    map_to_gif_params['Cs'] = 'native'
    map_to_gif_params['map_name'] = my_map.name
    map_to_gif_params['gif_name'] = get_name_in_media(dir=settings.MEDIA_ALM2MAP_IMAGE, suffix='map.gif')
    map_to_gif_params['notitle'] = None


@receiver(pre_delete, sender=Session)
def free_session(sender, instance, **kwargs):
    print('PRE_DELETING SESSION FILES')

@receiver(pre_save, sender=Session)
def pre_save_session(sender, instance, **kwargs):
    print('PRE_SAVING SESSION FILES')


def alm_form_view(request):
    if not hasattr(request.session, 'files'):
        request.session['files'] = []

    print('!!!!!!!!!!!!!!!!!!! {}'.format(request.session['files']))

    if request.method == 'POST':
        forms = get_forms(request)
        map_to_gif_params = {}
        if forms['alm_form'].is_valid():
            alm_attrs = get_alm_form_data(forms['alm_form'])
            forms_and_data = {'forms': forms.values()}
            my_alm = galm(**alm_attrs)

            if forms['smooth_form'].is_valid():
                my_alm = my_alm.smooth(forms['smooth_form'].cleaned_data['smooth_value'])

            alm_to_map_params = alm_attrs.copy()
            alm_to_map_params.pop('name')
            alm_to_map_params['map_name'] = get_name_in_media(dir=settings.MEDIA_ALM2MAP_MAP, suffix='map.fit')
            request.session['files'].append(alm_to_map_params['map_name'])
            my_map = my_alm.to_map(**alm_to_map_params)
            map_to_gif_params_init(map_to_gif_params, my_map)

            if forms['image_form'].is_valid():
                cuts = get_image_form_cuts(forms['image_form'])
                map_to_gif_params['Cs'] = cuts

            if forms['ps_form'].is_valid():
                ps_file = PointSource(
                    name=forms['ps_form'].cleaned_data['point_source_file'].temporary_file_path(),
                )
                ps_map = ps_file.to_pixelmap(**my_map.get_attrs())
                my_map.add_map(ps_map, c1=-forms['ps_form'].cleaned_data['ps_mult'])
                request.session['files'].append(ps_file.name)

            if forms['mask_form'].is_valid():
                try:
                    mask_path = forms['mask_form'].cleaned_data['mask_names'].mask_file.path
                    masked = conv.mask_map(
                        my_map.name,
                        mask_path,
                        **alm_attrs
                    )
                    my_map.name = masked
                except:
                    conv.tools.debug('Unable to add mask')

            if forms['cut_form'].is_valid():
                cuts = get_zone_cuts(forms['cut_form'])
                if cuts:
                    print('!!!!!!!!!!!!!!1  {}'.format(cuts))
                    cuts_gif_params = get_cut_gif_params(cuts, map_to_gif_params)
                    map_zone_gif = conv.map_to_gif(**cuts_gif_params)
                    forms_and_data['cut'] = os.path.basename(map_zone_gif)
                    map_to_gif_params['cut'] = cuts
                    request.session['files'].append(cuts_gif_params['gif_name'])

            map_to_gif_params['map_name'] = my_map.name
            gif = conv.map_to_gif(**map_to_gif_params)
            request.session['files'].append(gif)

            forms_and_data.update({
                'map': os.path.basename(gif),
                'fit': os.path.basename(my_map.name),
            })
            res = render_to_response(
                'alm2map/result.html',
                forms_and_data,
                context_instance=RequestContext(request),
            )
        else:
            res = render_to_response(
                'alm2map/index.html',
                {'forms': forms.values()},
                context_instance=RequestContext(request),
            )
    else:
        forms = get_forms()
        res = render_to_response(
            'alm2map/index.html',
            {'forms': forms.values()},
            context_instance=RequestContext(request),
        )
    print('!!!!!!!!!!!!!!!!!!! {}'.format(request.session['files']))
    request.session.save()
    return res
