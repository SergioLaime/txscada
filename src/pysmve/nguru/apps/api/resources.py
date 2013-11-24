from apps.hmi.models import Formula, SVGElement, SVGScreen
from apps.mara.models import AI, COMaster, DI, Energy, Event, IED, Profile, SV
from tastypie import fields
from tastypie.api import Api
from tastypie.authorization import Authorization
from tastypie.resources import ALL, ALL_WITH_RELATIONS, ModelResource
from datetime import datetime

# API Entry Point
api = Api(api_name='v1')
auth = Authorization()

class ProfileResource(ModelResource):

    """REST resource for Profile"""
    class Meta:
        resource_name = 'profile'
        queryset = Profile.objects.all()
        allowed_methods = ['get', ]
        ordering = SVGElement._meta.get_all_field_names()

api.register(ProfileResource())


class COMasterResource(ModelResource):

    """REST resource for COMaster"""
    class Meta:
        resource_name = 'comaster'
        queryset = COMaster.objects.all()
        allowed_methods = ['get', ]
        ordering = SVGElement._meta.get_all_field_names()

api.register(COMasterResource())


class IEDResource(ModelResource):

    """REST resource for IED"""
    class Meta:
        resource_name = 'ied'
        queryset = IED.objects.all()
        allowed_methods = ['get', ]
        ordering = SVGElement._meta.get_all_field_names()
api.register(IEDResource())


class SVResource(ModelResource):

    """REST resource for SV"""
    class Meta:
        resource_name = 'sv'
        queryset = SV.objects.all()
        allowed_methods = ['get', ]
        ordering = SVGElement._meta.get_all_field_names()
api.register(SVResource())


class DIResource(ModelResource):

    """REST resource for DI"""
    class Meta:
        resource_name = 'di'
        queryset = DI.objects.all()
        allowed_methods = ['get', ]
        ordering = SVGElement._meta.get_all_field_names()
api.register(DIResource())


class EventResource(ModelResource):

    """REST resource for Event"""
    class Meta:
        resource_name = 'event'
        queryset = Event.objects.all()
        allowed_methods = ['get', 'put']
        filtering = {
            'timestamp': ALL,
            'pk': ALL,
            'timestamp_ack': ALL,
        }
        ordering = Event._meta.get_all_field_names()
        authorization = auth
        order_by = ('-timestamp')

    def dehydrate(self, bundle):
        bundle.data['tag'] = bundle.obj.di.tag
        bundle.data['texto'] = unicode(bundle.obj)
        return bundle

    def obj_update(self, bundle, skip_errors=False, **kwargs):
        """
        A ORM-specific implementation of ``obj_update``.
        """
        if not bundle.obj or not self.get_bundle_detail_data(bundle):
            try:
                lookup_kwargs = self.lookup_kwargs_with_identifiers(bundle, kwargs)
            except:
                # if there is trouble hydrating the data, fall back to just
                # using kwargs by itself (usually it only contains a "pk" key
                # and this will work fine.
                lookup_kwargs = kwargs

            try:
                bundle.obj = self.obj_get(bundle=bundle, **lookup_kwargs)
            except Event.ObjectDoesNotExist:
                raise NotFound("A model instance matching the provided arguments could not be found.")

        self.authorized_update_detail(self.get_object_list(bundle.request), bundle)

        if bundle.data.get('timestamp_ack', None) == 'now':
            bundle.data['timestamp_ack'] = datetime.now()

        bundle = self.full_hydrate(bundle)
        return self.save(bundle, skip_errors=skip_errors)



api.register(EventResource())


class AIResource(ModelResource):

    """REST resource for AI"""
    class Meta:
        resource_name = 'ai'
        queryset = AI.objects.all()
        allowed_methods = ['get', ]
        ordering = SVGElement._meta.get_all_field_names()
api.register(AIResource())


# class EnergyPointResource(ModelResource):
#     """REST resource for EnergyPoint"""
#     class Meta:
#         resource_name = 'energypoint'
#         queryset = EnergyPoint.objects.all()
#         allowed_methods = ['get', ]


class EnergyResource(ModelResource):

    """REST resource for Energy"""
    class Meta:
        resource_name = 'energy'
        queryset = Energy.objects.all()
        allowed_methods = ['get', ]
        ordering = SVGElement._meta.get_all_field_names()
api.register(EnergyResource())


class SVGScreenResource(ModelResource):

    """REST resource for SVGScreen"""

    profile = fields.ForeignKey(ProfileResource, 'profile')
    parent = fields.ForeignKey('self', 'parent', null=True, blank=True)

    class Meta:
        resource_name = 'svgscreen'
        queryset = SVGScreen.objects.all()
        allowed_methods = ['get', ]
        filtering = {
            'name': ALL,
            'id': ALL,
            'profile': ALL,
        }
        ordering = SVGElement._meta.get_all_field_names()
api.register(SVGScreenResource())


class FormulaResource(ModelResource):

    class Meta:
        resource_name = 'formula'
        queryset = Formula.objects.select_related('svg_element')
        allowed_methods = ['get', ]
        ordering = SVGElement._meta.get_all_field_names()

    def dehydrate(self, bundle):
        bundle.data['tag'] = bundle.obj.target.tag
        return bundle


api.register(FormulaResource())


class SVGElementResource(ModelResource):
    '''This resource allows to put updates on the screen'''
    screen = fields.ForeignKey(SVGScreenResource, 'screen')

    class Meta:
        resource_name = 'svgelement'
        queryset = SVGElement.objects.select_related('formula')
        allowed_methods = ['get', ]
        limit = 200
        filtering = {
            'screen': ALL_WITH_RELATIONS,
            'last_update': ALL_WITH_RELATIONS,
            'enabled': ALL_WITH_RELATIONS,
        }
        ordering = SVGElement._meta.get_all_field_names()
        order_by = 'last_update'


    def dehydrate(self, bundle):
        bundle.data['style'] = bundle.obj.style
        return bundle

api.register(SVGElementResource())


class SVGElementDetailResource(ModelResource):
    screen = fields.ForeignKey(SVGScreenResource, 'screen')
    on_click_jump = fields.ForeignKey(SVGScreenResource,
                                      'on_click_jump',
                                      blank=True,
                                      null=True,
                                      )

    formulas = fields.ToManyField(FormulaResource, 'formula_set', full=True)

    def dehydrate(self, bundle):
        #bundle.data['formulas'] = bundle.obj.formulas
        return bundle

    class Meta:
        resource_name = 'svgelementdetail'
        queryset = SVGElement.objects.select_related('formula', 'screen')
        allowed_methods = ['get', ]
        limit = 200
        filtering = {
            'screen': ALL_WITH_RELATIONS,
            'last_update': ALL_WITH_RELATIONS,
            'enabled': ALL_WITH_RELATIONS,
            'on_click_jump': ALL,
        }
        ordering = SVGElement._meta.get_all_field_names()
        order_by = 'last_update'

api.register(SVGElementDetailResource())



# api.register(EnergyPointResource())
