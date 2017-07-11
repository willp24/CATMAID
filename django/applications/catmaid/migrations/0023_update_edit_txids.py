# -*- coding: utf-8 -*-
# Generated by Django 1.10.7 on 2017-07-10 15:00
from __future__ import unicode_literals

from django.db import migrations


forward = """
    CREATE OR REPLACE FUNCTION on_edit() RETURNS trigger
    LANGUAGE plpgsql AS
    $$
    BEGIN
        NEW.edition_time := now();
        NEW.txid := txid_current();
        RETURN NEW;
    END;
    $$;
"""

backward = """
    CREATE OR REPLACE FUNCTION on_edit() RETURNS trigger
    LANGUAGE plpgsql AS
    $$
    BEGIN
        NEW.edition_time := now();
        RETURN NEW;
    END;
    $$;
"""

class Migration(migrations.Migration):
    """This migration updates CATMAID's on_edit() trigger function to not only
    update the edition time, but also the update's transaction ID. This is done
    also by the history tracking update trigger, but history tracking isn't
    enabled everywhere. An up-to-date transaction ID allows to relate table
    updates to the transaction log table.
    """

    dependencies = [
        ('catmaid', '0022_add_reconstruction_sampler_tables'),
    ]

    operations = [
        migrations.RunSQL(forward, backward)
    ]