from django.core.management.base import BaseCommand
from data_wrapper.models import Sample, SeqData
import csv

# TODO: probably change to using PANDAS at some point

class Command(BaseCommand):
    help = 'Command to add data to the OLC Database Portal'

    def add_arguments(self, parser):
        parser.add_argument('datapath',
                            type=str,
                            help='Path to CSV file to use to add to the database.')

    def handle(self, *args, **options):
        with open(options['datapath']) as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                # If sample does not exist in database, add it to DB.
                try:
                    Sample.objects.get(seqid=row['SeqID'])
                except:
                    Sample.objects.create(seqid=row['SeqID'])
                # Now go through and add metadata from the combinedMetadata to our SeqData
                SeqData.objects.update_or_create(seqid=Sample.objects.get(seqid=row['SeqID']),
                                                 genus=row['Genus'],
                                                 n50=row['N50'],
                                                 num_contigs=row['NumContigs'],
                                                 rmlst=row['rMLST_Result'],
                                                 sequencing_date=row['SequencingDate'],
                                                 analyst=row['Analyst'],
                                                 sample_purity=row['SamplePurity'],
                                                 assembly_quality=row['AssemblyQuality'],
                                                 total_length=row['TotalLength'],
                                                 mean_insert_size=row['MeanInsertSize'],
                                                 insert_size_std=row['InsertSizeSTD'],
                                                 average_coverage_depth=row['AverageCoverageDepth'],
                                                 coverage_depth_std=row['CoverageDepthSTD'],
                                                 percent_gc=row['PercentGC'],
                                                 mash_reference_genome=row['MASH_ReferenceGenome'],
                                                 mash_num_matching_hashes=row['MASH_NumMatchingHashes'],
                                                 sixteens_result=row['16S_result'],
                                                 mlst=row['MLST_Result'],
                                                 mlst_allele_1=row['MLST_gene_1_allele'],
                                                 mlst_allele_2=row['MLST_gene_2_allele'],
                                                 mlst_allele_3=row['MLST_gene_3_allele'],
                                                 mlst_allele_4=row['MLST_gene_4_allele'],
                                                 mlst_allele_5=row['MLST_gene_5_allele'],
                                                 mlst_allele_6=row['MLST_gene_6_allele'],
                                                 mlst_allele_7=row['MLST_gene_7_allele'],
                                                 core_genes_present=row['CoreGenesPresent'],
                                                 ecoli_serotype=row['E_coli_Serotype'],
                                                 sistr_serovar_antigen=row['SISTR_serovar_antigen'],
                                                 sistr_serovar_cgmlst=row['SISTR_serovar_cgMLST'],
                                                 sistr_serovar_h1=row['SISTR_h1'],
                                                 sistr_serovar_h2=row['SISTR_h2'],
                                                 sistr_serovar_serovar=row['SISTR_serovar'],
                                                 geneseekr_profile=row['GeneSeekr_Profile'],
                                                 vtyper_profile=row['Vtyper_Profile'],
                                                 amr_profile=row['AMR_Profile'],
                                                 amr_resistant=row['AMR Resistant/Sensitive'],
                                                 plasmid_profile=row['PlasmidProfile'],
                                                 total_predicted_genes=row['TotalPredictedGenes'],
                                                 predicted_genes_over_3000=row['PredictedGenesOver3000bp'],
                                                 predicted_genes_over_1000=row['PredictedGenesOver1000bp'],
                                                 predicted_genes_over_500=row['PredictedGenesOver500bp'],
                                                 predicted_genes_under_500=row['PredictedGenesUnder500bp'],
                                                 num_clusters_pf=row['NumClustersPF'],
                                                 percent_reads_phix=row['PercentReadsPhiX'],
                                                 error_rate=row['ErrorRate'],
                                                 length_forward_read=row['LengthForwardRead'],
                                                 length_reverse_read=row['LengthReverseRead'],
                                                 real_time_strain=row['RealTimeStrain'],
                                                 flowcell=row['Flowcell'],
                                                 machine_name=row['MachineName'],
                                                 pipeline_version=row['PipelineVersion'],
                                                 date_assembled=row['AssemblyDate']
                                                 )
        print('Things will eventually be done here.')
