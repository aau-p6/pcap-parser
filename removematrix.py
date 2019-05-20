import os
def main():
    #for Protocol in Protocols:
        Protocol = "OLSR"
        for test_typer_count in os.walk("%s" % (Protocol)).next()[1]:
            if os.path.isdir('%s/%s' % (Protocol, test_typer_count )) == True:
                for statistic_test_count in os.walk("%s/%s" % ( Protocol, test_typer_count)).next()[1]: 
                    dir_navn = Protocol + "/" + test_typer_count + "/" + statistic_test_count
                    os.popen("rm -r Matrix")



main()
