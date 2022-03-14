#!/usr/bin/env bash

MONTH=$1 # eg 2020-02
FORMAT="${2:-json}"
THIS_DIR=$(dirname $(readlink -f ${BASH_SOURCE[0]}))

CACHE_ISDCT=${CACHE_ISDCT:-"${THIS_DIR}/anonymize_isdct.py"}
DATA_DIR=${DATA_DIR:-""}
if [ -z "$DATA_DIR"]; then
    source "${THIS_DIR}/settings.sh" # defines DATA_DIR
fi

set -e

if [ -z "$MONTH" ]; then
    echo "Syntax: $(basename $0) YYYY-MM" >&2
    exit 1
fi

for inputf in $(find ${DATA_DIR}/${MONTH}-* -name Intel\*.tgz)
do
    # inputf = /global/homes/g/glock/h5lmt/2020-02-25/Intel_DCT_20200225.tgz
    bn=$(basename "$inputf" .tgz)
    if [ $FORMAT == "json" ]; then
        $CACHE_ISDCT -j "$inputf" -o "${bn}.json" && gzip -9 "${bn}.json"
    else
        $CACHE_ISDCT -c "$inputf" -o "${bn}.csv" && gzip -9 "${bn}.csv"
    fi
done
