# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Puzzle'
        db.create_table(u'puzzle_puzzle', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('description', self.gf('django.db.models.fields.TextField')()),
        ))
        db.send_create_signal(u'puzzle', ['Puzzle'])

        # Adding model 'Dataset'
        db.create_table(u'puzzle_dataset', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('puzzle', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['puzzle.Puzzle'])),
            ('scale', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('score', self.gf('django.db.models.fields.IntegerField')(default=10)),
            ('data', self.gf('django.db.models.fields.files.FileField')(max_length=100)),
            ('solution', self.gf('django.db.models.fields.files.FileField')(max_length=100)),
        ))
        db.send_create_signal(u'puzzle', ['Dataset'])

        # Adding model 'UserProfile'
        db.create_table(u'puzzle_userprofile', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.OneToOneField')(related_name='profile', unique=True, to=orm['auth.User'])),
            ('student_type', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('desc', self.gf('django.db.models.fields.TextField')()),
            ('score', self.gf('django.db.models.fields.IntegerField')(default=0)),
        ))
        db.send_create_signal(u'puzzle', ['UserProfile'])

        # Adding model 'Answer'
        db.create_table(u'puzzle_answer', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('dataset', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['puzzle.Dataset'])),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['puzzle.UserProfile'])),
            ('answer', self.gf('django.db.models.fields.files.FileField')(max_length=100)),
            ('source_code', self.gf('django.db.models.fields.files.FileField')(max_length=100)),
            ('submitted_time', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2014, 4, 15, 0, 0))),
            ('result', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal(u'puzzle', ['Answer'])


    def backwards(self, orm):
        # Deleting model 'Puzzle'
        db.delete_table(u'puzzle_puzzle')

        # Deleting model 'Dataset'
        db.delete_table(u'puzzle_dataset')

        # Deleting model 'UserProfile'
        db.delete_table(u'puzzle_userprofile')

        # Deleting model 'Answer'
        db.delete_table(u'puzzle_answer')


    models = {
        u'auth.group': {
            'Meta': {'object_name': 'Group'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        u'auth.permission': {
            'Meta': {'ordering': "(u'content_type__app_label', u'content_type__model', u'codename')", 'unique_together': "((u'content_type', u'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True', 'to': u"orm['auth.Group']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True', 'to': u"orm['auth.Permission']"}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'puzzle.answer': {
            'Meta': {'object_name': 'Answer'},
            'answer': ('django.db.models.fields.files.FileField', [], {'max_length': '100'}),
            'dataset': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['puzzle.Dataset']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'result': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'source_code': ('django.db.models.fields.files.FileField', [], {'max_length': '100'}),
            'submitted_time': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2014, 4, 15, 0, 0)'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['puzzle.UserProfile']"})
        },
        u'puzzle.dataset': {
            'Meta': {'object_name': 'Dataset'},
            'data': ('django.db.models.fields.files.FileField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'puzzle': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['puzzle.Puzzle']"}),
            'scale': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'score': ('django.db.models.fields.IntegerField', [], {'default': '10'}),
            'solution': ('django.db.models.fields.files.FileField', [], {'max_length': '100'})
        },
        u'puzzle.puzzle': {
            'Meta': {'object_name': 'Puzzle'},
            'description': ('django.db.models.fields.TextField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'puzzle.userprofile': {
            'Meta': {'object_name': 'UserProfile'},
            'desc': ('django.db.models.fields.TextField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'score': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'student_type': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'user': ('django.db.models.fields.related.OneToOneField', [], {'related_name': "'profile'", 'unique': 'True', 'to': u"orm['auth.User']"})
        }
    }

    complete_apps = ['puzzle']