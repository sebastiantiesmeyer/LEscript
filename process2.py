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

weights = []
sittings = []

class person():
    """ a person that has languages is wants to practice and teach..."""
    def __init__(self, l_p, l_t, id_number):
        self.id = id_number;
        self.sittings = []
        self.l_t=l_t
        self.l_p=l_p
        for lang in l_p:
            [self.sittings.append(sitting([0,1][i],lang,True,self)) for i in [0,1]]
            
        for lang in l_t:
            [self.sittings.append(sitting([0,1][i],lang,False,self)) for i in [0,1]]
            
        for i in range(len(self.sittings)-1):
            for j in range(i+1,len(self.sittings)):
                if self.sittings[i].t == self.sittings[j].t:
                    w = weight(-1,[self.sittings[i],self.sittings[j]])
                    self.sittings[i].weights.append(w)
                    self.sittings[j].weights.append(w)
                if self.sittings[i].p == self.sittings[j].p:
                    w = weight(-1,[self.sittings[i],self.sittings[j]])
                    self.sittings[i].weights.append(w)
                    self.sittings[j].weights.append(w)
                    
def sigmoid(x):
    return(1/(1+np.exp(-x)))               
                
class sitting():
    def __init__(self, time, language, practice, person, init='rand', bias = -0.1):
        self.t = time
        self.l = language
        self.p = practice
        if init=='rand':
            self.s = np.random.uniform()
#            self.s = (-1 if np.random.uniform()>0.5 else 1)
        else:
            self.s = init
        self.b = bias
        self.id=len(sittings)
        self.person = person
        self.weights = []
        self.delta = 0
        sittings.append(self)
    def prep_delta(self, eta=0.1):
        for i in range(len(self.weights)):
            self.delta += self.weights[i].get_other(self).s*self.weights[i].w*eta
    def update(self):
        if np.random.uniform()<sigmoid(self.delta):
            self.s=1
        else:
            self.s=-1
        

        
        
class weight():
    def __init__(self,w, ends):
        self.w = w
        self.ends = ends
        weights.append(self)
    def get_other(self,w):
        if w==self.ends[0]:
            return self.ends[1]     
        elif w==self.ends[1]:
            return self.ends[0]        
        
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
        if i>10:
            break

    for i in range(len(sittings)-1):
        for j in range(i+1,len(sittings)):
            if (not (sittings[i].person == sittings[j].person)) and  sittings[i].t == sittings[j].t and sittings[i].l == sittings[j].l and not(sittings[i].p == sittings[j].p):
                w = weight(1, [sittings[i],sittings[j]])
                sittings[i].weights.append(w)
                sittings[j].weights.append(w)
    for i in range(len(weights)):
        if weights[i].ends[0].person == weights[i].ends[1].person and (weights[i].ends[0].t == weights[i].ends[1].t or (weights[i].ends[0].p == weights[i].ends[1].p)):
            weights[i].w=-1
    
    return (pool)


def draw_tables():
    G = nx.DiGraph()
    node_colors = []
    edge_colors = []
    for i in range(len(sittings)):
        node_colors.append(float(sittings[i].s))
        G.add_node(i)
        
    for i in range(len(sittings)):
        for w in sittings[i].weights:

            ln = len(G.edges)
            j=w.get_other(sittings[i]).id
            
            G.add_edge(i,j)
            if ln<len(G.edges):
                edge_colors.append((w.w))
        


    print(node_colors)
        
    nx.draw(G, node_color=node_colors, width = 1, edge_color=edge_colors, with_labels=True)
    
def print_energy():
    print(sum([w.ends[0].s*w.ends[0].s*w.w for w in weights]))
        
def print_results():
    for i in range(len(sittings)):
        if sittings[i].s==1:
            print(sittings[i].person.id,sittings[i].l,sittings[i].t,sittings[i].p)
    
def update_round(eta=0.1):
    for i in range(len(sittings)):
        sittings[i].prep_delta(eta)    
    for i in range(len(sittings)):
        sittings[i].update()
    print_energy()
    for i in range(len(weights)):
        if weights[i].w<0:
            weights[i].w-=1

name = "/home/sebastian/Documents/LEscript/sheet.xlsx"
pool = create_pool(load_sheet(name))
[update_round(i*0.001) for i in range(500)] 
draw_tables()
print_results()

