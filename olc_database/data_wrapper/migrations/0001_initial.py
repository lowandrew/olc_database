# Generated by Django 2.0.4 on 2018-05-09 14:14

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
            name='CultureData',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('received_date', models.DateField()),
                ('gdna_extraction_date', models.DateField()),
                ('gdna_extraction_method', models.CharField(max_length=64)),
                ('gdna_extracted_by', models.CharField(max_length=64)),
                ('quantification_date', models.DateField()),
                ('quantification_method', models.CharField(max_length=64)),
                ('quantified_by', models.CharField(max_length=64)),
                ('concentration', models.FloatField()),
                ('discard_date', models.DateField()),
                ('is_active', models.CharField(choices=[('YES', 'YES'), ('NO', 'NO')], default='NO', max_length=8)),
            ],
        ),
        migrations.CreateModel(
            name='HistoricalCultureData',
            fields=[
                ('id', models.IntegerField(auto_created=True, blank=True, db_index=True, verbose_name='ID')),
                ('received_date', models.DateField()),
                ('gdna_extraction_date', models.DateField()),
                ('gdna_extraction_method', models.CharField(max_length=64)),
                ('gdna_extracted_by', models.CharField(max_length=64)),
                ('quantification_date', models.DateField()),
                ('quantification_method', models.CharField(max_length=64)),
                ('quantified_by', models.CharField(max_length=64)),
                ('concentration', models.FloatField()),
                ('discard_date', models.DateField()),
                ('is_active', models.CharField(choices=[('YES', 'YES'), ('NO', 'NO')], default='NO', max_length=8)),
                ('history_id', models.AutoField(primary_key=True, serialize=False)),
                ('history_date', models.DateTimeField()),
                ('history_change_reason', models.CharField(max_length=100, null=True)),
                ('history_type', models.CharField(choices=[('+', 'Created'), ('~', 'Changed'), ('-', 'Deleted')], max_length=1)),
                ('history_user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'historical culture data',
                'ordering': ('-history_date', '-history_id'),
                'get_latest_by': 'history_date',
            },
        ),
        migrations.CreateModel(
            name='HistoricalLSTSData',
            fields=[
                ('id', models.IntegerField(auto_created=True, blank=True, db_index=True, verbose_name='ID')),
                ('lsts_id', models.CharField(max_length=88)),
                ('country_of_origin', models.CharField(max_length=128)),
                ('food', models.CharField(max_length=128)),
                ('history_id', models.AutoField(primary_key=True, serialize=False)),
                ('history_date', models.DateTimeField()),
                ('history_change_reason', models.CharField(max_length=100, null=True)),
                ('history_type', models.CharField(choices=[('+', 'Created'), ('~', 'Changed'), ('-', 'Deleted')], max_length=1)),
                ('history_user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'historical lsts data',
                'ordering': ('-history_date', '-history_id'),
                'get_latest_by': 'history_date',
            },
        ),
        migrations.CreateModel(
            name='HistoricalOLN',
            fields=[
                ('id', models.IntegerField(auto_created=True, blank=True, db_index=True, verbose_name='ID')),
                ('oln_id', models.CharField(max_length=64)),
                ('extra_lsts_data', models.CharField(max_length=64)),
                ('other_id', models.CharField(max_length=64)),
                ('oln_genus', models.CharField(max_length=64)),
                ('oln_species', models.CharField(max_length=64)),
                ('oln_subspecies', models.CharField(max_length=64)),
                ('oln_serotype', models.CharField(max_length=64)),
                ('oln_verotoxin', models.CharField(max_length=64)),
                ('oln_source', models.CharField(max_length=64)),
                ('oneenzyme', models.CharField(max_length=64)),
                ('twoenzyme', models.CharField(max_length=64)),
                ('history_id', models.AutoField(primary_key=True, serialize=False)),
                ('history_date', models.DateTimeField()),
                ('history_change_reason', models.CharField(max_length=100, null=True)),
                ('history_type', models.CharField(choices=[('+', 'Created'), ('~', 'Changed'), ('-', 'Deleted')], max_length=1)),
                ('history_user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'historical oln',
                'ordering': ('-history_date', '-history_id'),
                'get_latest_by': 'history_date',
            },
        ),
        migrations.CreateModel(
            name='HistoricalResFinderData',
            fields=[
                ('id', models.IntegerField(auto_created=True, blank=True, db_index=True, verbose_name='ID')),
                ('resfinder_gene', models.CharField(max_length=56)),
                ('resfinder_allele', models.IntegerField()),
                ('resfinder_resistance', models.CharField(max_length=64)),
                ('resfinder_percent_identity', models.FloatField()),
                ('resfinder_percent_covered', models.FloatField()),
                ('resfinder_contig', models.CharField(max_length=128)),
                ('resfinder_location', models.CharField(max_length=64)),
                ('resfinder_sequence', models.CharField(max_length=8192)),
                ('resfinder_aa_identity', models.CharField(max_length=64)),
                ('history_id', models.AutoField(primary_key=True, serialize=False)),
                ('history_date', models.DateTimeField()),
                ('history_change_reason', models.CharField(max_length=100, null=True)),
                ('history_type', models.CharField(choices=[('+', 'Created'), ('~', 'Changed'), ('-', 'Deleted')], max_length=1)),
                ('history_user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'historical res finder data',
                'ordering': ('-history_date', '-history_id'),
                'get_latest_by': 'history_date',
            },
        ),
        migrations.CreateModel(
            name='HistoricalSeqData',
            fields=[
                ('id', models.IntegerField(auto_created=True, blank=True, db_index=True, verbose_name='ID')),
                ('seqid', models.CharField(max_length=64)),
                ('genus', models.CharField(max_length=128)),
                ('n50', models.IntegerField()),
                ('num_contigs', models.IntegerField()),
                ('rmlst', models.CharField(max_length=56)),
                ('sequencing_date', models.DateField()),
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
                ('date_assembled', models.DateField()),
                ('history_id', models.AutoField(primary_key=True, serialize=False)),
                ('history_date', models.DateTimeField()),
                ('history_change_reason', models.CharField(max_length=100, null=True)),
                ('history_type', models.CharField(choices=[('+', 'Created'), ('~', 'Changed'), ('-', 'Deleted')], max_length=1)),
                ('history_user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'historical seq data',
                'ordering': ('-history_date', '-history_id'),
                'get_latest_by': 'history_date',
            },
        ),
        migrations.CreateModel(
            name='HistoricalSeqTracking',
            fields=[
                ('id', models.IntegerField(auto_created=True, blank=True, db_index=True, verbose_name='ID')),
                ('priority', models.CharField(max_length=128)),
                ('curator_flag', models.CharField(max_length=128)),
                ('comment', models.CharField(max_length=512)),
                ('history_id', models.AutoField(primary_key=True, serialize=False)),
                ('history_date', models.DateTimeField()),
                ('history_change_reason', models.CharField(max_length=100, null=True)),
                ('history_type', models.CharField(choices=[('+', 'Created'), ('~', 'Changed'), ('-', 'Deleted')], max_length=1)),
                ('history_user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'historical seq tracking',
                'ordering': ('-history_date', '-history_id'),
                'get_latest_by': 'history_date',
            },
        ),
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
            name='OLN',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('oln_id', models.CharField(max_length=64)),
                ('extra_lsts_data', models.CharField(max_length=64)),
                ('other_id', models.CharField(max_length=64)),
                ('oln_genus', models.CharField(max_length=64)),
                ('oln_species', models.CharField(max_length=64)),
                ('oln_subspecies', models.CharField(max_length=64)),
                ('oln_serotype', models.CharField(max_length=64)),
                ('oln_verotoxin', models.CharField(max_length=64)),
                ('oln_source', models.CharField(max_length=64)),
                ('oneenzyme', models.CharField(max_length=64)),
                ('twoenzyme', models.CharField(max_length=64)),
                ('lsts_id', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='data_wrapper.LSTSData')),
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
            name='SavedTables',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('table_attributes', django.contrib.postgres.fields.ArrayField(base_field=models.CharField(max_length=128), size=None)),
                ('table_name', models.CharField(max_length=256)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='SeqData',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('seqid', models.CharField(max_length=64)),
                ('genus', models.CharField(max_length=128)),
                ('n50', models.IntegerField()),
                ('num_contigs', models.IntegerField()),
                ('rmlst', models.CharField(max_length=56)),
                ('sequencing_date', models.DateField()),
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
                ('date_assembled', models.DateField()),
                ('lsts_id', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='data_wrapper.LSTSData')),
                ('oln_id', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='data_wrapper.OLN')),
            ],
        ),
        migrations.CreateModel(
            name='SeqIdList',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('seqid_list', django.contrib.postgres.fields.ArrayField(base_field=models.CharField(max_length=48), size=None)),
            ],
        ),
        migrations.CreateModel(
            name='SeqTracking',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('priority', models.CharField(max_length=128)),
                ('curator_flag', models.CharField(max_length=128)),
                ('comment', models.CharField(max_length=512)),
                ('lsts_id', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='data_wrapper.LSTSData')),
                ('oln_id', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='data_wrapper.OLN')),
                ('seqid', models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to='data_wrapper.SeqData')),
            ],
        ),
        migrations.AddField(
            model_name='resfinderdata',
            name='seqid',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='resfinder_data', to='data_wrapper.SeqData'),
        ),
        migrations.AddField(
            model_name='historicalseqtracking',
            name='lsts_id',
            field=models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='data_wrapper.LSTSData'),
        ),
        migrations.AddField(
            model_name='historicalseqtracking',
            name='oln_id',
            field=models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='data_wrapper.OLN'),
        ),
        migrations.AddField(
            model_name='historicalseqtracking',
            name='seqid',
            field=models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='data_wrapper.SeqData'),
        ),
        migrations.AddField(
            model_name='historicalseqdata',
            name='lsts_id',
            field=models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='data_wrapper.LSTSData'),
        ),
        migrations.AddField(
            model_name='historicalseqdata',
            name='oln_id',
            field=models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='data_wrapper.OLN'),
        ),
        migrations.AddField(
            model_name='historicalresfinderdata',
            name='seqid',
            field=models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='data_wrapper.SeqData'),
        ),
        migrations.AddField(
            model_name='historicaloln',
            name='lsts_id',
            field=models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='data_wrapper.LSTSData'),
        ),
        migrations.AddField(
            model_name='historicalculturedata',
            name='oln_id',
            field=models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='data_wrapper.OLN'),
        ),
        migrations.AddField(
            model_name='culturedata',
            name='oln_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='data_wrapper.OLN'),
        ),
    ]