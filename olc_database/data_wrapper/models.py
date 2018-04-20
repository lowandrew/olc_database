from django.db import models


# Create your models here.
class Sample(models.Model):
    seqid = models.CharField(max_length=56)

    def __str__(self):
        return self.seqid


class SeqData(models.Model):
    seqid = models.ForeignKey(Sample, on_delete=models.CASCADE, related_name='seqdata')
    genus = models.CharField(max_length=128)
    n50 = models.IntegerField()
    num_contigs = models.IntegerField()
    rmlst = models.CharField(max_length=56)
    sequencing_date = models.DateTimeField()
    analyst = models.CharField(max_length=128)
    sample_purity = models.CharField(max_length=64)
    assembly_quality = models.CharField(max_length=64)
    total_length = models.IntegerField()
    mean_insert_size = models.FloatField()
    insert_size_std = models.FloatField()
    average_coverage_depth = models.FloatField()
    coverage_depth_std = models.FloatField()
    percent_gc = models.FloatField()
    mash_reference_genome = models.CharField(max_length=256)
    mash_num_matching_hashes = models.CharField(max_length=128)  # This will maybe need to be changed to non-char.
    sixteens_result = models.CharField(max_length=256)
    mlst = models.CharField(max_length=56)
    mlst_allele_1 = models.CharField(max_length=56)
    mlst_allele_2 = models.CharField(max_length=56)
    mlst_allele_3 = models.CharField(max_length=56)
    mlst_allele_4 = models.CharField(max_length=56)
    mlst_allele_5 = models.CharField(max_length=56)
    mlst_allele_6 = models.CharField(max_length=56)
    mlst_allele_7 = models.CharField(max_length=56)
    core_genes_present = models.CharField(max_length=128)  # Also might have to be changed.
    ecoli_serotype = models.CharField(max_length=128)
    sistr_serovar_antigen = models.CharField(max_length=512)
    sistr_serovar_cgmlst = models.CharField(max_length=56)
    sistr_serovar_serogroup = models.CharField(max_length=56)
    sistr_serovar_h1 = models.CharField(max_length=56)
    sistr_serovar_h2 = models.CharField(max_length=56)
    sistr_serovar_serovar = models.CharField(max_length=56)
    geneseekr_profile = models.CharField(max_length=128)
    vtyper_profile = models.CharField(max_length=128)
    amr_profile = models.CharField(max_length=512)
    amr_resistant = models.CharField(max_length=56)
    plasmid_profile = models.CharField(max_length=128)
    total_predicted_genes = models.IntegerField()
    predicted_genes_over_3000 = models.IntegerField()
    predicted_genes_over_1000 = models.IntegerField()
    predicted_genes_over_500 = models.IntegerField()
    predicted_genes_under_500 = models.IntegerField()
    num_clusters_pf = models.IntegerField()
    percent_reads_phix = models.FloatField()
    error_rate = models.FloatField()
    length_forward_read = models.FloatField()
    length_reverse_read = models.FloatField()
    real_time_strain = models.CharField(max_length=64)
    flowcell = models.CharField(max_length=128)
    machine_name = models.CharField(max_length=64)
    pipeline_version = models.CharField(max_length=64)
    date_assembled = models.DateTimeField()


class LSTSData(models.Model):
    seqid = models.ForeignKey(Sample, on_delete=models.CASCADE, related_name='lsts_data')
    lsts_id = models.CharField(max_length=88)
    country_of_origin = models.CharField(max_length=128)
    food = models.CharField(max_length=128)

    def __str__(self):
        return self.lsts_id
