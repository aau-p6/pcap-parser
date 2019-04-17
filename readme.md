#PCAP parsing for ns trace files
This repo holds scripts for parsing the pcap output files of our ns3 sims

## Requirements

It is recommended to use this in a virtual environment if you want to contribute.

```bash
sudo dnf install libpcap-devel # fedora
sudo apt install libpcap-dev # Ubuntu

```

to install python requirements run:
```bash
pip install -r requirements.txt
```

## Usage

put the pcap files in the pcaps folder and run the relevant script