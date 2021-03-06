#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Apr 10 23:18:23 2019

@author: sebastian
"""

import pandas as pd
import numpy as np
import re
import copy
import networkx as nx
import matplotlib.pyplot as plt

class person():
    """ a person that has languages is wants to practice and teach..."""
    def __init__(self, l_p, l_t, id_number):
        self.id = id_number;
        self.l_p = l_p
        self.l_t = l_t
        self.t_p = None
        self.t_t = None
        
class table():
    def __init__(self,language, second, id_number):
        self.language = language
        self.second = second
        self.has_teacher = False
        self.has_pupil = False
        self.id = id_number
        
        
def load_sheet(name):
    sheet = pd.read_excel(name,header=2)
    return sheet

def extract_languages(string):
    string = re.split('\W+',string)  
    return string

def clean_pool(pool):
    
    langs_offered = []
    langs_requested = []
    
    for i in range(len(pool)):
        langs_offered += [l for l in pool[i].l_t if not l in langs_offered]
        langs_requested += [l for l in pool[i].l_p if not l in langs_requested]

    for i in range(len(pool)):
        if not any([l in langs_requested for l in pool[i].l_t]) or not any([l in langs_offered for l in pool[i].l_p]):
            pool.pop(i)
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

    
    return clean_pool(pool)

def draw_tables(pool,t_1,t_2):
    G = nx.DiGraph()
    colormap = []
    for p in pool:       
        add_edge=[0,0]
        if p.t_p is not None:
            G.add_node(str(p.id)+'_p')
            colormap.append('red')
            add_edge[0]=1
            if not "t_"+str(p.t_p.id) in G.nodes:
                G.add_node("t_"+str(p.t_p.id))
                colormap.append('blue')

            G.add_edge("t_"+str(p.t_p.id),str(p.id)+'_p')
            
        if p.t_t is not None:
            G.add_node(str(p.id)+'_t')
            colormap.append('red')

            add_edge[1]=1
            
            if not "t_"+str(p.t_t.id) in G.nodes:
                G.add_node("t_"+str(p.t_t.id))
                colormap.append('blue')

            G.add_edge("t_"+str(p.t_t.id),str(p.id)+'_t')
        
        if sum(add_edge)==2: 
            G.add_edge(str(p.id)+'_p',str(p.id)+'_t') 

    nx.draw(G,  with_labels=True)
    
def fit_pool(pool,solution = [] , t_1 = [], t_2 = [],bad_tables = [], bad_people =[], id_number = 0, init = False):
    todo = pool.copy()
    
    bad_tables_cp = copy.deepcopy(bad_tables)
    bad_people_cp = copy.deepcopy(bad_people)
    
    for i in range(len(pool)):
        #some stopping criteria
        if (len(bad_tables)> len(pool)*2):
            return [todo, solution, t_1, t_2, bad_tables, bad_people]
        print(i,len(pool)*2,len(bad_tables))

        pool_cp = copy.deepcopy(pool)
        p = pool_cp.pop(i)   
        solution_cp = copy.deepcopy(solution)
        
        #add the person as a new freeby:
        for lp in p.l_p:     
            t_1_cp = copy.deepcopy(t_1)
            t1 = table(lp,0,id_number)
            t1.has_pupil=True
            id_number+=1
            p.t_p = t1
            t_1_cp.append(t_1_cp)
            bad_tables_cp.append(t_1_cp)
            
            for lt in p.l_t:
                t_2_cp = copy.deepcopy(t_2)
                t2 = table(lt,1,id_number)
                t2.has_teacher=True
                p.t_t = t2
                id_number+=1
                t_2_cp.append(t2)
                bad_tables_cp.append(t_2_cp)
                bad_people_cp.append(p)
                
                solution_cp.append(p)
#                draw_tables(solution_cp,t_1_cp,t_2_cp)
#                plt.pause(0.01)
                
                fit_pool(pool_cp,solution_cp,t_1_cp,t_2_cp,bad_tables_cp,bad_people_cp,id_number=id_number)
                
                            
                
            
        
        else:
            pass
        
    return solution
        


name = "/home/sebastian/Documents/LEscript/sheet.xlsx"
pool = create_pool(load_sheet(name))
fit_pool(pool,[],[],[],init=True)

