#!/usr/bin/env python3

from collections import defaultdict
import csv
import gzip
import re
import sys

def gtf(file):
    """
    gtf.py
    Kamil Slowikowski (https://github.com/slowkow)
    December 24, 2013
    Read GFF/GTF files. Works with gzip compressed files and pandas.
        http://useast.ensembl.org/info/website/upload/gff.html

    Slightly modified by jim (https://github.com/jimni) to add a progress bar

    Slightly modified to remove the progress bar and return a dict instead
    of pandas DataFrame.
    """


    GTF_HEADER  = ['chromosome', 'source', 'feature', 'start', 'end', 'score',
                   'strand', 'frame']
    R_SEMICOLON = re.compile(r'\s*;\s*')
    R_COMMA     = re.compile(r'\s*,\s*')
    R_KEYVALUE  = re.compile(r'(\s+|\s*=\s*)')


    def dataframe(filename):
        """Open an optionally gzipped GTF file and return a dictionnary
        """
        # Each column is a list stored as a value in this dict.
        result = defaultdict(list)

        for i, line in enumerate(lines(filename)):
            for key in line.keys():
                # This key has not been seen yet, so set it to None for all
                # previous lines.
                if key not in result:
                    result[key] = [None] * i

            # Ensure this row has some value for each column.
            for key in result.keys():
                result[key].append(line.get(key, None))

        # print(result.keys())
        return result

    def lines(filename):
        """Open an optionally gzipped GTF file and generate a dict for each line.
        """
        fn_open = gzip.open if filename.endswith('.gz') else open

        with fn_open(filename) as fh:
            for line in fh:
                if line.startswith('#'):
                    continue
                else:
                    yield parse(line)


    def parse(line):
        """Parse a single GTF line and return a dict.
        """
        result = {}

        fields = line.rstrip().split('\t')

        for i, col in enumerate(GTF_HEADER):
            result[col] = _get_value(fields[i])
        # INFO field consists of "key1=value;key2=value;...".
        infos = [x for x in re.split(R_SEMICOLON, fields[-1]) if x.strip()]

        for i, info in enumerate(infos, 1):
            # It should be key="value".
            try:
                key, _, value = re.split(R_KEYVALUE, info, 1)
            # But sometimes it is just "value".
            except ValueError:
                key = 'INFO{}'.format(i)
                value = info
            # Ignore the field if there is no value.
            if value:
                result[key] = _get_value(value)

        return result


    def _get_value(value):
        if not value:
            return None

        # Strip double and single quotes.
        value = value.strip('"\'')

        # Return a list if the value has a comma.
        # if ',' in value:
        #     value = re.split(R_COMMA, value)
        # These values are equivalent to None.
        if value in ['', '.', 'NA']:
            return None

        return value

    return dataframe(file)


def tsv(file):

    def most_frequent_count(lst):
        # ATTENTION, if both values have same count, max is random
        s = max(set(lst), key = lst.count)
        return [s, lst.count(s)]

    genes_dict = defaultdict(list)
    with open(file) as f:
        reader = csv.DictReader(f, delimiter='\t')
        for row in reader:
            if row['role'] != 'Driver':
                genes_dict[row['gene_normalized']].append(row['role'].lower())
        genes_dict = {
            k: most_frequent_count(v)
            for k, v in genes_dict.items()
        }
    return genes_dict

if __name__ == '__main__':
    file = "data/cancermine_collated.tsv"
    tsv(file)
