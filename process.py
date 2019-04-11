#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Apr 10 23:18:23 2019

@author: sebastian
"""

import pandas as pd
import numpy as np
import re


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
        
def load_sheet(name):
    sheet = pd.read_excel(name,header=2)
    return sheet

def extract_languages(string):
    string = re.split('\W+',string)  
    return string

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
    return pool



def fit_pool(pool,solution = None , t_1 = [], t_2 = [],bad_tables = [], bad_people =[], id_number = 0, init = False):
    todo = pool.copy()
    
    for i in range(len(pool)):
        #some stopping criteria
        if (len(bad_tables)> len(pool)*2):
            return [todo, t_t, t_p, bad_tables, bad_people]
        
        pool_cp = pool.copy()
        p = pool_cp.pop(i)        
        #add the person as a new freeby:
        for lp in p.l_p:            
            t1 = table(lp,0,id_number)
            t1.has_pupil=True
            id_number+=1
            for lt in p.l_t:
                t2 = table(lt,1,id_number)
                t2.has_teacher=True
                id_number+=1
                            
            if not init:
                t1 = table(lp,1,id_number)
                t1.has_pupil=True
                id_number+=1
                for lt in p.l_t:
                    t2 = table(lt,0,id_number)
                    t2.has_teacher=True
                    id_number+=1
                
            
        
        
        else:
            pass
        


name = "/home/sebastian/Documents/LEscript/sheet.xlsx"
pool = create_pool(load_sheet(name))
fit_pool(pool,None,[],[],init=True)

