# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2018-07-24 16:46
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import otree.db.models
import otree_save_the_change.mixins


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('otree', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Group',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('id_in_subsession', otree.db.models.PositiveIntegerField(db_index=True, null=True)),
                ('round_number', otree.db.models.PositiveIntegerField(db_index=True, null=True)),
                ('session', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='game1_group', to='otree.Session')),
            ],
            options={
                'db_table': 'game1_group',
            },
            bases=(otree_save_the_change.mixins.SaveTheChange, models.Model),
        ),
        migrations.CreateModel(
            name='Player',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('id_in_group', otree.db.models.PositiveIntegerField(db_index=True, null=True)),
                ('_payoff', otree.db.models.CurrencyField(default=0, null=True)),
                ('round_number', otree.db.models.PositiveIntegerField(db_index=True, null=True)),
                ('_gbat_arrived', otree.db.models.BooleanField(choices=[(True, 'Yes'), (False, 'No')], default=False)),
                ('_gbat_grouped', otree.db.models.BooleanField(choices=[(True, 'Yes'), (False, 'No')], default=False)),
                ('game1_score', otree.db.models.IntegerField(null=True)),
                ('game1_rank', otree.db.models.IntegerField(null=True)),
                ('game1_bonus', otree.db.models.IntegerField(null=True)),
                ('attempted', otree.db.models.IntegerField(null=True)),
                ('firm', otree.db.models.StringField(max_length=10000, null=True)),
                ('switch', otree.db.models.StringField(max_length=10000, null=True)),
                ('c5', otree.db.models.StringField(choices=[('Yes', 'Yes'), ('No', 'No')], max_length=10000, null=True)),
                ('c10', otree.db.models.StringField(choices=[('Yes', 'Yes'), ('No', 'No')], max_length=10000, null=True)),
                ('c15', otree.db.models.StringField(choices=[('Yes', 'Yes'), ('No', 'No')], max_length=10000, null=True)),
                ('c20', otree.db.models.StringField(choices=[('Yes', 'Yes'), ('No', 'No')], max_length=10000, null=True)),
                ('c25', otree.db.models.StringField(choices=[('Yes', 'Yes'), ('No', 'No')], max_length=10000, null=True)),
                ('c30', otree.db.models.StringField(choices=[('Yes', 'Yes'), ('No', 'No')], max_length=10000, null=True)),
                ('c35', otree.db.models.StringField(choices=[('Yes', 'Yes'), ('No', 'No')], max_length=10000, null=True)),
                ('c40', otree.db.models.StringField(choices=[('Yes', 'Yes'), ('No', 'No')], max_length=10000, null=True)),
                ('c45', otree.db.models.StringField(choices=[('Yes', 'Yes'), ('No', 'No')], max_length=10000, null=True)),
                ('c50', otree.db.models.StringField(choices=[('Yes', 'Yes'), ('No', 'No')], max_length=10000, null=True)),
                ('time_ChooseFirm', otree.db.models.StringField(max_length=10000, null=True)),
                ('time_Instructions1', otree.db.models.StringField(max_length=10000, null=True)),
                ('time_Game1', otree.db.models.StringField(max_length=10000, null=True)),
                ('time_Results1', otree.db.models.StringField(max_length=10000, null=True)),
                ('q6', otree.db.models.StringField(max_length=10000, null=True, verbose_name='Why did you choose this firm?')),
                ('group', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='game1.Group')),
                ('participant', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='game1_player', to='otree.Participant')),
                ('session', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='game1_player', to='otree.Session')),
            ],
            options={
                'db_table': 'game1_player',
            },
            bases=(otree_save_the_change.mixins.SaveTheChange, models.Model),
        ),
        migrations.CreateModel(
            name='Subsession',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('round_number', otree.db.models.PositiveIntegerField(db_index=True, null=True)),
                ('session', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='game1_subsession', to='otree.Session')),
            ],
            options={
                'db_table': 'game1_subsession',
            },
            bases=(otree_save_the_change.mixins.SaveTheChange, models.Model),
        ),
        migrations.AddField(
            model_name='player',
            name='subsession',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='game1.Subsession'),
        ),
        migrations.AddField(
            model_name='group',
            name='subsession',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='game1.Subsession'),
        ),
    ]
