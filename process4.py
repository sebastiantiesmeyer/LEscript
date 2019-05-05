#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Apr 10 23:18:23 2019

@author: sebastian
"""

import pandas as pd
import numpy as np
import re
from copy import deepcopy
import networkx as nx
import matplotlib.pyplot as plt
import gc  

tables = []
persons = []
languages = set()

class Person():
    """ a Person that has languages is wants to practice and teach..."""
    def __init__(self, l_p, l_t, id_number):
        self.id = id_number;

        self.langs = [l_t,l_p]
        self.tables=[None,None]
        self.potential = [[],[]]
        persons.append(self)
        
    def get_degree(self):
        return([len(l)  if (self.tables[i] is None) else np.inf for [i,l] in enumerate(self.potential)])
        
    def remove_table(self,table):
        for time in [0,1]:
            if table in self.potential[time]:
                self.potential[time].remove(table)
            if table.lang in self.langs[time]:
                self.langs[time].remove(table.lang)
            if self.tables[time]==table:
                self.tables[time]=None
                
    def cleanup(self):
        '''remove this Person from the Solution.  '''
        for t in self.potential:
            for table in t:
                table.remove_person(self)
        for table in self.tables:
            if table is not None:
                table.remove_person(self)
                
    def seat(self,table):
        
        time = table.t
        
        if self.tables[time] is not None:
            raise Exception('Already busy at time '+str(time))
        
        lang = table.lang
        prac = ([lang in l for l in self.langs])
        
        print(self.id,lang,prac,time)
        
        if not any(prac):
            raise Exception("The person does not speak that language : ( ")
        
        
        prac = np.argmax(prac)
        
        table.seat(self,prac)
        
        for table_ in self.potential[time]:
            table_.remove_person(self)
        for table_ in self.potential[1-time]:
            if table_.lang in self.langs[prac]:
                table_.remove_person(self)
        
        self.tables[time] = table

        self.potential[time]=[]
        self.potential[1-time]=[table_ for table_ in self.potential[1-time] if not table_.lang in self.langs[prac] ]
        self.langs[prac]=[]
        

 
class Table():
    """A Table that has a language and a number of persons."""
    def __init__(self,t,lang,all_people):
        self.t = t
        self.lang = lang
        self.people = [[],[]]
        self.potential = [[],[]]
        for p in all_people:
            for i in [0,1]:
                if lang in p.langs[i]:
                    self.potential[i].append(p)
                    p.potential[t].append(self)
        #tables.append(self)
        
    def get_degree(self):
        return ([len(p) if not(self.people[i]) else np.inf for i,p in enumerate(self.potential)])
        
    def get_id(self):
        return('_'.join([p.id for p in self.people[0]+self.people[1]]))
        
    def cleanup(self):
        for potential in self.potential:
            for pers in potential:
                pers.remove_table(self)        
        for person in self.people:
            for pers in person:
                pers.remove_table(self)
    
    def remove_person(self,person):        
        for time in [0,1]:
            if person in self.potential[time]:
                self.potential[time].remove(person)
            if person in self.people[time]:
                self.people[time].remove(person)   
 
    def seat(self, person, prac):
        
        self.potential[prac].remove(person)
        self.people[prac].append(person)

class Solution():
    """a Solution that gets passed through a recursive solver"""
    def __init__(self,tables,persons):
        self.tables=tables
        self.persons=persons
        
    def get_goodness(self):
        return(sum([sum([t is not None for t in p.tables]) for p in self.persons]))
    
    def clean(self):
        pass
    
    def get_id(self):
        return('-'.join([t.get_id for t in self.tables]))
        
    def __eq__(self, other):
        if isinstance(other,Solution):
            return self.get_id==other.get_id
        else:
            return False

    
def load_sheet(name):
    sheet = pd.read_excel(name,header=2)
    return sheet

def extract_languages(string):
    string = re.split('\W+',string)  
    string = [s for s in string if s != '']
    return string


def create_pool(sheet):
    pool = []
    id_number = 0;
    for i,row in sheet.iterrows():
        try:
            p = Person(extract_languages(row[4])+extract_languages(row[5]),extract_languages(row[6]),id_number)
            pool.append(p)
            [[languages.add(lang) for lang in p.langs[i]] for i in [0,1]]
            id_number+=1
        except:
            pass


    for l in languages:
        [tables.append(Table(i,l,pool)) for i in [0,1]]
        
    return (pool)


    
def clean(world):
    changed = False

    for t in world.tables:
        
        degrees = t.get_degree()
        occupied = [len(persons) for persons in t.people]

        if not all ([degrees[i] or occupied[i] for i in [0,1]]): 
            
            t.cleanup()
            changed=True

            world.tables.remove(t)  
            
            break
            
    for p in world.persons:
        
        degrees = p.get_degree()
        occupied = [table is not None for table in p.tables]
        
        if not all ([degrees[i] or occupied[i] for i in [0,1]]):

            p.cleanup()
            
            changed=True

            world.persons.remove(p)         
            
            break

    if changed:
        return clean(world)
    else:
        return (world)



def solve(world,done = [],champ = None, first_call=False):
    """ Solve the world problem using a greedy approach. Let's hope it works : )  """
    
    
    
    if world is not None:
        
        for p in range(len(world.persons)):
            for time in [0,1]:
                for t in range(len(world.persons[p].potential[time])):
                    world_ = deepcopy(world)
                    world_.persons[p].seat(world_.persons[p].potential[time][t])
    
#                    print(world_.get_goodness())#,world.persons[p].potential)
                    
                    solve(clean(world_),[],champ)
#                break
#            break

            
        
    
    
#    winner = [world.tables[0],world.tables[0].get_degree()[0],0]
#    
#    degrees_tables = np.array([min(t.get_degree())  for t in world.tables], dtype=np.float)
#    degrees_people = np.array([min(p.get_degree())  for p in world.persons], dtype=np.float)
#    degrees_tables[np.isnan(degrees_tables)] = np.inf
#    degrees_people[np.isnan(degrees_people)] = np.inf
#    
#    print(degrees_tables, degrees_people)
#    
#    if first_call:
#        degrees_tables=degrees_tables[::2]
#        degrees_people=degrees_people[::2]
#        idcs = (np.argsort(np.concatenate([degrees_tables,degrees_people])))
#
#    else:        
#        idcs = (np.argsort(np.concatenate([degrees_tables,degrees_people])))
#
#    for i,idx in enumerate(idcs):
#        
#        if i<idcs.shape[0]//2+1:
#            
#            if idx<degrees_tables.shape[0]:                 
#                #is the candidate a Table?
#                Table_ = world.tables[idx]    
#                #is the session in question practice or teach?
#                practice = np.argmin(Table_.get_degree())
#                
#                for i_p in range(len(Table_.potential[practice])):
#                    
#                    #create new world for the next recursive step
#                    world_local=deepcopy(world)
#                    
#                    #find the Table of interest
#                    Table_ = world_local.tables[idx]
#                    
#                    #find the persons of question:
#                    Person_ = Table_.potential[practice][i_p]
#                             
#                    #seat the Person at the Table
#                    Person_.tables[Table_.t]=Table_
#                    # & vice versa
#                    Table_.people[practice].append(Person_)
#                    
#                    removables =[]
#                    #remove Person from all tables at the same time:
#                    for Table__ in Person_.potential[Table_.t]:
#                        Table__.remove_person(Person_)
#                    #remove Person from all tables that are of the same practice category:
#                    for Table__ in Person_.potential[1-Table_.t]:
#                        if (Table__.lang in Person_.langs[practice]):
#                            Table__.remove_person(Person_)
#                            removables.append(Table__)
#                            
#                    for Table__ in removables:
#                        Person_.potential[1-Table_.t].remove(Table__)
#                            
#                    Person_.potential[Table_.t]   = []
#                    
#                    world_local = clean(world_local)
#                    
#                    if not (world_local is None):
#                        champ = solve(world_local,[],champ)
#                        
#                        if champ.get_goodness()<world_local.get_goodness():
#                            return world_local
#        return champ
#                        
#                    
#                    
#                
#            else:
#                Person = world.persons[idx-degrees_tables.shape[0]]
#                practice = np.argmin(Table.get_degree())
#                for Table in Person.potential[practice]:
#                    pass

            
    return champ

name = "sheet.xlsx"
pool = create_pool(load_sheet(name))
world = Solution(tables,persons)
print(len(world.persons))
world = clean(deepcopy(world))
print(len(world.persons))

champ = solve(world,[],world,first_call=True)
#draw_tables()
#print_results()


#
#def print_energy():
#    print(sum([w.ends[0].s*w.ends[0].s*w.w for w in weights]))
# 
#def choose_energy(energies,theta):
#    energies=np.array(energies)
#    energies+=0
#    energies/=energies.sum()
#    print(set(energies))
#    return np.random.choice(range(energies.shape[0]),p=energies )
#       
#def print_results():
#    pass
#
#def draw_tables():
#    G = nx.DiGraph()
#    node_sizes = []
#    node_colors=[s.Person.id/len(persons) for s in sittings]
#    edge_colors = []
#    for i in range(len(sittings)):
#        node_sizes.append(float(sittings[i].s>0.5)*300+100)
#        G.add_node(i)
#        
#    for i in range(len(sittings)):
#        for w in sittings[i].weights:
#
#            ln = len(G.edges)
#            j=w.get_other(sittings[i]).id
#            
#            G.add_edge(i,j)
#            if ln<len(G.edges):
#                edge_colors.append((w.w))
#        
#
#
#    print(node_colors, node_sizes)
#        
#    nx.draw(G, node_color=node_colors, node_size=node_sizes, width = 1, edge_color=edge_colors, with_labels=True)
#    
