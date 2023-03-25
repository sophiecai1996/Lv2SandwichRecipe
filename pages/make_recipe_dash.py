#!/usr/bin/env python


import argparse
import numpy as np
import sys

type_list = ['normal', 'fighting', 'flying', 'poison', 'ground', 'rock',
'bug', 'ghost', 'steel', 'fire', 'water', 'electric',
'grass', 'psychic', 'ice', 'dragon', 'dark', 'fairy']
power_list = ['egg_power', 'catching_power', 'exp_power', 
'item_power', 'raid_power', 'humungo_power', 'teensy_power', 
'encounter_power']

flavorBonus = {('sweet', 'salty'): 'egg_power', ('sweet', 'sour'): 'catching_power', ('sweet', 'bitter'): 'egg_power', ('sweet', 'spicy'): 'raid_power',
('salty', 'sweet'): 'encounter_power', ('salty', 'sour'): 'encounter_power', ('salty', 'bitter'): 'exp_power', ('salty', 'spicy'): 'encounter_power',
('sour', 'sweet'): 'catching_power', ('sour', 'salty'): 'teensy_power', ('sour', 'bitter'): 'teensy_power', ('sour', 'spicy'): 'teensy_power',
('bitter', 'sweet'): 'item_power', ('bitter', 'salty'): 'exp_power', ('bitter', 'sour'): 'item_power', ('bitter', 'spicy'): 'item_power',
('spicy', 'sweet'): 'raid_power', ('spicy', 'salty'): 'humungo_power', ('spicy', 'sour'): 'humungo_power', ('spicy', 'bitter'): 'humungo_power'}
flavor_sort = ['sweet', 'sour', 'bitter', 'salty', 'spicy']

def recipe2power(seasoning_flavor, material_flavor, seasoning_power, material_power):
    flavor = np.array(seasoning_flavor) + np.array(material_flavor)
    power = np.array(seasoning_power) + np.array(material_power)
    # calculate flavor bonus
    flavor_reorder = np.array([flavor[1], flavor[0], flavor[2], flavor[4], flavor[3]])
    index_sort = np.argsort(-flavor_reorder, kind='mergesort')
    flavor_final = (flavor_sort[index_sort[0]], flavor_sort[index_sort[1]])
    # calculate power score
    powerBonus = flavorBonus[flavor_final]
    power[power_list.index(powerBonus)] += 100
    index_sort = np.argsort(-power, kind='mergesort')
    return(power_list[index_sort[0]], power_list[index_sort[1]], power_list[index_sort[2]])

def recipe2type(seasoning_typescore, material_typescore, type1, type2):
    typescore = np.array(seasoning_typescore) + np.array(material_typescore)
    index_sort = np.argsort(-typescore, kind='mergesort')
    if type_list.index(type1) != index_sort[0]:
        return(False, 0, '', '')
    if type2:
        if type_list.index(type2) != index_sort[2]:
            return(False, 0, '', '')
    if typescore[index_sort[2]] >= 180:
        return(True, 2, type_list[index_sort[2]], type_list[index_sort[1]])
    else:
        return(True, 1, type_list[index_sort[2]], type_list[index_sort[1]])

def make_recipe_power(input_type1, input_type2, input_power1, input_power2):
    fh = open('assets/seasoning_combine.txt', 'r')
    seasoning_recipe_list = []
    seasoning_flavor_total = []
    seasoning_power_total = []
    seasoning_typescore_total = []
    for line in fh:
        toks = line.strip().split('\t')
        seasoning_recipe = toks[0].split('|')
        seasoning_recipe_list.append(seasoning_recipe)
        flavor_total = [int(x) for x in toks[1:6]]
        power_total = [int(x) for x in toks[6:16]]
        typescore_total = [int(x) for x in toks[16:34]]
        seasoning_flavor_total.append(flavor_total)
        seasoning_power_total.append(power_total)
        seasoning_typescore_total.append(typescore_total)
    fh.close()
    seasoning_num = len(seasoning_recipe_list)

    recipeMessage = []
    fh = open('assets/material_combine_'+input_type1+'.txt', 'r')
    for line in fh:
        toks = line.strip().split('\t')
        material_recipe = toks[0].split('|')
        flavor_total = [int(x) for x in toks[1:6]]
        power_total = [int(x) for x in toks[6:16]]
        typescore_total = [int(x) for x in toks[16:34]]
        lv_collection = [False, False]
        for i in range(seasoning_num):
            seasoning_recipe = seasoning_recipe_list[i]
            seasoning_flavor = seasoning_flavor_total[i]
            seasoning_power = seasoning_power_total[i]
            seasoning_typescore = seasoning_typescore_total[i]

            # calculate power
            power1, power2, power3 = recipe2power(seasoning_flavor, flavor_total, seasoning_power, power_total)
            if power1 != input_power1:
                continue
            if input_power2:
                if power2 != input_power2:
                    continue

            # calculate type
            ind_candidate, lv_candidate, type2, type3 = recipe2type(seasoning_typescore, typescore_total, input_type1, input_type2)
            
            # output
            if ind_candidate:
                if lv_collection[lv_candidate-1]:
                    continue
                lv_collection[lv_candidate-1] = True
                total_recipe = material_recipe+seasoning_recipe
                
                mealPower1 = input_power1+':Lv2'+ ' ' + input_type1
                mealPower2 = 'egg_power:Lv'+str(lv_candidate) if power2=='egg_power' else power2+':Lv'+str(lv_candidate)+' '+type2
                mealPower3 = power3+':Lv1'+' ' + type3
                recipeMessage.append('\n'.join([', '.join(total_recipe), mealPower1, mealPower2, mealPower3]) + '\n')
    return('\n'.join(recipeMessage))

def make_recipe_egg(input_type2, input_power2):
    fh = open('assets/seasoning_combine.txt', 'r')
    seasoning_recipe_list = []
    seasoning_flavor_total = []
    seasoning_power_total = []
    seasoning_typescore_total = []
    for line in fh:
        toks = line.strip().split('\t')
        seasoning_recipe = toks[0].split('|')
        seasoning_recipe_list.append(seasoning_recipe)
        flavor_total = [int(x) for x in toks[1:6]]
        power_total = [int(x) for x in toks[6:16]]
        typescore_total = [int(x) for x in toks[16:34]]
        seasoning_flavor_total.append(flavor_total)
        seasoning_power_total.append(power_total)
        seasoning_typescore_total.append(typescore_total)
    fh.close()
    seasoning_num = len(seasoning_recipe_list)

    recipeMessage = []
    for input_type1 in type_list:

        fh = open('assets/material_combine_'+input_type1+'.txt', 'r')
        for line in fh:
            toks = line.strip().split('\t')
            material_recipe = toks[0].split('|')
            flavor_total = [int(x) for x in toks[1:6]]
            power_total = [int(x) for x in toks[6:16]]
            typescore_total = [int(x) for x in toks[16:34]]
            typescore = np.array(typescore_total, dtype=int)
            index_sort = np.argsort(-typescore, kind='mergesort')
            if typescore[index_sort[2]] < 180:
                continue

            lv_collection = False
            for i in range(seasoning_num):
                seasoning_recipe = seasoning_recipe_list[i]
                seasoning_flavor = seasoning_flavor_total[i]
                seasoning_power = seasoning_power_total[i]
                seasoning_typescore = seasoning_typescore_total[i]

                # calculate power
                power1, power2, power3 = recipe2power(seasoning_flavor, flavor_total, seasoning_power, power_total)
                if power2 != input_power2:
                    continue

                # calculate type
                ind_candidate, lv_candidate, type2, type3 = recipe2type(seasoning_typescore, typescore_total, input_type1, input_type2)
                
                # output
                if ind_candidate:
                    if lv_collection:
                        continue
                    lv_collection = True
                    total_recipe = material_recipe+seasoning_recipe
                    
                    mealPower1 = 'egg_power:Lv2'
                    mealPower2 = power2+':Lv'+str(lv_candidate)+' '+type2
                    mealPower3 = power3+':Lv1'+' ' + type3  
                    recipeMessage.append('\n'.join([', '.join(total_recipe), mealPower1, mealPower2, mealPower3]) + '\n')
    return('\n'.join(recipeMessage))


import dash
from dash import Dash, dcc, Output, Input, html, State, callback
import dash_bootstrap_components as dbc

type_options = [
{'label': '-', 'value':False},
{'label': 'Normal', 'value':'normal'},
{'label': 'Fighting', 'value':'fighting'},
{'label': 'Flying', 'value':'flying'},
{'label': 'Poison', 'value':'poison'},
{'label': 'Ground', 'value':'ground'},
{'label': 'Rock', 'value':'rock'},
{'label': 'Bug', 'value':'bug'},
{'label': 'Ghost', 'value':'ghost'},
{'label': 'Steel', 'value':'steel'},
{'label': 'Fire', 'value':'fire'},
{'label': 'Water', 'value':'water'},
{'label': 'Electric', 'value':'electric'},
{'label': 'Grass', 'value':'grass'},
{'label': 'Psychic', 'value':'psychic'},
{'label': 'Ice', 'value':'ice'},
{'label': 'Dragon', 'value':'dragon'},
{'label': 'Dark', 'value':'dark'},
{'label': 'Fairy', 'value':'fairy'}
]

power_options = [
{'label': '-', 'value':False},
{'label':'Egg Power', 'value':'egg_power'},
{'label':'Catching Power', 'value':'catching_power'},
{'label':'Exp. Point Power', 'value':'exp_power'},
{'label':'Item Drop Power', 'value':'item_power'},
{'label':'Raid Power', 'value':'raid_power'},
{'label':'Humungo Power', 'value':'humungo_power'},
{'label':'Teensy Power', 'value':'teensy_power'},
{'label':'Encounter power', 'value':'encounter_power'}
]

#app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
dash.register_page(__name__, title='English', order=1)

recipe_loading = dcc.Markdown(children='', style={'white-space': 'pre'})
recipe = dcc.Markdown(children='', style={'white-space': 'pre'})

def layout():
    return html.Div([
#app.layout = html.Div([
        dcc.Markdown('# Lv2 Sandwich Designer', style={'textAlign':'center'}),
        dcc.Markdown('Before you start, here\'s one tip:\n'
            'In single player mode, it\'s impossible to get a type boost larger than 280 without Herba Mystica.\n'
            'We are not using Herba Mystica here, so I cannot design a recipe with multiple meal powers for the same type.\n',
            style={'textAlign': 'center', 'white-space': 'pre'}),

        dcc.Markdown('### Let\'s Start Now', style={'textAlign': 'center'}),
        html.Hr(),
        dbc.Row([
            dbc.Col([
                dcc.Markdown('Type for meal power 1'),
                dcc.Dropdown(id = 'type1', options = type_options, value=type_list[15]),
                html.Br(),
                dcc.Markdown('Meal power 1'),
                dcc.Dropdown(id = 'power1', options = power_options[1:], value=power_list[5])
                ], width=3),
            dbc.Col([
                dcc.Markdown('Type for meal power 2'),
                dcc.Dropdown(id = 'type2', options = type_options, value=type_list[16]),
                html.Br(),
                dcc.Markdown('Meal power 2'),
                dcc.Dropdown(id = 'power2', options = power_options, value=power_list[6])
                ], width=3)
        ], justify='center'),

        dbc.Row([
            dbc.Col([
                html.Br(),
                dbc.Button('Submit', id='submit_button', className="d-grid gap-2 col-6 mx-auto"),
                html.Br(),
                dcc.Markdown('Tips for EGG POWER:\n'
                    'If meal power 1 is not EGG POWER, please do select a type for it!\n'
                    'If you need EGG POWER, I suggest put it in Meal power 2, so that it would be much faster.\n'
                    'Type is not important for EGG POWER. It will be ignored no matter selected or not.',
                    style={'white-space': 'pre'})
                ], width=6)
        ], justify='center'),

        dcc.Markdown('### Here Are Some Recipes', style={'textAlign': 'center'}),
        html.Hr(),
        dbc.Row([
            dbc.Col([
                html.Br(),
                dcc.Loading(id='loading_recipe', children=[recipe_loading], type='default'),
                html.Br(),
                recipe
            ], width=6)
        ], justify='center')

])

@callback(
#@app.callback(
    Output(recipe, component_property='children'),
    Output(recipe_loading, component_property='children'),
    [Input('submit_button', component_property = 'n_clicks')],
    [State('type1', component_property='value'), 
    State('power1', component_property='value'),
    State('type2', component_property='value'),
    State('power2', component_property='value')],
    prevent_initial_calls = True
)
def make_recipe(submit, input_type1, input_power1, input_type2, input_power2):
    if input_type1==input_type2:
        return('Sorry, it\'s impossible to get such a recipe without Herba Mystica :(', '')
    if input_power1==input_power2:
        return('Meal powers should be different. Try selecting a different power!', '')

    if input_power1 != 'egg_power':
        if not input_type1:
            return('Please specify the type for meal power 1!', '')
        if input_power2 == 'egg_power':
            input_type2 = False
        recipeMessage = make_recipe_power(input_type1, input_type2, input_power1, input_power2)
    else:
        if not input_power2:
            input_power2 = 'encounter_power'
        recipeMessage = make_recipe_egg(args.type2, input_power2)
    if len(recipeMessage.strip())==0:
        recipeMessage = 'Oops, no recipe is found.\nTry removing some restriction for Meal power 2 to see what are available.'
    return(recipeMessage, '')

# Run app
if __name__=='__main__':
    app.run_server()

