import sys
import csv
from datetime import datetime
import gc
gc.disable()

def main(infile1,infile2,outfile1,outfile2,outfile3):
        ifile1 = open(infile1,'rU')
        ifile2 = open(infile2,'rU')
        ofile1 = open(outfile1,'w')#feature 1
        ofile2 = open(outfile2,'w')#feature 2
        ofile3 = open(outfile3,'w')#feature 3
        #read from batch_payment.txt to set the seed for the trusted or unverified "friend"
        firstline = ifile1.readline()
        accarray = []
        friendarray = []
        reader = csv.reader(ifile1)
        for row in reader:
                try:
                        row[0] = datetime.strptime(row[0],"%Y-%m-%d %H:%M:%S")
                        row[1] = int(row[1])
                        row[2] = int(row[2])
                        row[3] = float(row[3])
                except ValueError:
                        continue

                if row[1] in accarray:
                        friendarray[accarray.index(row[1])].append(row[2])
                        if row[2] in accarray:
                                friendarray[accarray.index(row[2])].append(row[1])
                        else:
                                accarray.append(row[2])
                                friendarray.append([])
                                friendarray[accarray.index(row[2])].append(row[1])
                else:
                        accarray.append(row[1])
                        friendarray.append([])
                        friendarray[accarray.index(row[1])].append(row[2])
                        if row[2] in accarray:
                                friendarray[accarray.index(row[2])].append(row[1])
                        else:
                                accarray.append(row[2])
                                friendarray.append([])
                                friendarray[accarray.index(row[2])].append(row[1])
        ifile1.close()
        print 'Read batch_payment'
               
        #read in stream_payment.txt
        firstline2 = ifile2.readline()
        reader2 = csv.reader(ifile2)
        for row2 in reader2:
                try:
                        row2[0] = datetime.strptime(row2[0],"%Y-%m-%d %H:%M:%S")
                        row2[1] = int(row2[1])
                        row2[2] = int(row2[2])
                        row2[3] = float(row2[3])
                except ValueError:
                        continue

                if row2[1] in accarray:
                        trusted3 = 0
                        friendarray[accarray.index(row2[1])] = list(set(friendarray[accarray.index(row2[1])]))
                        if row2[2] in friendarray[accarray.index(row2[1])]:
                                ofile1.write('trusted \n')
                                ofile2.write('trusted \n')
                                ofile3.write('trusted \n')
                        else:
                                ofile1.write('unverified \n')
                                for friend in friendarray[accarray.index(row2[1])]:
                                        friendarray[accarray.index(friend)] = list(set(friendarray[accarray.index(friend)]))
                                        if row2[2] in friendarray[accarray.index(friend)]:
                                                ofile2.write('trusted \n')
                                                ofile3.write('trusted \n')
                                                break
                                        else:
                                                for friend2 in friendarray[accarray.index(friend)]:
                                                        if row2[2] in friendarray[accarray.index(friend2)]:
                                                                ofile3.write('trusted \n')
                                                                trusted3 = 1
                                                                break
                                                        else:
                                                                for friend3 in friendarray[accarray.index(friend2)]:
                                                                        if row2[2] in friendarray[accarray.index(friend3)]:
                                                                                ofile3.write('trusted \n')
                                                                                trusted3 = 1
                                                                                break
                                                if trusted3 != 1:
                                                        ofile3.write('unverified \n')
                                                        break
                                
                                
                                                ofile2.write('unverified \n')
                                
                else:
                        ofile1.write('unverified \n')
                        ofile2.write('unverified \n')
                        ofile3.write('unverified \n')
                        
        ifile2.close()
        ofile1.close()
        ofile2.close()
        ofile3.close()
                        
main(sys.argv[1],sys.argv[2],sys.argv[3],sys.argv[4],sys.argv[5])
