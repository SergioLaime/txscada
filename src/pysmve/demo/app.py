# encoding: utf-8

from flask import Flask, render_template, jsonify, request
from jinja2 import FileSystemLoader
import os
from utils.decorators import stacktraceable
from utils.marshall import dumps
from datetime import *


ROOT_PATH = os.path.dirname(__file__)
template_path = 'templates'
app = Flask(__name__)
app.jinja_loader = FileSystemLoader(os.path.join(ROOT_PATH, template_path))

# Base de datos
import models

# Test purposue
from random import seed, randrange
seed(os.getpid())
from utils.datatable import parseparams
#--------------------------------------------------------------------
# Contex processors y cosas para los temapltes
#--------------------------------------------------------------------

@app.context_processor
def static_url():
    return dict(STATIC_URL = '/static/')

@app.context_processor
def publish_models():
    import peewee
    d = {}
    for name in dir(models): 
        obj = getattr(models, name)
        try:
            assert issubclass(obj, peewee.Model)
        except:
            pass
        d[name] = obj
    return d
    
@app.template_filter('draw_table')
def draw_table(table=None, attributes = None, hide_columns = None, name = None):
    '''Renderiza una tabla de peewee conmo una jQuery Datatable
    generado configuración inicial'''
    from operator import attrgetter
    import json
    if not name:
        name = table._meta.model_name
    if not attributes: attributes = ''
    attributes += ' flag="model-datatable" model="%s"' % name
    fields = [field for field in table._meta.fields.values()]
    fields.sort(key=attrgetter('_order'))
    ths = ''.join(['<th>%s</th>' % f.verbose_name for f in fields])
    table = '<table %s>%s</table>' % (attributes or '', '<thead><tr>%s</tr></thead>' % ths)
    # Script initial configuration
    obj = {
        'bProcessing': True,
        'bServerSide': True,
        'bJQueryUI': True,
    }
    
    script = '''<script type="text/javascript">
        if (typeof(datatables) == "undefined"){
            datatables = {};
        }
        datatables.%(name)s = %(conf)s;
        </script>''' % dict(conf=json.dumps(obj), name=name)
        
    return '\n'.join([table, script])
    


@app.route("/")
#@stacktraceable
def index():
    """Renders index template"""
    return render_template("index.html", **{
        'tab_conexiones': True,
        'tab_devel': True, 
    })



    
@app.route('/valores/')
def valores():
    '''Retorna valores'''
    rand_pot = lambda : "%.2f Kw" % (randrange(1,250)/10.)
    rand_pot_r = lambda : "%.2f KVa" % (randrange(1,250)/10.)
    rand_current = lambda : "%.2f KVa" % (randrange(1000,5000)/10.)
    rand_volt = lambda : "%.2f V" % (randrange(10000, 14000)/100.)
    
    from models import Profile, COMaster, VarSys, IED, AI, DI
    comaster = Profile.by_name('default').comaster_set.get(address='192.168.1.97')
    
    ied1 = IED.get(co_master=comaster, addr_485_IED=1)
    ied2 = IED.get(co_master=comaster, addr_485_IED=2)
    ied3 = IED.get(co_master=comaster, addr_485_IED=3)
    
    potencia_2 = AI.get(id=2).value
    potencia_2 = ("%s W" % (potencia_2 * 1.09)) if potencia_2 != 0x4000 else '0 KW'
    
    potencia_r_2 = AI.get(id=3).value
    potencia_r_2 = ("%s VA" % (potencia_r_2 * 1.09)) if potencia_r_2 != 0x4000 else '0 KW'
        
    return jsonify({
        # Potencia 
        'potencia-1': rand_pot(),
        #'potencia-2': AI.get(ied=ied2, offset=0).value,
        # FIXME: Indirección correcta
        'potencia-2': potencia_2,
        'potencia-3': rand_pot(),
        'potencia-4': rand_pot(),
        # Potencias reactivas
        'potencia-r-1': rand_pot_r(),
        #'potencia-r-2': AI.get(ied=ied2, offset=1).|value,
        'potencia-r-2': potencia_r_2,
        'potencia-r-3': rand_pot_r(),
        'potencia-r-4': rand_pot_r(),
        # Corrientes
        'corriente-1': rand_current(),
        'corriente-2': rand_current(),
        'corriente-3': rand_current(),
        'corriente-4': rand_current(),
        
        #'tension-1': "%.2f Kv" % AI.get(ied=ied1, offset=0).value,
        'tension-1': "%.2f Kv" % (AI.get(id=1).value /float(100)),  
        
        'interruptor-1': DI.get(ied=ied1, port=1, bit=0).value, 
        'interruptor-2': DI.get(ied=ied1, port=1, bit=1).value,
        })

@app.route('/eventos/')
def eventos():
    '''jQuery datatable inspired json data'''
    data = []
    #print request.values
    options = parseparams(request.values)
    #import ipdb; ipdb.set_trace()
    for i in xrange(options.get('display_length', 10)):
        data.append(["Evento", randrange(1, 10), randrange(1,20), randrange(1, 10)])
    return jsonify(dict(aaData = data))

@app.route('/potencias_historicas/')
def potencias_historicas():
    from datetime import date, time, datetime, timedelta
    d = datetime.combine(date.today(), time(0, 0, 0))
    next = datetime.today() + timedelta(days=1)
    data = []
    while d < next:
        data.append([d, randrange(1,100)])
        d += timedelta(minutes=randrange(1,60))
    return dumps(dict(data=data))

@app.route('/api/comaster/')
def comaster():
    return jsonify({'aaData': []})

def dump(iterable, skip=None):
    if not skip: skip = []
    data = []
    for obj in iterable:
        names = [ name for name in obj._meta.fields.keys() if not name in skip ]
        fields = map(lambda name: (name, getattr(obj, name)), obj._meta.fields.keys())
        data.append(dict(fields))
    return data

@app.route('/api/ais/')
@stacktraceable
def analog_inputs():
    """docstring for analog_inputs"""
    from flask_peewee.serializer import Serializer
    from models import AI
    from json import dumps    
    return dumps(dump(AI.select(), skip=['ied']))


@app.route('/api/events/')
def events():
    '''Events'''
    from datetime import datetime
    import models
    params = parseparams(request.values)
    #models.Profile.get(name='default').comaster_
    events = models.Event.select().order_by(('timestamp', 'desc')).limit(params.get('display_length', 10))
    aaData = []
    for ev in events:
        descs = ['Apertura' if ev.value else 'Cierre     ',  'de Interruptor campo %d' % ev.di.bit, "(%s)" % ev.di, ]
        desc = ' '.join(map(unicode, descs))
        
        aaData.append(["Estacion 1", ev.value, desc, "%s.%.2f" % (ev.timestamp.strftime('%x %X'), ev.subsec)])
    #aaData = [('Estación 1', '1', 'Descripcion %d' % d, datetime.now())
    #          for d in range(10)]
    return dumps(dict(aaData=aaData, iTotalRecords=len(aaData)))


def dateiter(base, limit, step):
    current = base
    while current < limit:
        yield current
        current += step
    
def generate_pq_for_day(a_date, step=None):
    '''
    Genera los 96 valores de energía
    '''
    if not step:
        step = timedelta(minutes=15)
    a_date = datetime.combine(date.today(), time(0, 0, 0))
    limit = a_date + timedelta(days=1)
    maketuple = lambda d: (d.isoformat(), randrange(1, 100), randrange(1, 50), )
    return [ maketuple(d) for d in dateiter(a_date, limit, step)]

@app.route('/api/energy/')
#@stacktraceable
def energy_values():
    '''
    '''
    params = parseparams(request.values)
    
    #print params
    today_midnight = datetime.combine(date.today(), time(0, 0, 0))
    data = generate_pq_for_day(today_midnight)
    #data = data[:params['display_length']]
    
    paged = data[:params.get('display_length', 96)]
    return dumps({
                  'aaData': paged,
                  'iTotalRecords': len(data),
                  #'iTotalDisplayRecords': len(paged),
                  })
    
@app.route('/api/energy/<int:day>/<int:month>/<int:year>/')
@stacktraceable
def energy_by_day(day, month, year):
    from models import Energy
    try:
        assert 1970 <= year <= 2050, "Invalid year"
        base=datetime(year, month, day)
    except ValueError:
        return "Invalid date"
    except AssertionError as e:
        return unicode(e)
    year = int(year)
    month = int(month)
    day = int(day)
    
    start = datetime(year, month, day, 0, 0, 0)
    end = datetime(year, month, day, 23, 59, 59)
    qs = Energy.filter(address=2)
    qs = qs.filter(timestamp__gte=start).filter(timestamp__lt=end)
    qs.order_by('timestamp')
    def maketuple(e):
        return e.timestamp.isoformat(), e.val, e.val
    data = [maketuple(e) for e in qs ]
    
    return dumps(dict(data=data))
