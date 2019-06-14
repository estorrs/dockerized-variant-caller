#!/bin/bash

CWL="cwl/dockerized-variant-caller.cwl"
YAML="cwl/tests/inputs.yaml"

mkdir -p cwl/tests/test_results
RABIX_ARGS="--basedir cwl/tests/test_results"

rabix $RABIX_ARGS $CWL $YAML
