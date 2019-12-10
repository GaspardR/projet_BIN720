# **Project description**

This repository is our term project for the MSc course [BIN702 - Bioinformatic Algorithms](https://www.usherbrooke.ca/admission/fiches-cours/BIN702/), given by professor [Manuel Lafond](http://info.usherbrooke.ca/mlafond/index.php) of the Computer Science department at the [Université de Sherbrooke](https://www.usherbrooke.ca/).

The aim of this project is to simulate the evolution of a healthy cell towards a cancerous cell.

### **Prerequisites**

This project was developped using `Python 3.6` and only the included basic packages are used.

### **Installing**

Installing this project is as easy as cloning the git repository.
```
git clone https://github.com/GaspardR/projet_BIN720.git
```

Next, you need to download the human genome annotation.
Also, you will need to download the cancer associated genes annotation from CancerMine.
```bash
cd /path/to/this/repository/
mkdir data/
cd data/

# Genome annotation
wget ftp://ftp.ensembl.org/pub/release-98/gtf/homo_sapiens/Homo_sapiens.GRCh38.98.gtf.gz
gunzip Homo_sapiens.GRCh38.98.gtf.gz
awk '$3 == "gene" {print $0}' Homo_sapiens.GRCh38.98.gtf > annotation.gtf

# Cancer associated genes annotation
wget https://zenodo.org/record/3525385/files/cancermine_collated.tsv
```

### **Running**
Simply run with:
```
python3 main.py /path/to/annotation.gtf /path/to/cancer_genes_annotation.tsv $SIZE_OF_POPULATION $NUMBER_OF_CYCLES
```
Where `$SIZE_OF_POPULATION`is the number of cells to use for the simulation and
`$NUMBER_OF_CYCLES` the number of cycles to do for each cell.

The return value is the number of cells that developped a cancerous state.

__NOTE:__
Usage of custom annotations for both genes and cancer_genes is possible, please follow see the `--help` and/or don't hesitate to contact us!

## **Authors**
- **Gaspard Reulet**, <gaspard.reulet@usherbrooke.ca>
- **Cyril Mougin**, <cyril.mougin@usherbrooke.ca>
