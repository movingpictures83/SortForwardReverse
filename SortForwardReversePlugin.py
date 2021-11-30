import sys
import PyPluMA

class SortForwardReversePlugin:
    def input(self, filename):
        infile = open(filename, 'r')
        self.parameters = dict()
        for line in infile:
           contents = line.strip().split('\t')
           self.parameters[contents[0]] = contents[1]

        forwardPrefix = PyPluMA.prefix() + "/" + self.parameters["forwardPrefix"]
        reversePrefix = PyPluMA.prefix() + "/" + self.parameters["reversePrefix"]
        #forwardPrefix = sys.argv[1]
        #reversePrefix = sys.argv[2]

        forwardFASTA = open(forwardPrefix + ".fasta", 'r')
        forwardQUAL = open(forwardPrefix + ".qual", 'r')
        reverseFASTA = open(reversePrefix + ".fasta", 'r')
        reverseQUAL = open(reversePrefix + ".qual", 'r')
        self.seqids = list()


        # Read first file
        # Store sequence names
        # Sort
        # Use this same order for the rest

        self.fF = dict()
        self.fQ = dict()
        self.rF = dict()
        self.rQ = dict()

        pos = 0
        for line in forwardFASTA:
           line = line.strip()
           if (pos % 2 == 0):
              seqid = line.strip().split('\t')[0]
              self.seqids.append(seqid)
           else:
              self.fF[seqid] = line
           pos += 1

        self.seqids.sort()

        pos = 0
        for line in forwardQUAL:
            line = line.strip()
            if (pos % 2 == 0):
               contents = line.split('\t')
               seqid = contents[0]
               qual = contents[1]
            else:
               self.fQ[seqid] = (qual, line)
            pos += 1

        pos = 0
        for line in reverseFASTA:
           line = line.strip()
           if (pos % 2 == 0):
              seqid = line.strip().split('\t')[0]
           else:
              self.rF[seqid] = line
           pos += 1

        pos = 0
        for line in reverseQUAL:
            line = line.strip()
            if (pos % 2 == 0):
               contents = line.split('\t')
               seqid = contents[0]
               qual = contents[1]
            else:
               self.rQ[seqid] = (qual, line)
            pos += 1


    def run(self):
       pass

    def output(self, filename):
        sortedForwardPrefix = PyPluMA.prefix() + "/" + self.parameters["sortedForwardPrefix"]
        sortedReversePrefix = PyPluMA.prefix() + "/" + self.parameters["sortedReversePrefix"]
        sortedForwardFASTA = open(sortedForwardPrefix + ".fasta", 'w')
        sortedForwardQUAL = open(sortedForwardPrefix + ".qual", 'w')
        sortedReverseFASTA = open(sortedReversePrefix + ".fasta", 'w')
        sortedReverseQUAL = open(sortedReversePrefix + ".qual", 'w')


        for i in range(0, len(self.seqids)):
            seqid = self.seqids[i]
            # We know seqid is in fF
            # Check in rF, if so use
            if (seqid in self.rF):
             sortedForwardFASTA.write(seqid+"\n")
             sortedForwardFASTA.write(self.fF[seqid])
             sortedForwardQUAL.write(seqid+"\t"+self.fQ[seqid][0]+"\n")
             sortedForwardQUAL.write(self.fQ[seqid][1])
             sortedReverseFASTA.write(seqid+"\n")
             sortedReverseFASTA.write(self.rF[seqid])
             sortedReverseQUAL.write(seqid+"\t"+self.rQ[seqid][0]+"\n")
             sortedReverseQUAL.write(self.rQ[seqid][1])

             if (i != len(self.seqids)-1):
                sortedForwardFASTA.write("\n")
                sortedForwardQUAL.write("\n")
                sortedReverseFASTA.write("\n")
                sortedReverseQUAL.write("\n")
