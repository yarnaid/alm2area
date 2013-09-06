import os
from django.db import models
import time
from glespy.alm import Alm as gAlm
from cmb import settings

from django.core.files.temp import NamedTemporaryFile
from os.path import join

from django.db.models.signals import pre_save, pre_delete
from django.dispatch import receiver

# Create your models here.


def print_name(func):
    if settings.DEBUG:
        print('[{}]: start'.format(func.__name__))
    return func

class Alm(models.Model):
    alm_file = models.FileField('alms', upload_to=settings.MEDIA_ALM2AREA_ALM)
    alm_name = models.CharField(max_length=100)
    alm_lmax = models.PositiveIntegerField('l_max', default=10)
    alm_lmin = models.PositiveIntegerField('l_min', default=1)

    def __unicode__(self):
        return '{} {}-{}'.format(self.alm_name, self.alm_lmin, self.alm_lmax)

    def __str__(self):
        return '{}'.format(self.alm_name)


    class Meta:
        ordering = ('alm_lmax', 'alm_lmin')
        verbose_name = 'a_lm'
        verbose_name_plural = "a_lm's"


class Mask(models.Model):
    mask_file = models.FileField(
        'Mask file',
        max_length=300,
        upload_to=settings.MEDIA_ALM2AREA_MASK
    )
    mask_name = models.CharField(
        max_length=100,
        null=True,
        blank=True,
    )

    def __unicode__(self):
        return '{}'.format(self.mask_name)


# class MapImage(models.Model):
#     map_image_name = models.FileField(null=True,
#                                       upload_to='alm2area',
#     )
#     map_image_maxv = models.FloatField('Max cut value', null=True, blank=True)
#     map_image_minv = models.FloatField('Min cut value', null=True, blank=True)


class CalculatedMap(models.Model):
    calculated_map_lmax = models.PositiveIntegerField()
    calculated_map_lmin = models.PositiveIntegerField()
    calculated_map_nx = models.PositiveIntegerField()
    calculated_map_np = models.PositiveIntegerField()
    calculated_map_name = models.CharField(max_length=300)
    calculated_map_alm = models.ForeignKey(Alm)
    calculated_map_path = models.CharField(max_length=300)

    @print_name
    def calc(self):
        alm = gAlm(name=self.calculated_map_alm.alm_file.path)
        pixel_map = alm.to_map(
            nx=self.calculated_map_nx,
            np=self.calculated_map_np,
            lmax=self.calculated_map_lmax,
            lmin=self.calculated_map_lmin,
            map_name=NamedTemporaryFile(
                dir=join(
                    settings.MEDIA_ROOT,
                    settings.MEDIA_ALM2AREA_MAP,
                ),
                suffix='_'+'_'.join([str(int(time.time())), 'map.fit']),
            ).name
        )
        self.calculated_map_path = pixel_map.name
        return pixel_map

    def __repr__(self):
        return self.calculated_map_name

    def __str__(self):
        return self.calculated_map_name


    def __unicode__(self):
        return self.__str__()

@receiver(pre_save, sender=CalculatedMap)
@print_name
def calc_map_before_save(sender, instance, **kwargs):
    try:
        os.remove(instance.calculated_map_path)
    except:
        pass
    instance.calc()

@receiver(pre_delete, sender=CalculatedMap)
@print_name
def remove_map_with_record(sender, instance, **kwargs):
    try:
        os.remove(instance.calculated_map_path)
    except:
        pass
