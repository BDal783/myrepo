#Brendon Dal Comp 383
import os
from Bio import SeqIO

#second problem:
#downloading comparison genome
first_dataset = 'datasets download genome accession GCF_000845245.1 --include gff3,rna,cds,protein,genome,seq-report'
#running command through terminal
os.system(first_dataset)
#unzipping the downloaded file

unzip= 'unzip ncbi_dataset.zip'

#running it through the terminal
os.system(unzip)
#aligning the refrence genome
base_alignment = 'bowtie2-build ncbi_dataset/data/GCF_000845245.1/GCF_000845245.1_ViralProj14559_genomic.fna HCMV'
#running it through terminal
os.system(base_alignment)
#finding the lengths of donor 1 and 2 before alignment
first_length = 'wc -l SRR5660030_1.fastq'
second_length = 'wc -l SRR5660033_1.fastq'
#running both through terminal
os.system(first_length)
os.system(second_length)
#aligning donor 1
first_alignment = 'bowtie2 --quiet -x HCMV -1 topSRR5660030_1.fastq -2 topSRR5660030_2.fastq -S mapped_2dpi.sam'
#running it through the terminal
os.system(first_alignment)
#aligning donor 2
second_alignment = 'bowtie2 --quiet -x HCMV -1 topSRR5660033_1.fastq -2 topSRR5660033_2.fastq -S mapped_6dpi.sam'
os.system(second_alignment)
#mapping the alligned donor 1
mapped_2dpi = 'samtools view -c -F 4 mapped_2dpi.sam'
#running it through terminal
os.system(mapped_2dpi)
#mapping the second donor
mapped_6dpi = 'samtools view -c -F 4 mapped_6dpi.sam'
os.system(mapped_6dpi)
#printing out results to the log
echo_1 = 'echo "Donor 1 (2dpi) had $(expr $(wc -l < topSRR5660030_1.fastq) / 4) read pairs before Bowtie2 filtering and $(samtools view -c -F 4 mapped_2dpi.sam) read pairs after." >> PipelineProject.log'
os.system(echo_1)
echo_2 = 'echo "Donor 1 (6dpi) had $(expr $(wc -l < topSRR5660033_1.fastq) / 4) read pairs before Bowtie2 filtering and $(samtools view -c -F 4 mapped_6dpi.sam) read pairs after." >> PipelineProject.log'
os.system(echo_2)

#third problem:
#creating a bam file for 2dpi
bam1 = 'samtools view -b -F 4 mapped_2dpi.sam > mapped_2dpi.bam'
os.system(bam1)
#outputs paired ends to the bam file
into_bam1 = 'samtools fastq -1 mapped_2dpi.1.fastq -2 mapped_2dpi.2.fastq -s mapped_2dpi.unpaired.fastq mapped_2dpi.bam'
os.system(into_bam1)
#creating bam file for 6dpi
bam2 = 'samtools view -b -F 4 mapped_6dpi.sam > mapped_6dpi.bam'
os.system(bam2)
#outputting paired ends into bam file
into_bam2 = 'samtools fastq -1 mapped_6dpi.1.fastq -2 mapped_6dpi.2.fastq -s mapped_6dpi.unpaired.fastq mapped_6dpi.bam'
os.system(into_bam2)
#creating a combined assembly with a kmer size of 99
combined = 'spades.py -k 99 -t 1 --isolate -1 mapped_2dpi.1.fastq -2 mapped_2dpi.2.fastq -1 mapped_6dpi.1.fastq -2 mapped_6dpi.2.fastq -o HCMV_combined_assembly'
os.system(combined)
#printing out results to the log
echo3 = 'echo "spades.py -k 99 -t 1 --isolate -1 mapped_2dpi.1.fastq -2 mapped_2dpi.2.fastq -1 mapped_6dpi.1.fastq -2 mapped_6dpi.2.fastq -o HCMV_combined_assembly" >> PipelineProject.log'
os.system(echo3)

#fourth proplem:
#function to count contigs
bp = 0
def count_contigs(fasta_file, length_threshold=1000):
    #establishing count
    count = 0
    global bp
    #for loop to count the contigs in the fasta file
    for record in SeqIO.parse(fasta_file, "fasta"):
        if len(record.seq) > length_threshold:
            #add 1 to the count
            count += 1
            bp += len(record.seq)
    #return count
    return count
#calls for the function
contigs = (count_contigs("HCMV_combined_assembly/K99/final_contigs.fasta"))
print(contigs)
print(bp)

with open('PipelineProject.log', 'a') as f:
    f.write("There are " + str(contigs) + " contigs > 1000bp in the assmbly.")
    f.write("\n")
    f.write("There are " + str(bp) + " bp in the assembly.")
    f.write("\n")
    f.close()

#fifth problem:
# function to find longest contig
def longest_contig(fasta_file):
    #stores the contig
    contig = None
    #records length
    max_length = 0
    #for loop that parses through the fasta file
    for record in SeqIO.parse(fasta_file, "fasta"):
        #if next record seq is longer that current saved seq
        if len(record.seq) > max_length:
            #saves new seq
            contig = record
            #records new max_length
            max_length = len(record.seq)

    return contig
#runs the function
longest = longest_contig("HCMV_combined_assembly/K99/final_contigs.fasta")
print(longest)
#saving it to a new file to run blast with
with open('problem5_contig_file.fasta', 'w') as handle:
    SeqIO.write(longest, handle, "fasta")

#downloading data base for betaherpsvirinae
subfamily = 'datasets download virus genome taxon Betaherpesvirinae --include genome'
os.system(subfamily)
os.system(unzip)
#making my own copy and renaming it
move = 'mv ncbi_dataset/data/genomic.fna Betaherpesbirinae.fna'
#making database
db = 'makeblastdb -in Betaherpesbirinae.fna -out Betaherpesbirinae -title Betaherpesbirinae -dbtype nucl'
os.system(db)
#using blast 
blast_command = 'blastn -query problem5_contig_file.fasta -db Betaherpesbirinae -out myresults.tsv -outfmt "6 sacc pident length qstart qend sstart send bitscore evalue stitle" -max_target_seqs 10 -max_hsps 1'
os.system(blast_command)
#opening output file and saving results
with open('myresults.tsv', 'r') as f:
    lines = f.readlines()
    f.close()
with open('PipelineProject.log', 'a') as file:
    for i in lines:
        file.write(i)
    file.close()