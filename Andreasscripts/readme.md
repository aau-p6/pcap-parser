I toppen af ns3 folderen skal der laves en ny mappe kaldet Results så som dette<br/> /home/user/workspace/ns3/ns-3-dev/Results<br/>
I denne mappe skal der laves 4 nye mapper kaldet AODV DSR DSDV OLSR så at vi altså blandt andet har denne sti <br/> /home/user/workspace/ns3/ns-3-dev/Results/OLSR<br/>

automatic.py gemmes i top folderen altså i /home/user/workspace/ns3/ns-3-dev<br/>
automatic.py spytter også en masse fejlbekseder ud omkring broken pipe. Fejlen forsøger jeg at fikse, men jeg har ikke givet den det største fokus, da scriptet stadig virker.<br/>
nyOverhead.py og statistic.py gemmes i /home/user/workspace/ns3/ns-3-dev/Results<br/>

For at køre simulationer automatisk så kør automatic.py, men ændr i de ting der står i den. i nuet er den sat op til at køre 10 tests hvor node count inkrementeres med 5 for hver gang den køres, og så køres der 20 af disse tests for at skabe noget statistik over testen.<br/>

For hive information ud af en simulation så kør nyOverhead.py det er værd at nævne at den godt kan være langsom hvis man har kørt mange tests igennem. Denne vil gemme i fil kaldet collected_data i hver af test mapperne 
/home/user/workspace/ns3/ns-3-dev/Results/OLSR/OLSR5<br/>

Overheadthreading.py er en "ny" version som kører det i tråde for at reducere tiden markant. Maks antal tilladte tråde kan findes i toppen af scriptet, som kan ændres som man ønsker.

statistic.py har brug for at nyOverhead.py er kørt igennem først<br/>
For videre at hive data ud så som gennemsnitlig droprate, end to end delay og overhead så kør statistic.py denne vil gemmes i test typer mappen hvilket vil sige  /home/user/workspace/ns3/ns-3-dev/Results/OLSR under navnet statistic_data.txt
Denne fil indeholder de tidligere nævnte værdier lige så vel som variationen og worst case værdien.<br/>

Derudover så bliver confidence intervallet for de forskelliger værdier præsenteret med 2 decimaler, Overhead præsenteres som i bytes i tusinde, End to end delay præsenteres i millisekunder og Droprate præsenteres i procent.<br/>

bitchboi.cc er bare scriptet der laver simulationen så den skal gemmes i /scratch
