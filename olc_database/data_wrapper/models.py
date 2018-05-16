from django.db import models
from olc_database.users.models import User
from django.contrib.postgres.fields import ArrayField
from simple_history.models import HistoricalRecords


# Create your models here.

class SeqIdList(models.Model):
    seqid_list = ArrayField(models.CharField(max_length=256, null=True, blank=True))


class OlnIdList(models.Model):
    olnid_list = ArrayField(models.CharField(max_length=256, null=True, blank=True))


class LstsIdList(models.Model):
    lstsid_list = ArrayField(models.CharField(max_length=256, null=True, blank=True))


# Both this and SavedTables are probably good to stay
class SavedQueries(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    search_terms = ArrayField(models.CharField(max_length=48))
    search_attributes = ArrayField(models.CharField(max_length=48))
    search_operations = ArrayField(models.CharField(max_length=48))
    search_combine_operations = ArrayField(models.CharField(max_length=48))
    query_name = models.CharField(max_length=256, null=True, blank=True)

    def __str__(self):
        return self.query_name


class SavedTables(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    table_attributes = ArrayField(models.CharField(max_length=128, null=True, blank=True))
    table_name = models.CharField(max_length=256, null=True, blank=True)

    def __str__(self):
        return self.table_name


# This is pretty much a placeholder model - to be updated once imports of data from LSTS get wholly figured out.
class LSTSData(models.Model):
    lsts_id = models.CharField(max_length=88)
    country_of_origin = models.CharField(max_length=128, null=True, blank=True)
    food = models.CharField(max_length=128, null=True, blank=True)
    history = HistoricalRecords()

    def __str__(self):
        return self.lsts_id


class OLN(models.Model):
    oln_id = models.CharField(max_length=64, null=True, blank=True)
    lsts_id = models.ForeignKey(LSTSData, on_delete=models.CASCADE, null=True)
    extra_lsts_data = models.CharField(max_length=64, null=True, blank=True)
    other_id = models.CharField(max_length=64, null=True, blank=True)
    oln_genus = models.CharField(max_length=64, null=True, blank=True,
                                 help_text='Genus!')
    oln_species = models.CharField(max_length=64, null=True, blank=True)
    oln_subspecies = models.CharField(max_length=64, null=True, blank=True)
    oln_serotype = models.CharField(max_length=64, null=True, blank=True)
    oln_verotoxin = models.CharField(max_length=64, null=True, blank=True)
    oln_source = models.CharField(max_length=64, null=True, blank=True)
    oneenzyme = models.CharField(max_length=64, null=True, blank=True)
    twoenzyme = models.CharField(max_length=64, null=True, blank=True)

    history = HistoricalRecords()

    def __str__(self):
        return self.oln_id


class SeqData(models.Model):
    seqid = models.CharField(max_length=64, null=True, blank=True)
    lsts_id = models.ForeignKey(LSTSData, on_delete=models.CASCADE, null=True)
    oln_id = models.ForeignKey(OLN, on_delete=models.CASCADE, null=True)
    genus = models.CharField(max_length=128, null=True, blank=True)
    n50 = models.IntegerField(null=True, blank=True)
    num_contigs = models.IntegerField(null=True, blank=True)
    rmlst = models.CharField(max_length=56, null=True, blank=True)
    sequencing_date = models.DateField(null=True, blank=True)
    analyst = models.CharField(max_length=128, null=True, blank=True)
    sample_purity = models.CharField(max_length=64, null=True, blank=True)
    assembly_quality = models.CharField(max_length=64, null=True, blank=True)
    total_length = models.IntegerField(null=True, blank=True)
    mean_insert_size = models.FloatField(null=True, blank=True)
    insert_size_std = models.FloatField(null=True, blank=True)
    average_coverage_depth = models.FloatField(null=True, blank=True)
    coverage_depth_std = models.FloatField(null=True, blank=True)
    percent_gc = models.FloatField(null=True, blank=True)
    mash_reference_genome = models.CharField(max_length=256, null=True, blank=True)
    mash_num_matching_hashes = models.CharField(max_length=128, null=True, blank=True)  # This will maybe need to be changed to non-char.
    sixteens_result = models.CharField(max_length=256, null=True, blank=True)
    mlst = models.CharField(max_length=56, null=True, blank=True)
    mlst_allele_1 = models.CharField(max_length=56, null=True, blank=True)
    mlst_allele_2 = models.CharField(max_length=56, null=True, blank=True)
    mlst_allele_3 = models.CharField(max_length=56, null=True, blank=True)
    mlst_allele_4 = models.CharField(max_length=56, null=True, blank=True)
    mlst_allele_5 = models.CharField(max_length=56, null=True, blank=True)
    mlst_allele_6 = models.CharField(max_length=56, null=True, blank=True)
    mlst_allele_7 = models.CharField(max_length=56, null=True, blank=True)
    core_genes_present = models.CharField(max_length=128, null=True, blank=True)  # Also might have to be changed to non-char.
    ecoli_serotype = models.CharField(max_length=128, null=True, blank=True)
    sistr_serovar_antigen = models.CharField(max_length=512, null=True, blank=True)
    sistr_serovar_cgmlst = models.CharField(max_length=56, null=True, blank=True)
    sistr_serovar_serogroup = models.CharField(max_length=56, null=True, blank=True)
    sistr_serovar_h1 = models.CharField(max_length=56, null=True, blank=True)
    sistr_serovar_h2 = models.CharField(max_length=56, null=True, blank=True)
    sistr_serovar_serovar = models.CharField(max_length=56, null=True, blank=True)
    geneseekr_profile = models.CharField(max_length=128, null=True, blank=True)
    vtyper_profile = models.CharField(max_length=128, null=True, blank=True)
    amr_profile = models.CharField(max_length=512, null=True, blank=True)
    amr_resistant = models.CharField(max_length=56, null=True, blank=True)
    plasmid_profile = models.CharField(max_length=128, null=True, blank=True)
    total_predicted_genes = models.IntegerField(null=True, blank=True)
    predicted_genes_over_3000 = models.IntegerField(null=True, blank=True)
    predicted_genes_over_1000 = models.IntegerField(null=True, blank=True)
    predicted_genes_over_500 = models.IntegerField(null=True, blank=True)
    predicted_genes_under_500 = models.IntegerField(null=True, blank=True)
    num_clusters_pf = models.IntegerField(null=True, blank=True)
    percent_reads_phix = models.FloatField(null=True, blank=True)
    error_rate = models.FloatField(null=True, blank=True)
    length_forward_read = models.FloatField(null=True, blank=True)
    length_reverse_read = models.FloatField(null=True, blank=True)
    real_time_strain = models.CharField(max_length=64, null=True, blank=True)
    flowcell = models.CharField(max_length=128, null=True, blank=True)
    machine_name = models.CharField(max_length=64, null=True, blank=True)
    pipeline_version = models.CharField(max_length=64, null=True, blank=True)
    date_assembled = models.DateField(null=True, blank=True)
    history = HistoricalRecords()

    def __str__(self):
        return self.seqid


class SeqTracking(models.Model):
    seqid = models.OneToOneField(SeqData, on_delete=models.CASCADE, null=True)  # Allow null as we SeqTracking should be
    # happening before we actually receive SeqDataCharField
    lsts_id = models.ForeignKey(LSTSData, on_delete=models.CASCADE, null=True)
    oln_id = models.ForeignKey(OLN, on_delete=models.CASCADE, null=True)
    priority = models.CharField(max_length=128, null=True, blank=True)
    curator_flag = models.CharField(max_length=128, null=True, blank=True)
    comment = models.CharField(max_length=512, null=True, blank=True)
    history = HistoricalRecords()

    def __str__(self):
        return self.seqid.seqid


class ResFinderData(models.Model):
    # Can have multiple resfinders to one SEQID, so this does have to be ForeignKey, not OneToOne
    seqid = models.ForeignKey(SeqData, on_delete=models.CASCADE, related_name='resfinder_data')
    resfinder_gene = models.CharField(max_length=56, null=True, blank=True)
    resfinder_allele = models.IntegerField(null=True, blank=True)
    resfinder_resistance = models.CharField(max_length=64, null=True, blank=True)
    resfinder_percent_identity = models.FloatField(null=True, blank=True)
    resfinder_percent_covered = models.FloatField(null=True, blank=True)
    resfinder_contig = models.CharField(max_length=128, null=True, blank=True)
    resfinder_location = models.CharField(max_length=64, null=True, blank=True)
    resfinder_sequence = models.CharField(max_length=8192, null=True, blank=True)
    resfinder_aa_identity = models.CharField(max_length=64, null=True, blank=True)  # This is a dash sometimes, so can't have as FloatField :(

    history = HistoricalRecords()

    def __str__(self):
        return self.seqid.seqid


class CultureData(models.Model):
    active_choices = (
        ('YES', 'YES'),
        ('NO', 'NO')
    )
    # Should we allow null values for oln_id - I'm going to say no: forms will create empty OLN models as necessary,
    # as CultureData should always have an oln_id
    oln_id = models.ForeignKey(OLN, on_delete=models.CASCADE)
    received_date = models.DateField(null=True, blank=True)
    gdna_extraction_date = models.DateField(null=True, blank=True)
    gdna_extraction_method = models.CharField(max_length=64, null=True, blank=True)
    gdna_extracted_by = models.CharField(max_length=64, null=True, blank=True)
    quantification_date = models.DateField(null=True, blank=True)
    quantification_method = models.CharField(max_length=64, null=True, blank=True)
    quantified_by = models.CharField(max_length=64, null=True, blank=True)
    concentration = models.FloatField(null=True, blank=True)
    discard_date = models.DateField(null=True, blank=True)
    is_active = models.CharField(max_length=8,
                                 choices=active_choices,
                                 default='NO')

    history = HistoricalRecords()

    def __str__(self):
        return self.oln_id.oln_id
