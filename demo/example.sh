#!/bin/bash

INPUT_REFERENCE_FASTA=$PWD/tests/data/synthetic/synthetic.fa
INPUT_BAM=$PWD/tests/data/synthetic/synthetic.bam
OUTPUT_DIR=$PWD/tests/outputs

mkdir -p OUTPUT_DIR

docker run -v $INPUT_REFERENCE_FASTA:/data/synthetic.fa -v $INPUT_BAM:/data/synthetic.bam -v $OUTPUT_DIR:/data/outputs dockerized-variant-caller python dockerized-variant-caller/dockerized-variant-caller.py --reference-fasta /data/synthetic.fa --output-vcf /data/outputs/output.vcf /data/synthetic.bam
