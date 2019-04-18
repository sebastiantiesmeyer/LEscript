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

class person():
    """ a person that has languages is wants to practice and teach..."""
    def __init__(self, l_p, l_t, id_number):
        self.id = id_number;
        self.occupied = [False, False]
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
        self.people = []
        
        
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
 
        
def corrcoef(data):
    return np.outer(data.flatten(),data.flatten())

def create_weights(data):
    w = np.zeros([data.flatten().shape[0]]*2)
    w.diag = data.flatten()
    #punish double-learner or double-exister:
    w[0::4,0::4]=-10
    w[1::4,1::4]=-10
    w[0::4,1::4]=-10
    w[1::4,0::4]=-10

    w[2::4,2::4]=-10
    w[3::4,3::4]=-10
    w[3::4,2::4]=-10
    w[2::4,3::4]=-10

    
    return(w)
#def create_dataset(pool):
    
def sigmoid(x):
    return(1/(1+np.exp(-x)))

def upgrade(data):
    
    delta = np.zeros(data.shape)
    
    #no 2 timeslots at the same time:
    delta[:,:,:,0]=data[:,:,:,0]-data[:,:,:,1]
    delta[:,:,:,1]=data[:,:,:,1]-data[:,:,:,0]
    
    #no 2 practice/teach sessions at the same time:
    delta[:,:,0,:]=data[:,:,0,:]-data[:,:,1,:]
    delta[:,:,1,:]=data[:,:,1,:]-data[:,:,0,:]
    
    #only 1 "teach language"/"practice language":
    
    mean_p = data[:,:,0,:].sum(1)
    mean_t = data[:,:,1,:].sum(1)
    
    delta[:,:,0,:] += data[:,:,0,:] - np.tile(mean_p[:,np.newaxis,:],[1,16,1])
    delta[:,:,1,:] += data[:,:,1,:] - np.tile(mean_t[:,np.newaxis,:],[1,16,1])
    
    langs_p = data[:,:,0].sum(-1)-data[:,:,1].sum(-1)
    
    
    delta += np.random.normal(size=delta.shape)/50
    delta/=50
    
    return delta
    
    
    
  

name = "/home/sebastian/Documents/LEscript/sheet.xlsx"
pool = create_pool(load_sheet(name))
#data=create_dataset(pool)
inter = [p.l_p for p in pool]+[p.l_t for p in pool]
langs = []
for i in inter:
    langs+= i
langs=set(langs)

data = np.zeros([len(pool),len(langs),2,2])
#dataset shape: [n_people, n_languages, (teach/practice), n_timeslots].

for i,p in enumerate(pool):
    for j,l_p in enumerate(p.l_p):
        for k,lang in enumerate(langs):
            if lang==l_p:
                data[i,k,0,:]=1
        
for i,p in enumerate(pool):
    for j,l_t in enumerate(p.l_t):
        for k,lang in enumerate(langs):
            if lang==l_t:
                data[i,k,1,:]=1
        
data1=data.copy()

for i in range(100):
    data1 = data1+upgrade(data1)
    data1[data1<0]=0
    data1[data1>1]=1
    data1=data1**1.5
    plt.imshow(data1[0,:,:,0])
    plt.pause(0.01)

#return(data)

