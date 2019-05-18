#!/usr/bin/env python3

import pcapy
import os

# Definer fil listen som vil indeholde alle Pcap filer
File_list = []


def main():

    # Vi finder alle Pcap filer i den folder vi er i
    for file in os.listdir("pcaps/"):
        if file.endswith(".pcap"):
            File_list.append(os.path.abspath(os.path.join("pcaps/", file)))

    overhead_sum = 0
    # Vi kan nu finde alt data sendt som set i pcap filen
    for file in File_list:
        # Vi laeser fra vores oenskede pcap fil
        reader = pcapy.open_offline(file)

        # Vi finder hvor mange frames der er i pcap filen
        Lenght = os.popen('tshark -r {} | wc -l'.format(file)).read()
        test = Lenght[0] + Lenght[1] + Lenght[2]
        PcapLenght = int(test)
        # print(PcapLenght)


        try:
            # Vi koerer igennem alle pakker/frames og finder deres laengder
            for x in range(0, PcapLenght-1):
                (header, payload) = reader.next()
                # print(header.getlen());
                # Summer alle frames laengder

                if header is not None:
                    overhead_sum = overhead_sum + header.getlen()

        except pcapy.PcapError:
            # print("FEJL")
            print(overhead_sum)
            break

    print(overhead_sum)



main()
