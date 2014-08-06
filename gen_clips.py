#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import shutil


class GenerateCLIPS(object):
    @staticmethod
    def generate_clips_facts(choice, block_map, knol):
        choice = choice.split(' ')
        # create a clips out directory
        out_dir = './clips_out'
        if os.path.exists(out_dir):
            shutil.rmtree(out_dir)
        os.makedirs(out_dir)
        for n in choice:
            block = block_map[int(n)]
            block_label = block.replace('.csv', '')
            clips_file = block_label + '.txt'
            clips_file_dir = out_dir + '/' + clips_file
            clips_out = open(clips_file_dir, 'wb')
            def_temp = """(deftemplate spec-io-fact(multislot VNV (type STRING))
(slot module (type STRING))
(slot signalName (type STRING))
(slot fieldname (type STRING))
(slot  direction (type STRING))
(slot source (type STRING))
(slot active (type STRING))
(slot iotype   (type STRING))
(slot logicalName (type STRING))
(slot constraint (type STRING))
(multislot comment (type STRING))
)"""
            def_temp_cleaned = ''
            for line in def_temp.strip().split('\n'):
                def_temp_cleaned += line

            clips_out.write(def_temp_cleaned)
            clips_out.write('\n')
            facts_head = """deffacts("""
            clips_out.write(facts_head)
            vnv = raw_input('Enter VNV name: ')
            for i, signal in enumerate(knol[block]['Signal Name']):
                signal = signal.strip()
                fact = """(spec-io-fact (VNV "%s")
(module "%s")
(signalName "%s")
(fieldName "%s")
(width "%s")
(direction "%s")
(source "%s")
(active "%s")
(iotype "%s")
(logicalName "%s")
(constraint "%s")
(comment "%s"))"""
                field = knol[block]['Field'][i].strip()
                width = knol[block]['Width'][i].strip()
                direction = knol[block]['Direction'][i].strip()
                source = knol[block]['Source'][i].strip()
                active = knol[block]['Active'][i].strip()
                io_type = knol[block]['Type'][i].strip()
                logical_name = knol[block]['Logical Name'][i].strip()
                constraints = knol[block]['Constraints'][i].strip()
                comments = knol[block]['Comments'][i].strip()
                fact = fact % (
                    vnv, block_label, signal, field, width, direction, source, active, io_type, logical_name, constraints,
                    comments)
                fact_cleaned = ''
                for line in fact.strip().split('\n'):
                    fact_cleaned += line
                clips_out.write(fact_cleaned)
                clips_out.write('\n')
            clips_out.write(')')
            clips_out.close()