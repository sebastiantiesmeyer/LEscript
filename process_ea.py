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
import random

from deap import base
from deap import creator
from deap import tools
from deap import algorithms


weights = []
sittings = []
combinations = []
persons = []

class person():
    """ a person that has languages is wants to practice and teach..."""
    def __init__(self, l_p, l_t, id_number):
        self.id = id_number;
        self.sittings = []
        self.l_t=l_t
        self.l_p=l_p
        
        for i in [0,1]:
            for lang in l_p:
                self.sittings.append(sitting(i,lang,True,self))
            for lang in l_t:
                self.sittings.append(sitting(i,lang,False,self))

        persons.append(self)
                
def sigmoid(x):
    return(1/(1+np.exp(-x)))               
                
class sitting():
    def __init__(self, time, language, practice, person, init=-1.0, bias = -0.1):
        self.t = time
        self.l = language
        self.p = practice
        self.id=len(sittings)
        self.person = person
        sittings.append(self)
        
        
def load_sheet(name):
    sheet = pd.read_excel(name,header=2)
    return sheet

def extract_languages(string):
    string = re.split('\W+',string)  
    string = [s for s in string if s != '']
    return string

def clean_pool(pool):
    
    langs_offered = []
    langs_requested = []
    
    for i in range(len(pool)):
        langs_offered += [l for l in pool[i].l_t if not l in langs_offered]
        langs_requested += [l for l in pool[i].l_p if not l in langs_requested]

    for i in range(len(pool)):
        if not any([l in langs_requested for l in pool[i].l_t]) or not any([l in langs_offered for l in pool[i].l_p]):
            del pool[i]
            pool = clean_pool(pool)
            break
    return(pool)

def create_pool(sheet):
    pool = []
    id_number = 0;
    for i,row in sheet.iterrows():
        try:
            p = person(extract_languages(row[4])+extract_languages(row[5]),extract_languages(row[6]),id_number)
            pool.append(p)
            id_number+=1
        except:
            pass
    
    for i,pers in enumerate(persons):
        combinations.append([])
        for j in range(len(pers.sittings)-1):
            for k in range(j+1,len(pers.sittings)):
                if (pers.sittings[k].t != pers.sittings[j].t):
                    if (pers.sittings[k].p != pers.sittings[j].p):
                        combinations[-1].append([pers.sittings[k],pers.sittings[j]])

    return (pool)


def draw_tables():
    G = nx.DiGraph()
    node_sizes = []
    node_colors=[]
    edge_colors = []
    labeldict = {}
#    for i in range(len(sittings)):
##        print(sittings[i].s)
#        node_sizes.append(float(sittings[i].s==1)*300+100)
#        G.add_node(i)#+
#        labeldict[i]=str(int(sittings[i].p))+sittings[i].l[0]+str(sittings[i].t)
#        node_colors.append(sittings[i].person.id/len(persons))
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
#    nx.draw_circular(G, node_color=node_colors, node_size=node_sizes, width = 1, 
#                     labels = labeldict, edge_color=edge_colors, with_labels=True)
#

#def print_results():
#    for i in range(len(sittings)):
#        if sittings[i].s==1:
#            print(sittings[i].person.id,sittings[i].l,sittings[i].t,sittings[i].p)
#    
rnd=0
def evalLE(individual):

    score=0
    
    sittings_1 = []
    sittings_2 = []

    for i,n in enumerate(individual):
        if n>0:
            if combinations[i][n-1][0].t==0: 
                [sitting_1,sitting_2]=combinations[i][n-1]
            else:
                [sitting_2,sitting_1]=combinations[i][n-1]
            sittings_1.append(sitting_1)
            sittings_2.append(sitting_2)
        
#    print(sittings_1)
    langs_t_1,langs_t_2,langs_p_1,langs_p_2 = [],[],[],[]
    global rnd
    for s in sittings_1:
        if s.p:
            langs_p_1.append(s.l)
        else:
            langs_t_1.append(s.l)
    for s in sittings_2:
        if s.p:
            langs_p_2.append(s.l)
        else:
            langs_t_2.append(s.l)
    
    for lang in set(langs_p_1+langs_t_1):
        if not lang in langs_p_1 or not lang in langs_t_1:
            score-=0.00001*rnd
        else:
            score += 1/max(0.5,(langs_p_1.count(lang)-langs_t_1.count(lang))**2)
#            print(score)
        
        
    for lang in set(langs_p_2+langs_t_2):
        if not lang in langs_p_2 or not lang in langs_t_2:
            score-=0.00001*rnd
        else:
            score += 1/max(0.5,((langs_p_2.count(lang)-langs_t_2.count(lang))**2))
#            print(score)
    rnd+=1
    
    return (score,)
        

def mutUniformIntNp(low, up, indpb,individual):
    """Mutate an individual by replacing attributes, with probability *indpb*,
    by a integer uniformly drawn between *low* and *up* inclusively.
    
    :param individual: :term:`Sequence <sequence>` individual to be mutated.
    :param low: The lower bound or a :term:`python:sequence` of
                of lower bounds of the range from wich to draw the new
                integer.
    :param up: The upper bound or a :term:`python:sequence` of
               of upper bounds of the range from wich to draw the new
               integer.
    :param indpb: Independent probability for each attribute to be mutated.
    :returns: A tuple of one individual.
    """
    size = individual.shape[0]-1

    if up.shape[0]-1 < size:
        raise IndexError("up must be at least the size of individual: %d < %d" % (len(up), size))
    
    for i, xl, xu in zip(range(size), low, up):
        if random.random() < indpb[i]:
            individual[i] = random.randint(xl, xu)
    
    return individual,

def cxTwoPointCopy(ind1, ind2):
    """Execute a two points crossover with copy on the input individuals. The
    copy is required because the slicing in numpy returns a view of the data,
    which leads to a self overwritting in the swap operation. It prevents
    ::
    
        >>> import numpy
        >>> a = numpy.array((1,2,3,4))
        >>> b = numpy.array((5.6.7.8))
        >>> a[1:3], b[1:3] = b[1:3], a[1:3]
        >>> print(a)
        [1 6 7 4]
        >>> print(b)
        [5 6 7 8]
    """
    size = ind1.shape[0]
    cxpoint1 = random.randint(1, size)
    cxpoint2 = random.randint(1, size - 1)
    if cxpoint2 >= cxpoint1:
        cxpoint2 += 1
    else: # Swap the two cx points
        cxpoint1, cxpoint2 = cxpoint2, cxpoint1

    ind1[cxpoint1:cxpoint2], ind2[cxpoint1:cxpoint2] \
        = ind2[cxpoint1:cxpoint2].copy(), ind1[cxpoint1:cxpoint2].copy()
        
    return ind1, ind2

name = "sheet.xlsx"
pool = create_pool(load_sheet(name))
#for i in range(900):update_round(i*0.001)
draw_tables()

def init(): return 0
    
creator.create("FitnessMax", base.Fitness, weights=(1.0,))
creator.create("Individual", np.ndarray, fitness=creator.FitnessMax)

toolbox = base.Toolbox()
# Attribute generator 
#toolbox.register("attr_bool", random.randint, 0, 1)
# Structure initializers
toolbox.register("individual", tools.initRepeat, creator.Individual, 
    init, len(combinations))
toolbox.register("population", tools.initRepeat, list, toolbox.individual)

toolbox.register("evaluate", evalLE)
toolbox.register("mate", tools.cxTwoPoint)
toolbox.register("mutate", mutUniformIntNp,np.array([0 for c in combinations]), 
                 np.array([len(c) for c in combinations]), np.array([0.5 for c in combinations]))
toolbox.register("select", tools.selTournament, tournsize=300)

#def main():
pop = toolbox.population(n=4000)
hof = tools.HallOfFame(1, lambda ind1,ind2: all([ind1[i]==ind2[i] for i in range(ind1.shape[0])]))
stats = tools.Statistics(lambda ind: ind.fitness.values)
stats.register("avg", np.mean)
stats.register("std", np.std)
stats.register("min", np.min)
stats.register("max", np.max)

pop, log = algorithms.eaSimple(pop, toolbox, cxpb=0.5, mutpb=0.5, ngen=500, 
                               stats=stats, halloffame=hof, verbose=True)

