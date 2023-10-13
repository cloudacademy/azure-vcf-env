#!/usr/bin/env bash
set -e

# Trim Azure mgmt packages included api versions
keep_api_versions=1
mgmt_client_dir=venv/lib/python*/site-packages/azure/mgmt
skip_clients=( "eventhub" "monitor" "keyvault") # skip clients requiring more than latest version of the API
for client_dir in $mgmt_client_dir/*; do
    if [[ " ${skip_clients[*]} " =~ " $(basename ${client_dir}) " ]]; then
        echo "skipping pruning $client_dir"
        continue
    fi
    old_IFS=$IFS; IFS=$'\n'
    api_dirs=($(find $client_dir -maxdepth 1 -type d -regex "$client_dir/v[0-9][0-9][0-9][0-9].*" | sort))
    unset IFS; IFS=$old_IFS
    if [[ ${#api_dirs[@]} -le $keep_api_versions ]]; then
        continue
    fi
    for i in $(seq 0 1 $(( ${#api_dirs[@]} - $(( $keep_api_versions + 1 )) )) ); do
        rm -rf ${api_dirs[i]}
    done
done