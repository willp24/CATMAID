# -*- coding: utf-8 -*-
# Generated by Django 1.10.8 on 2017-10-18 18:26
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone

forward_create_tables = """
    CREATE TABLE point (
        radius real DEFAULT 0 NOT NULL,
        confidence smallint DEFAULT 5 NOT NULL
    )
    INHERITS (location);

    CREATE TABLE point_connector (
        point_id bigint NOT NULL,
        connector_id bigint NOT NULL,
        confidence smallint DEFAULT 5 NOT NULL
    )
    INHERITS (relation_instance);

    CREATE TABLE point_class_instance (
        point_id bigint NOT NULL,
        class_instance_id integer NOT NULL
    )
    INHERITS (relation_instance);


    -- Point constraints
    ALTER TABLE ONLY point
    ADD CONSTRAINT point_pkey PRIMARY KEY (id);

    -- Point Connector constraints
    ALTER TABLE ONLY point_connector
    ADD CONSTRAINT point_connector_pkey PRIMARY KEY (id);

    ALTER TABLE ONLY point_connector
    ADD CONSTRAINT point_connector_project_id_uniq
    UNIQUE (project_id, point_id, connector_id, relation_id);

    ALTER TABLE ONLY point_connector
    ADD CONSTRAINT point_connector_sa_id
    FOREIGN KEY (point_id)
    REFERENCES point(id) DEFERRABLE INITIALLY DEFERRED;

    ALTER TABLE ONLY point_connector
    ADD CONSTRAINT point_connector_connector_id_fkey
    FOREIGN KEY (connector_id)
    REFERENCES connector(id) DEFERRABLE INITIALLY DEFERRED;

    -- Point Class Instance constraints
    ALTER TABLE ONLY point_class_instance
    ADD CONSTRAINT point_class_instance_pkey PRIMARY KEY (id);

    ALTER TABLE ONLY point_class_instance
    ADD CONSTRAINT point_class_instance_sa_id
    FOREIGN KEY (point_id)
    REFERENCES point(id) DEFERRABLE INITIALLY DEFERRED;

    ALTER TABLE ONLY point_class_instance
    ADD CONSTRAINT point_connector_class_instance_id_fkey
    FOREIGN KEY (class_instance_id)
    REFERENCES class_instance(id) DEFERRABLE INITIALLY DEFERRED;


    -- Create history tables
    SELECT create_history_table('point'::regclass, 'edition_time', 'txid');
    SELECT create_history_table('point_connector'::regclass, 'edition_time', 'txid');
    SELECT create_history_table('point_class_instance'::regclass, 'edition_time', 'txid');
"""

backward_create_tables = """
    SELECT disable_history_tracking_for_table('point'::regclass,
        get_history_table_name('point'::regclass));
    SELECT drop_history_table('point'::regclass);

    SELECT disable_history_tracking_for_table('point_connector'::regclass,
        get_history_table_name('point_connector'::regclass));
    SELECT drop_history_table('point_connector'::regclass);

    SELECT disable_history_tracking_for_table('point_class_instance'::regclass,
        get_history_table_name('point_class_instance'::regclass));
    SELECT drop_history_table('point_class_instance'::regclass);

    DROP TABLE point CASCADE;
    DROP TABLE point_connector CASCADE;
    DROP TABLE point_class_instance CASCADE;
"""

class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('catmaid', '0027_update_data_view_name'),
    ]

    operations = [
        migrations.RunSQL(
            forward_create_tables,
            backward_create_tables,
            [
                migrations.CreateModel(
                    name='Point',
                    fields=[
                        ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                        ('creation_time', models.DateTimeField(default=django.utils.timezone.now)),
                        ('edition_time', models.DateTimeField(default=django.utils.timezone.now)),
                        ('location_x', models.FloatField()),
                        ('location_y', models.FloatField()),
                        ('location_z', models.FloatField()),
                        ('radius', models.FloatField(default=0)),
                        ('confidence', models.IntegerField(default=5)),
                        ('editor', models.ForeignKey(db_column='editor_id',
                            on_delete=django.db.models.deletion.CASCADE,
                            related_name='point_editor', to=settings.AUTH_USER_MODEL)),
                        ('project', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='catmaid.Project')),
                        ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                    ],
                    options={
                        'db_table': 'point',
                    }),
                migrations.CreateModel(
                    name='PointClassInstance',
                    fields=[
                        ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                        ('creation_time', models.DateTimeField(default=django.utils.timezone.now)),
                        ('edition_time', models.DateTimeField(default=django.utils.timezone.now)),
                        ('class_instance', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='catmaid.ClassInstance')),
                        ('project', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='catmaid.Project')),
                        ('relation', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='catmaid.Relation')),
                        ('point', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='catmaid.Point')),
                        ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                    ],
                    options={
                        'db_table': 'point_class_instance',
                    },
                ),
                migrations.CreateModel(
                    name='PointConnector',
                    fields=[
                        ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                        ('creation_time', models.DateTimeField(default=django.utils.timezone.now)),
                        ('edition_time', models.DateTimeField(default=django.utils.timezone.now)),
                        ('confidence', models.IntegerField(default=5)),
                        ('connector', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='catmaid.Connector')),
                        ('project', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='catmaid.Project')),
                        ('relation', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='catmaid.Relation')),
                        ('point', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='catmaid.Point')),
                        ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                    ],
                    options={
                        'db_table': 'point_connector',
                    },
                ),
                migrations.AlterUniqueTogether(
                    name='pointconnector',
                    unique_together=set([('project', 'point', 'connector', 'relation')]),
                ),
            ])
    ]
