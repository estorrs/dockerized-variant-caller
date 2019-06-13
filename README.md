# dockerized-variant-caller
An example repository structure of a dockerized tool.

## To build docker image

Navigate to the root of the repository and run
```bash
$: docker build -t dockerized-variant-caller .
```

To build a container with a specific tag
```bash
$: docker build -t dockerized-variant-caller:<tag> .
```

To run docker image in an interactive terminal
```bash
$: docker run -it dockerized-variant-caller /bin/bash
```

To push to a container registry (i.e. dockerhub)

note: you will need to have an active account at a container registry (such as dockerhub)
    - you may also need to run `docker login` to connect to your account from the server you are on
```bash
$: docker build -t <user>:dockerized-variant-caller:<tag> .
$: docker push <user>/dockerized-variant-caller:<tag>
```

## Running the docker image
Running on a fake dataset
```bash
$: docker run -it -v dockerized-variant-caller /bin/bash
$: python dockerized-variant-caller/dockerized-variant-caller.py --reference-fasta tests/data/synthetic/synthetic.fa --output-vcf output.vcf tests/data/synthetic/synthetic.bam
```

Running with mapped inputs
Since Docker cannot see outside file system. To run this tool on real data you need to mount volumes to the container.
```bash
$: docker run -it -v /system/path/to/bam:/container/path/to/bam -v /system/path/to/reference:/container/path/to/reference -v /system/path/to/output/directory:/container/path/to/output/directory dockerized-variant-caller /bin/bash
$: python dockerized-variant-caller/dockerized-variant-caller.py --reference-fasta /container/path/to/reference --output-vcf /container/path/to/output/directory/output.vcf /container/path/to/bam
```


## Testing

To run basic tests in one liner
```bash
$: docker run dockerized-variant-caller pytest tests/test_synthetic.py -vv
```

To run basic tests inside an interactive terminal
```bash
$: docker run -it dockerized-variant-caller /bin/bash
$: pytest tests/test_sythetic.py -vv
```

Run more realistic test case that requires mapping a reference fasta
```bash
$: docker run -it -v /path/to/reference/fasta:/data/hs37d5.fa dockerized-variant-caller pytest tests/test_real.py
```

To run cwl pipeline on synthetic test data
Must be on a machine that has rabbix executor installed.
Must run this command from repository root
```bash
$: bash cwl/tests/run_test.sh
```

