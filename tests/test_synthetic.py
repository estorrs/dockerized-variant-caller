import subprocess

import pytest

REFERENCE_FASTA = 'tests/data/synthetic/synthetic.fa'
TEST_BAM = 'tests/data/synthetic/synthetic.bam'

def test_haplotype_caller():
    tool_args = ['python', 'dockerized-variant-caller/dockerized-variant-caller.py',
            '--reference-fasta', REFERENCE_FASTA,
            '--output-vcf', 'tests/data/output.vcf',
            TEST_BAM]
    
    results = subprocess.check_output(tool_args).decode('utf-8')

    # just make sure we get here
    assert True

def test_call_with_variant_filter():
    tool_args = ['python', 'dockerized-variant-caller/dockerized-variant-caller.py',
            '--reference-fasta', REFERENCE_FASTA,
            '--output-vcf', 'tests/data/output.vcf',
            '--filter-variants',
            TEST_BAM]
    
    results = subprocess.check_output(tool_args).decode('utf-8')

    # just make sure we get here
    assert True
