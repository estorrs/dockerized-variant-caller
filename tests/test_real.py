import subprocess

import pytest

# requires hg37 reference to be mapped to /data/hs37d5.fa
# can download from ftp://ftp.1000genomes.ebi.ac.uk/vol1/ftp/technical/reference/phase2_reference_assembly_sequence/hs37d5.fa.gz

REFERENCE_FASTA = '/data/hs37d5.fa'
TEST_BAM = 'tests/data/real/test.bam'

def test_haplotype_caller():
    tool_args = ['python', 'dockerized-variant-caller/dockerized-variant-caller.py',
            '--reference-fasta', REFERENCE_FASTA,
            '--output-vcf', 'tests/data/output.vcf',
            TEST_BAM]
    
    results = subprocess.check_output(tool_args).decode('utf-8')

    # insert some kind of condition here
    assert True

def test_call_with_variant_filter():
    tool_args = ['python', 'dockerized-variant-caller/dockerized-variant-caller.py',
            '--reference-fasta', REFERENCE_FASTA,
            '--output-vcf', 'tests/data/output.vcf',
            '--filter-variants',
            TEST_BAM]
    
    results = subprocess.check_output(tool_args).decode('utf-8')

    # insert some kind of condition here
    assert True
