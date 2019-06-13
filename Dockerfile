FROM python:3.6

RUN apt-get update && apt-get install -y \
    vim \
    unzip

# set up miniconda
RUN wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh -O ~/miniconda.sh \
    && bash ~/miniconda.sh -b -p ./miniconda
ENV PATH="/miniconda/bin:$PATH"

# add channels
RUN conda config --add channels defaults \
    && conda config --add channels bioconda \
    && conda config --add channels conda-forge

# install necessary tools available through conda
RUN conda install -y picard samtools pytest

# install gatk
RUN wget https://github.com/broadinstitute/gatk/releases/download/4.0.12.0/gatk-4.0.12.0.zip \
    && unzip gatk-4.0.12.0.zip

# add gatk to path
ENV PATH="$PATH:/gatk-4.0.12.0/"

# make sure we have java 8. GATK needs java 8
RUN conda install -y -c cyclus java-jdk

# copy over our directory
COPY . /dockerized-variant-caller
WORKDIR /dockerized-variant-caller

CMD /bin/bash
