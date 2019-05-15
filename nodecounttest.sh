#!/bin/bash

# full path to the ns3 directory
ns3_path="/home/jellybelly/ns-allinone-3.29/ns-3.29/"

# Runs per configuration
runs=1
# Protocols to run tests on
protocol="olsr"

# For testing different node counts
max_nodes=50
min_nodes=10
node_step=5

cd "$ns3_path"
pwd

# Run a build before multithreading the tests

./waf

datetime=`date '+%Y-%m-%d %H:%M:%S'`

for (( nodes=$min_nodes; nodes<=$max_nodes; nodes+=$node_step)); do
    for (( run=0; run<$runs; run++ )); do
        echo "Starting $protocol-$run-$nodes-n test"
        mkdir -p "./runs/$protocol/n$nodes/run$run"
        ./waf --cwd="./runs/$protocol/n$nodes/run$run" --run "mainp6 --runNumber=$run --numNodes=$nodes" &
    done
done
     
exit 0
