import argparse
import logging
import os
import re
import subprocess

# set up logger
logging.basicConfig(format='%(asctime)s - %(message)s', level=logging.INFO)

# collect input arguments
parser = argparse.ArgumentParser()

parser.add_argument('input_bam', type=str,
        help='Filepath for .bam file to call variants on.')

parser.add_argument('--reference-fasta', type=str,
        help='Reference fasta to use for variant calling.')

parser.add_argument('--output-vcf', type=str, default='output.vcf',
        help='Filepath to store .vcf file output.')
parser.add_argument('--threads', type=int,
        default=1, help='how many processes to allow gatk to use')

# HaplotypeCaller related parameters
parser.add_argument('--confidence-threshold', type=int,
        default=20, help='Confidence threshold for gatk haplotype caller.')
parser.add_argument('--filter-variants',
        action="store_true", help='If true, will do filtering recommended by gatk to minimize \
false positives.')

args = parser.parse_args()

def check_arguments():
    """Validate input arguments"""
    if args.reference_fasta is None:
        raise ValueError('Must specify a reference fasta with --reference-fasta flag.')

def prepare_reference(reference_fp):
    """Prepares reference for gatk.
    This involves creating a .fai and .dict file
    """
    # create .fai if doesn't yet exist
    if not os.path.isfile(re.sub(r'.[^.]*$', '.fai', reference_fp)):
        logging.info('preparing reference .fai')
        tool_args = ('samtools', 'faidx', reference_fp)
        logging.info(f'executing the following command: {" ".join(tool_args)}')
        subprocess.check_output(tool_args)

    # create .dict file if doesn't yet exist
    if not os.path.isfile(re.sub(r'.[^.]*$', '.dict', reference_fp)):
        logging.info('preparing reference .dict')
        tool_args = ('picard', 'CreateSequenceDictionary',
                f'R={reference_fp}',
                'O=' + re.sub(r'.[^.]*$', '.dict', reference_fp))
        logging.info(f'executing the following command: {" ".join(tool_args)}')
        subprocess.check_output(tool_args)

def index_bam(input_bam_fp):
    "Indexes .bam file if not already present"""
    if not os.path.isfile(f'{input_bam_fp}.bai'):
        logging.info('preparing .bai index')
        tool_args = ('samtools', 'index', input_bam_fp)
    
        logging.info(f'executing the following command: {" ".join(tool_args)}')
        subprocess.check_output(tool_args)

def run_haplotype_caller(input_bam_fp, reference_fp, output_vcf_fp, confidence_threshold=20,
        threads=1):
    """
    Runs GATK HaplotypeCaller.
    Only running with one thread for now because issues were reported with -nct parameter
    """
    tool_args = ('gatk', 'HaplotypeCaller',
            '-R', reference_fp,
            '-I', input_bam_fp,
            '--dont-use-soft-clipped-bases',
            '--standard-min-confidence-threshold-for-calling', str(confidence_threshold),
            '-O', output_vcf_fp)

    logging.info('running HaplotypeCaller')
    logging.info(f'executing the following command: {" ".join(tool_args)}')
    subprocess.check_output(tool_args)

def run_variant_filtering(input_vcf_fp, reference_fp, output_vcf_fp, window=35,
        cluster=3, min_fisher_strand=30.0, max_qual_by_depth=2.0, threads=1):
    """
    Filter vcf with gatk VariantFiltration. The default parameters are recommended by GATK
    for rna-seq pipeline.
    """
    tool_args = ('gatk', 'VariantFiltration',
            '-R', reference_fp,
            '-V', input_vcf_fp,
            '-window', str(window),
            '-cluster', str(cluster),
            '--filter-name', 'FS',
            '--filter-expression', f'FS > {min_fisher_strand}',
            '--filter-name', 'QD',
            '--filter-expression', f'QD < {max_qual_by_depth}',
            '-O', output_vcf_fp)

    logging.info('Running VariantFiltration')
    logging.info(f'executing the following command: {" ".join(tool_args)}')
    subprocess.check_output(tool_args)


def main():
    check_arguments()

    # index bam
    index_bam(args.input_bam)
    # prepare reference
    prepare_reference(args.reference_fasta)

    if args.filter_variants:
        run_haplotype_caller(args.input_bam, args.reference_fasta, 'temp.vcf',
            confidence_threshold=args.confidence_threshold)
        run_variant_filtering('temp.vcf', args.reference_fasta, args.output_vcf)
        os.remove('temp.vcf')
        os.remove('temp.vcf.idx')
    else:
        run_haplotype_caller(args.input_bam, args.reference_fasta, args.output_vcf,
            confidence_threshold=args.confidence_threshold)

if __name__ == '__main__':
    main()
