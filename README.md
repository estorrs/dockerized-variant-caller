# dockerized-variant-caller
An example skeleton of a dockerized tool.

## To build docker image

Navigate to the root of the repository and run
```bash
docker build -t dockerized-variant-caller .
```

To build a container with a specific tag
```bash
docker build -t dockerized-variant-caller:<tag> .
```

To run docker image in an interactive terminal
```bash
docker run -it dockerized-variant-caller /bin/bash
```

To push to a container registry (i.e. dockerhub)

note: you will need to have an active account at a container registry (such as dockerhub)
    - you may also need to run `docker login` to connect to your account from the server you are on
```bash
docker build -t <user>:dockerized-variant-caller:<tag> .
docker push <user>/dockerized-variant-caller:<tag>
```

To pull container from registry
```bash
docker pull <user>/dockerized-variant-caller:<tag>
```

## Running the tool from inside docker container
Running on a fake dataset
```bash
docker run -it dockerized-variant-caller /bin/bash
python dockerized-variant-caller/dockerized-variant-caller.py --reference-fasta tests/data/synthetic/synthetic.fa --output-vcf output.vcf tests/data/synthetic/synthetic.bam
```

Running with mapped inputs.
Since Docker cannot see outside file system. To run this tool on real data you need to mount volumes to the container.
```bash
docker run -it -v /absolute/path/to/bam:/container/path/to/bam -v /absolue/path/to/reference:/container/path/to/reference -v /absolute/path/to/output/directory:/container/path/to/output/directory dockerized-variant-caller /bin/bash
python dockerized-variant-caller/dockerized-variant-caller.py --reference-fasta /container/path/to/reference --output-vcf /container/path/to/output/directory/output.vcf /container/path/to/bam
```

## Directly running the tool from a script
```bash
bash demo/example.sh
```

## Running the tool as a CWL tool
To run cwl pipeline on synthetic test data
Must be on a machine that has rabbix executor installed. Can be easily adapted to another executor, such as Cromwell, if desired.
```bash
bash cwl/tests/run_test.sh
```

## Testing

To run basic tests in one liner
```bash
docker run dockerized-variant-caller pytest tests/test_synthetic.py -vv
```

To run basic tests inside an interactive terminal
```bash
docker run -it dockerized-variant-caller /bin/bash
pytest tests/test_synthetic.py -vv
```

Run more realistic test case that requires mapping a reference fasta.
Assumes you're on denali or katmai. But you can run from anywhere. Just change the reference filepath.
Reference used is at ftp://ftp.1000genomes.ebi.ac.uk/vol1/ftp/technical/reference/phase2_reference_assembly_sequence/hs37d5.fa.gz
```bash
docker run -v /diskmnt/Projects/Users/estorrs/data/1000-genomes/hs37d5.fa:/data/hs37d5.fa dockerized-variant-caller pytest tests/test_real.py -vv
```

