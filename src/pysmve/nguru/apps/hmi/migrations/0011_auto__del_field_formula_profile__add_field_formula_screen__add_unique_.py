# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting field 'Formula.profile'
        db.delete_column('hmi_formula', 'profile_id')

        # Adding field 'Formula.screen'
        db.add_column('hmi_formula', 'screen',
                      self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='formulas', null=True, to=orm['hmi.SVGScreen']),
                      keep_default=False)

        # Adding unique constraint on 'SVGScreen', fields ['prefix', 'profile']
        db.create_unique('hmi_svgscreen', ['prefix', 'profile_id'])


    def backwards(self, orm):
        # Removing unique constraint on 'SVGScreen', fields ['prefix', 'profile']
        db.delete_unique('hmi_svgscreen', ['prefix', 'profile_id'])
        Profile = orm.models['mara.profile']
        p = Profile.objects.all()[0]

        # The following code is provided here to aid in writing a correct migration        # Adding field 'Formula.profile'
        db.add_column('hmi_formula', 'profile',
                      self.gf('django.db.models.fields.related.ForeignKey')(to=orm['mara.Profile']),
                      keep_default=False, default=p.pk,)

        # Deleting field 'Formula.screen'
        db.delete_column('hmi_formula', 'screen_id')


    models = {
        'hmi.color': {
            'Meta': {'object_name': 'Color'},
            'color': ('colorful.fields.RGBColorField', [], {'max_length': '7'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'profile': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['mara.Profile']"})
        },
        'hmi.formula': {
            'Meta': {'object_name': 'Formula'},
            'attribute': ('django.db.models.fields.CharField', [], {'max_length': '16'}),
            'formula': ('django.db.models.fields.TextField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'screen': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'formulas'", 'null': 'True', 'to': "orm['hmi.SVGScreen']"}),
            'tag': ('django.db.models.fields.CharField', [], {'max_length': '16'})
        },
        'hmi.svgelement': {
            'Meta': {'object_name': 'SVGElement'},
            'background': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.CharField', [], {'max_length': '120'}),
            'enabled': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_update': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'mark': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'profile': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['mara.Profile']"}),
            'tag': ('django.db.models.fields.CharField', [], {'max_length': '16'}),
            'text': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True', 'blank': 'True'})
        },
        'hmi.svgpropertychangeset': {
            'Meta': {'object_name': 'SVGPropertyChangeSet', 'db_table': "'color'"},
            'background': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'backgrounds'", 'null': 'True', 'to': "orm['hmi.Color']"}),
            'description': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'foreground': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'foregrounds'", 'null': 'True', 'to': "orm['hmi.Color']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'index': ('django.db.models.fields.IntegerField', [], {}),
            'profile': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['mara.Profile']"})
        },
        'hmi.svgscreen': {
            'Meta': {'unique_together': "(('prefix', 'profile'),)", 'object_name': 'SVGScreen'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '60'}),
            'parent': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'children'", 'null': 'True', 'to': "orm['hmi.SVGScreen']"}),
            'prefix': ('django.db.models.fields.CharField', [], {'max_length': '4'}),
            'profile': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['mara.Profile']"}),
            'root': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'svg': ('django.db.models.fields.files.FileField', [], {'max_length': '100'})
        },
        'mara.profile': {
            'Meta': {'unique_together': "(('name', 'version'),)", 'object_name': 'Profile'},
            'default': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '80'}),
            'version': ('django.db.models.fields.IntegerField', [], {'default': '1'})
        }
    }

    complete_apps = ['hmi']