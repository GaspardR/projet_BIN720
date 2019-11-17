# **Project description**

This repository is our term project for the MSc course [BIN702 - Bioinformatic Algorithms](https://www.usherbrooke.ca/admission/fiches-cours/BIN702/), given by professor [Manuel Lafond](http://info.usherbrooke.ca/mlafond/index.php) of the Computer Science department at the [Université de Sherbrooke](https://www.usherbrooke.ca/).

The aim of this project is to simulate the evolution of a healthy cell towards a cancerous cell.

### **Prerequisites**

This project was developped using `Python 3.6` and the following packages are
necessary for it to run.

- [Biopython](https://biopython.org/) (v1.74 or higher)

It can be installed using `pip3 install biopython` or [click here to follow alternative ways](https://biopython.org/wiki/Download).

### **Installing**

Installing this project is as easy as cloning the git repository.
```
git clone https://github.com/GaspardR/projet_BIN720.git
```

Next, you need to download the human genome annotation and each chromosome sequence from Ensembl
```bash
cd /path/to/this/repository/
mkdir data/
cd data/

# All chromosome sequences
wget ftp://ftp.ensembl.org/pub/release-98/fasta/homo_sapiens/dna/Homo_sapiens.GRCh38.dna.chromosome.*
gunzip *
cat * > all_chromosome.fa
rm Homo_sapiens.GRCh38.dna.chromosome*

# Genome annotation
wget ftp://ftp.ensembl.org/pub/release-98/gtf/homo_sapiens/Homo_sapiens.GRCh38.98.gtf.gz
gunzip Homo_sapiens.GRCh38.98.gtf.gz
awk '$3 == "gene" {print $0}' Homo_sapiens.GRCh38.98.gtf > annotation.gtf
```

### **Running**
Simply run with:
```
python3 main.py
```

## **Authors**
- **Gaspard Reulet**, <gaspard.reulet@usherbrooke.ca>
- **Cyril Mougin** <cyril.mougin@usherbrooke.ca>
