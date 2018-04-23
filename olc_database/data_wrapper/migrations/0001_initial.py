# Generated by Django 2.0.4 on 2018-04-23 15:52

from django.conf import settings
import django.contrib.postgres.fields
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='LSTSData',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('lsts_id', models.CharField(max_length=88)),
                ('country_of_origin', models.CharField(max_length=128)),
                ('food', models.CharField(max_length=128)),
            ],
        ),
        migrations.CreateModel(
            name='ResFinderData',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('resfinder_gene', models.CharField(max_length=56)),
                ('resfinder_allele', models.IntegerField()),
                ('resfinder_resistance', models.CharField(max_length=64)),
                ('resfinder_percent_identity', models.FloatField()),
                ('resfinder_percent_covered', models.FloatField()),
                ('resfinder_contig', models.CharField(max_length=128)),
                ('resfinder_location', models.CharField(max_length=64)),
                ('resfinder_sequence', models.CharField(max_length=8192)),
                ('resfinder_aa_identity', models.CharField(max_length=64)),
            ],
        ),
        migrations.CreateModel(
            name='Sample',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('seqid', models.CharField(max_length=56)),
            ],
        ),
        migrations.CreateModel(
            name='SavedQueries',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('search_terms', django.contrib.postgres.fields.ArrayField(base_field=models.CharField(max_length=48), size=None)),
                ('search_attributes', django.contrib.postgres.fields.ArrayField(base_field=models.CharField(max_length=48), size=None)),
                ('search_operations', django.contrib.postgres.fields.ArrayField(base_field=models.CharField(max_length=48), size=None)),
                ('search_combine_operations', django.contrib.postgres.fields.ArrayField(base_field=models.CharField(max_length=48), size=None)),
                ('query_name', models.CharField(max_length=256)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='SeqData',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('genus', models.CharField(max_length=128)),
                ('n50', models.IntegerField()),
                ('num_contigs', models.IntegerField()),
                ('rmlst', models.CharField(max_length=56)),
                ('sequencing_date', models.DateTimeField()),
                ('analyst', models.CharField(max_length=128)),
                ('sample_purity', models.CharField(max_length=64)),
                ('assembly_quality', models.CharField(max_length=64)),
                ('total_length', models.IntegerField()),
                ('mean_insert_size', models.FloatField()),
                ('insert_size_std', models.FloatField()),
                ('average_coverage_depth', models.FloatField()),
                ('coverage_depth_std', models.FloatField()),
                ('percent_gc', models.FloatField()),
                ('mash_reference_genome', models.CharField(max_length=256)),
                ('mash_num_matching_hashes', models.CharField(max_length=128)),
                ('sixteens_result', models.CharField(max_length=256)),
                ('mlst', models.CharField(max_length=56)),
                ('mlst_allele_1', models.CharField(max_length=56)),
                ('mlst_allele_2', models.CharField(max_length=56)),
                ('mlst_allele_3', models.CharField(max_length=56)),
                ('mlst_allele_4', models.CharField(max_length=56)),
                ('mlst_allele_5', models.CharField(max_length=56)),
                ('mlst_allele_6', models.CharField(max_length=56)),
                ('mlst_allele_7', models.CharField(max_length=56)),
                ('core_genes_present', models.CharField(max_length=128)),
                ('ecoli_serotype', models.CharField(max_length=128)),
                ('sistr_serovar_antigen', models.CharField(max_length=512)),
                ('sistr_serovar_cgmlst', models.CharField(max_length=56)),
                ('sistr_serovar_serogroup', models.CharField(max_length=56)),
                ('sistr_serovar_h1', models.CharField(max_length=56)),
                ('sistr_serovar_h2', models.CharField(max_length=56)),
                ('sistr_serovar_serovar', models.CharField(max_length=56)),
                ('geneseekr_profile', models.CharField(max_length=128)),
                ('vtyper_profile', models.CharField(max_length=128)),
                ('amr_profile', models.CharField(max_length=512)),
                ('amr_resistant', models.CharField(max_length=56)),
                ('plasmid_profile', models.CharField(max_length=128)),
                ('total_predicted_genes', models.IntegerField()),
                ('predicted_genes_over_3000', models.IntegerField()),
                ('predicted_genes_over_1000', models.IntegerField()),
                ('predicted_genes_over_500', models.IntegerField()),
                ('predicted_genes_under_500', models.IntegerField()),
                ('num_clusters_pf', models.IntegerField()),
                ('percent_reads_phix', models.FloatField()),
                ('error_rate', models.FloatField()),
                ('length_forward_read', models.FloatField()),
                ('length_reverse_read', models.FloatField()),
                ('real_time_strain', models.CharField(max_length=64)),
                ('flowcell', models.CharField(max_length=128)),
                ('machine_name', models.CharField(max_length=64)),
                ('pipeline_version', models.CharField(max_length=64)),
                ('date_assembled', models.DateTimeField()),
                ('seqid', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='seqdata', to='data_wrapper.Sample')),
            ],
        ),
        migrations.AddField(
            model_name='resfinderdata',
            name='seqid',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='resfinder_data', to='data_wrapper.Sample'),
        ),
        migrations.AddField(
            model_name='lstsdata',
            name='seqid',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='lsts_data', to='data_wrapper.Sample'),
        ),
    ]
