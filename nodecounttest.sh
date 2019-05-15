#!/bin/bash

# full path to the ns3 directory
ns3_path="/home/mikkel/ns3workspace/ns-3-allinone/ns-3-dev"

# Runs per configuration
runs=10
# Protocols to run tests on
protocol="olsr"

# For testing different node counts
max_nodes=50
min_nodes=10
node_step=10

cd "$ns3_path"
pwd

# Run a build before multithreading the tests

./waf

datetime=`date '+%Y-%m-%d %H:%M:%S'`

for (( nodes=$min_nodes; nodes<=$max_nodes; nodes+=$node_step)); do
    for (( run=0; run<$runs; run++ )); do
        echo "Starting $protocol-$run-$nodes-n test"
        mkdir -p "./runs/$protocol/n$nodes/run$run"
        ./waf --cwd="./runs/$protocol/run$run" --run "mainp6 --runNumber=$run --numNodes=$nodes" &
    done
done
     
