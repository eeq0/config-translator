#!/bin/sh
cd "$(dirname "$0")/.." || exit 1

for config in examples/*.conf examples/errors/*.conf; do
    echo "=== $config"
    sh run.sh --input "$config"
    echo "код возврата: $?"
    echo
done
