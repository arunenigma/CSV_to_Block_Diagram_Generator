from hierarchy import Hierarchy
from read_csv import ReadCSV
from os import walk
import sys

if __name__ == '__main__':
    csv_dir_path = sys.argv[1]
    read_csv = ReadCSV()
    hier = Hierarchy()
    for (directory, _, files) in walk(csv_dir_path):
        for f in files:
            try:
                if len(f.split('.')) == 2 and f.split('.')[1] == 'csv':
                    csv_name, csv_obj = read_csv.read_csv(directory, f)
                    hier.collect_first_row(csv_name, csv_obj)
            except NameError as e:
                print e.message

    hierarchy_edges = hier.hierarchy
    print hierarchy_edges
    hier.construct_graph()
    print hier.bfs_edges()