from layout import BlockDiagramLayout
from gen_clips import GenerateCLIPS
from gen_dot import GenerateDot
from hierarchy import Hierarchy
from read_csv import ReadCSV
from os import walk
import argparse


def main():
    parser = argparse.ArgumentParser(__file__, description='CSV to Block Diagram Converter')
    parser.add_argument('--path', '-p', help='Enter file path to csv directory', required=True)
    parser.add_argument('--dot', '-d', help='Generate dot files', required=False, type=bool)
    parser.add_argument('--clips', '-c', help='Generate CLIPS facts', required=False, type=bool)
    args = parser.parse_args()
    csv_dir_path = args.path
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

    hierarchy = hier.sorted_graph
    hier.construct_graph()
    hier.bfs_edges()
    levels = hier.levels

    for (directory, _, files) in walk(csv_dir_path):
        for f in files:
            try:
                if len(f.split('.')) == 2 and f.split('.')[1] == 'csv':
                    read_csv.read_csv_contents(directory, f)
            except NameError as e:
                print e.message

    knol = read_csv.knol_all
    layout = BlockDiagramLayout(levels, knol, hierarchy)
    layout.draw_layout()
    layout.write_dot()

    dot_out_dir = layout.dot_out_dir
    block_out_dir = layout.block_out_dir

    # write dot for individual blocks
    if args.dot:
        gen_dot = GenerateDot(dot_out_dir, block_out_dir)
        print '-' * 100
        print 'GENERATE DOT FILE(S)'
        print '-' * 100
        block_map = {}
        for i, block in enumerate(knol.keys()):
            print i+1, '=', block.replace('.csv', '')
            block_map[i+1] = block
        print
        choice = raw_input('Choose block(s) for dot file generation (space separated): ')
        gen_dot.generate_dot(choice, block_map, knol)

    # generate CLIPS facts for individual blocks
    if args.clips:
        gen_clips = GenerateCLIPS()
        print '-' * 100
        print 'GENERATE CLIPS FACTS'
        print '-' * 100
        block_map = {}
        for i, block in enumerate(knol.keys()):
            print i + 1, '=', block.replace('.csv', '')
            block_map[i + 1] = block
        print
        choice = raw_input('Choose block(s) for CLIPS facts generation (space separated): ')
        gen_clips.generate_clips_facts(choice, block_map, knol)

if __name__ == '__main__':
    main()

