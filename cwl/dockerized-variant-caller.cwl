class: CommandLineTool
cwlVersion: v1.0
$namespaces:
  sbg: 'https://www.sevenbridges.com/'
id: dockerized-variant-caller
baseCommand:
  - python
  - /dockerized-variant-caller/dockerized-variant-caller/dockerized-variant-caller.py
inputs:
  - id: threads
    type: int?
    inputBinding:
      position: 0
      prefix: '--threads'
  - id: filter_variants
    type: boolean?
    inputBinding:
      position: 0
      prefix: '--filter-variants'
  - id: reference_fasta
    type: File
    inputBinding:
      position: 0
      prefix: '--reference-fasta'
  - id: input_bam
    type: File
    inputBinding:
      position: 99
outputs:
  - id: output_vcf
    type: File?
    outputBinding:
      glob: output.vcf
label: dockerized-variant-caller
arguments:
  - position: 0
    prefix: '--output-vcf'
    valueFrom: output.vcf
requirements:
  - class: DockerRequirement
    dockerPull: 'estorrs/dockerized-variant-caller:0.0.1'
