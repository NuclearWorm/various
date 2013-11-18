#!/usr/bin/env python 
"""
Morphology module for word normalization
Works with AOT dictionaries: http://www.aot.ru/download.php 

Usage summary
=============
import Morphology

# create Morphology object
# first argument - is path for sqlite3 db cache which will be created automatically
# second argument - is path to morphs.mrd file, not necessary if cache is already built
morph = Morphology.Morphology('path/to/cache', 'path/to/morphs.mrd')
print morph.normalize('sold')

# prints set(['sell'])

License
=======
Copyright (c) 2008 Alexander Pak <irokez@gmail.com>

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
'''
"""

import sqlite3
import re
import os

class Morphology:
    conn = None
    db = None
    
    def __init__(self, db, lexicon = None):
        load = False
        if not os.path.exists(db):
            load = True
            
        self.conn = sqlite3.connect(db, check_same_thread = False)

        self.db = self.conn.cursor()

        if load:
            self.load(lexicon)
            
    def close(self):
        self.db.close()
        self.conn.close()
            
    def skip_lines(self, handle):
        line = handle.readline()
        if not len(line):
            return False
        
        line = line.strip()
        if re.search('^\d+$', line):
            for i in range(0, int(line)):
                line = handle.readline()
                if not len(line):
                    return False
        else:
            print line
            return False 
        
        return True

    def load(self, file):
        handle = open(file, 'r')
        
        # load rules
        self.load_rules(handle)
        
        # skip accents
        if not self.skip_lines(handle):
            return False
        
        # skip logs
        if not self.skip_lines(handle):
            return False
        
        # skip prefixes
        if not self.skip_lines(handle):
            return False
        
        print self.load_lemmas(handle), 'lemmas loaded'
        
        handle.close()
        
    def load_rules(self, handle):
        # create table
        self.db.execute('''create table rules(
                            id integer,
                            prefix text,
                            suffix text)''')
        
        lines = handle.readline().strip()
        reg_split = re.compile('\\%');
        alf = '[a-zA-Z]';
        reg_rule = re.compile('^(?P<suffix>' + alf + '*)\\*(?P<ancode>' + alf + '+)(?:\\*(?P<prefix>' + alf + '+))?$')
        
        for i in range(0, int(lines)):
            line = handle.readline()
            if not len(line):
                break
            
            rules = reg_split.split(line.strip())
            
            for rule in rules:
                match = reg_rule.search(rule)
                if match is not None:
                    record = match.groupdict()                  
                    if not record.has_key('prefix') or record['prefix'] is None:
                        record['prefix'] = ''
                        
                    suffix = record['suffix'].lower()
                    prefix = record['prefix'].lower()
                    
                    self.db.execute('insert into rules (id, prefix, suffix) values (?, ?, ?)', (i, prefix, suffix))

        self.db.execute('create index rules_id on rules(id)')
        return i
    
    def load_lemmas(self, handle):
        # create table
        self.db.execute('''create table lemmas(
                            base text,
                            rule integer)''')

        lines = int(handle.readline().strip())
        reg_split = re.compile('\s+')
        
        for i in range(0, lines):
            line = handle.readline()
            if not len(line):
                break
            
            record = reg_split.split(line)
            self.db.execute('insert into lemmas values(?, ?)', (record[0].lower() + '%', int(record[1])))
            
        self.db.execute('create index lemmas_base on lemmas(base)')
        
        return i
    
    def make_forms(self, lemma):
        self.db.execute('select prefix, suffix from rules where id = ?', (lemma['rule'],))

        forms = []
        for rule in self.db.fetchall():
            forms.append({
                          'base': lemma['base'],
                          'form': rule[0] + lemma['base'] + rule[1],
                          })
        return forms

    def normalize(self, word):
        word = word.lower()
        
        self.db.execute('select base, rule from lemmas where ? like base', (word,))
        
        lemmas = []
        for lemma in self.db.fetchall():
            base = lemma[0][0:-1]
            base = base.encode('utf-8')
            forms = self.make_forms({'base': base, 'rule': lemma[1]})
            for form in forms:
                if word == form['form']:
                    init_form = forms[0]['form'].encode('utf-8')
                    lemmas.append(init_form)
                    
        return set(lemmas)