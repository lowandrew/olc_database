from django.core.management.base import BaseCommand
from data_wrapper.models import SeqData, ResFinderData, OLN, LSTSData
import os
import csv
import pandas as pd
import re


def read_combined_metadata(data_folder):
    with open(os.path.join(data_folder, 'combinedMetadata.csv')) as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            # Sometimes people forget about the InterOp folder. Without that, phix and error rate can't be calculated.
            # If that happens, set those values to -1
            if row['PercentReadsPhiX'] == 'ND' or row['PercentReadsPhiX'] == '-':
                phix = -1.0
            else:
                phix = row['PercentReadsPhiX']
            if row['ErrorRate'] == 'ND' or row['ErrorRate'] == '-':
                error_rate = -1.0
            else:
                error_rate = row['ErrorRate']
            # Now go through and add metadata from the combinedMetadata to our SeqData
            # Figure out if Sample has OLN number, LSTS number or something else entirely.
            if row['SampleName'].startswith('OLC') or row['SampleName'].startswith('OLN') or row['SampleName'].startswith('OLF'):
                # Check if OLN entry exists, create if it doesn't.
                try:
                    OLN.objects.get(oln_id=row['SampleName'])
                except:
                    OLN.objects.create(oln_id=row['SampleName'])
                SeqData.objects.update_or_create(seqid=row['SeqID'],
                                                 genus=row['Genus'],
                                                 oln_id=OLN.objects.get(oln_id=row['SampleName']),
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
                                                 percent_reads_phix=phix,
                                                 error_rate=error_rate,
                                                 length_forward_read=row['LengthForwardRead'],
                                                 length_reverse_read=row['LengthReverseRead'],
                                                 real_time_strain=row['RealTimeStrain'],
                                                 flowcell=row['Flowcell'],
                                                 machine_name=row['MachineName'],
                                                 pipeline_version=row['PipelineVersion'],
                                                 date_assembled=row['AssemblyDate']
                                                 )
            # Add to LSTS Data if we get a regex match on SampleName
            elif re.match('[A-Z]{3,}-[A-Z]+-\d{4}-[A-Z]+-\d{4,5}', row['SampleName']):
                try:
                    LSTSData.objects.get(lsts_id=row['SampleName'])
                except:
                    LSTSData.objects.create(lsts_id=row['SampleName'])
                SeqData.objects.update_or_create(seqid=row['SeqID'],
                                                 genus=row['Genus'],
                                                 lsts_id=LSTSData.objects.get(lsts_id=row['SampleName']),
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
                                                 percent_reads_phix=phix,
                                                 error_rate=error_rate,
                                                 length_forward_read=row['LengthForwardRead'],
                                                 length_reverse_read=row['LengthReverseRead'],
                                                 real_time_strain=row['RealTimeStrain'],
                                                 flowcell=row['Flowcell'],
                                                 machine_name=row['MachineName'],
                                                 pipeline_version=row['PipelineVersion'],
                                                 date_assembled=row['AssemblyDate']
                                                 )
            else:
                SeqData.objects.update_or_create(seqid=row['SeqID'],
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
                                                 percent_reads_phix=phix,
                                                 error_rate=error_rate,
                                                 length_forward_read=row['LengthForwardRead'],
                                                 length_reverse_read=row['LengthReverseRead'],
                                                 real_time_strain=row['RealTimeStrain'],
                                                 flowcell=row['Flowcell'],
                                                 machine_name=row['MachineName'],
                                                 pipeline_version=row['PipelineVersion'],
                                                 date_assembled=row['AssemblyDate']
                                                 )


def read_resfinder(data_folder):
    df = pd.read_excel(os.path.join(data_folder, 'resfinder_assembled.xlsx'))
    for i in df.index:
        if pd.isnull(df.loc[i]['Strain']):
            continue
        # Add SeqData to database if it doesn't already exist for some
        try:
            SeqData.objects.get(seqid=df['Strain'][i])
        except:
            SeqData.objects.create(seqid=df['Strain'][i])
        # Now add data, yay.
        try:
            float(df['aa_Identity'][i])
        except:
            df['aa_Identity'][i] = 100.0
        ResFinderData.objects.update_or_create(seqid=SeqData.objects.get(seqid=df['Strain'][i]),
                                               resfinder_gene=df['Gene'][i],
                                               resfinder_allele=df['Allele'][i],
                                               resfinder_resistance=df['Resistance'][i],
                                               resfinder_percent_identity=df['PercentIdentity'][i],
                                               resfinder_percent_covered=df['PercentCovered'][i],
                                               resfinder_contig=df['Contig'][i],
                                               resfinder_location=df['Location'][i],
                                               resfinder_sequence=df['nt_sequence'][i],
                                               resfinder_aa_identity=df['aa_Identity'][i]
                                               )

# TODO: probably change to using PANDAS at some point
class Command(BaseCommand):
    help = 'Command to add data to the OLC Database Portal'

    def add_arguments(self, parser):
        parser.add_argument('datapath',
                            type=str,
                            help='Path to reports folder generated by pipeline2.0')

    def handle(self, *args, **options):
        read_combined_metadata(data_folder=options['datapath'])
        read_resfinder(data_folder=options['datapath'])
