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
                
                mealPower1 = e2c[input_power1]+':Lv2'+ ' ' + e2c[input_type1]
                mealPower2 = '蛋蛋力:Lv'+str(lv_candidate) if power2=='egg_power' else e2c[power2]+':Lv'+str(lv_candidate)+' '+e2c[type2]
                mealPower3 = e2c[power3]+':Lv1'+' ' + e2c[type3]
                recipeMessage.append('\n'.join([', '.join([e2c[x] for x in total_recipe]), mealPower1, mealPower2, mealPower3]) + '\n')
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
                    
                    mealPower1 = '蛋蛋力:Lv2'
                    mealPower2 = e2c[power2]+':Lv'+str(lv_candidate)+' '+e2c[type2]
                    mealPower3 = e2c[power3]+':Lv1'+' ' + e2c[type3] 
                    recipeMessage.append('\n'.join([', '.join([e2c[x] for x in total_recipe]), mealPower1, mealPower2, mealPower3]) + '\n')
    return('\n'.join(recipeMessage))


import dash
from dash import Dash, dcc, Output, Input, html, State, callback
import dash_bootstrap_components as dbc

type_options = [
{'label': '-', 'value':False},
{'label': '一般', 'value':'normal'},
{'label': '格斗', 'value':'fighting'},
{'label': '飞行', 'value':'flying'},
{'label': '毒', 'value':'poison'},
{'label': '地面', 'value':'ground'},
{'label': '岩石', 'value':'rock'},
{'label': '虫', 'value':'bug'},
{'label': '幽灵', 'value':'ghost'},
{'label': '钢', 'value':'steel'},
{'label': '火', 'value':'fire'},
{'label': '水', 'value':'water'},
{'label': '电', 'value':'electric'},
{'label': '草', 'value':'grass'},
{'label': '超能', 'value':'psychic'},
{'label': '冰', 'value':'ice'},
{'label': '龙', 'value':'dragon'},
{'label': '恶', 'value':'dark'},
{'label': '妖精', 'value':'fairy'}
]

power_options = [
{'label': '-', 'value':False},
{'label':'蛋蛋力', 'value':'egg_power'},
{'label':'捕获力', 'value':'catching_power'},
{'label':'经验力', 'value':'exp_power'},
{'label':'掉物力', 'value':'item_power'},
{'label':'团战力', 'value':'raid_power'},
{'label':'大大力', 'value':'humungo_power'},
{'label':'小小力', 'value':'teensy_power'},
{'label':'遭遇力', 'value':'encounter_power'}
]

e2c = {'normal':'一般','fighting':'格斗','flying':'飞行','poison':'毒', 'ground':'地面', 'rock':'岩石',
'bug':'虫', 'ghost':'幽灵', 'steel':'钢', 'fire':'火', 'water':'水', 'electric':'电',
'grass':'草', 'psychic':'超能', 'ice':'冰', 'dragon':'龙', 'dark':'恶', 'fairy':'妖精',
'egg_power':'蛋蛋力', 'catching_power':'捕获力', 'exp_power':'经验力', 'item_power':'掉物力',
'raid_power':'团战力', 'humungo_power':'大大力', 'teensy_power':'小小力', 'encounter_power':'遭遇力',
'basil':'罗勒', 'watercress':'豆瓣菜', 'tofu':'豆腐', 'red_bell_peper':'红椒片', 'cucumber':'小黄瓜片', 
'yellow_bell_pepper':'黄椒片', 'lettuce':'生菜', 'klawf_stick':'毛崖蟹棒', 'pickle':'酸黄瓜片', 
'green_bell_pepper':'青椒片', 'ham':'火腿片', 'proscuitto':'生火腿', 'onion':'洋葱片', 
'cherry_tomatoes':'小番茄块', 'bacon':'煎培根', 'red_onion':'红洋葱', 'avocado':'牛油果', 
'smoked_fillet':'烟熏鱼片', 'tomato':'番茄片', 'cheese':'芝士片', 'banana':'香蕉片', 
'strawberry':'草莓片', 'apple':'苹果片', 'kiwi':'奇异果片', 'jalapelo':'小辣椒', 'pineapple':'凤梨片', 
'chorizo':'煎辣香肠', 'herbed_sausage':'香草香肠', 'egg':'水煮蛋片', 'hamburger':'汉堡排', 
'potato_tortilla':'烘蛋', 'fired_fillet':'炸鱼片', 'potato_salad':'土豆沙拉', 'noddles':'面条', 'rice':'米饭', 
'wasabi':'芥末酱', 'horseradish':'辣根', 'curry_powder':'咖喱粉', 'mayonnaise':'蛋黄酱', 'ketchup':'番茄酱',
'mustard':'黄芥末酱', 'salt':'盐', 'pepper':'胡椒', 'butter':'黄油', 'yogurt':'酸奶', 'peanut_butter':'花生酱', 
'chili_sause':'辣酱','cream_cheese':'黄油芝士', 'jam':'莓果酱', 'olive_oil':'橄榄油', 'whipped_cream':'鲜奶油', 
'marmalade':'橘子酱', 'vinegar':'醋'}


#app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
dash.register_page(__name__, path='/', title='中文', order=0)

recipe_loading = dcc.Markdown(children='', style={'white-space': 'pre'})
recipe = dcc.Markdown(children='', style={'white-space': 'pre'})

def layout():
    return html.Div([
#app.layout = html.Div([
        dcc.Markdown('# Lv2 三明治设计室', style={'textAlign':'center'}),
        dcc.Markdown('嗨！你好呀！\n'
            '我会尽我所能依要求设计单人模式食谱（无秘传调味料），第一食力为2，\n'
            '第二食力为2或1，各食力对应属性必不相同（如果想要做出多种食力对应同\n'
            '一属性的三明治，需要单属性数值超过280，单人无秘传调味料无法完成）。',
            style={'textAlign': 'center', 'white-space': 'pre'}),

        dcc.Markdown('### 请选择属性和食力', style={'textAlign': 'center'}),
        html.Hr(),
        dbc.Row([
            dbc.Col([
                dcc.Markdown('第一食力属性'),
                dcc.Dropdown(id = 'type1', options = type_options, value=type_list[15]),
                html.Br(),
                dcc.Markdown('第一食力'),
                dcc.Dropdown(id = 'power1', options = power_options[1:], value=power_list[5])
                ], width=3),
            dbc.Col([
                dcc.Markdown('第二食力属性'),
                dcc.Dropdown(id = 'type2', options = type_options, value=type_list[16]),
                html.Br(),
                dcc.Markdown('第二食力'),
                dcc.Dropdown(id = 'power2', options = power_options, value=power_list[6])
                ], width=3)
        ], justify='center'),

        dbc.Row([
            dbc.Col([
                html.Br(),
                dbc.Button('提交', id='submit_button', className="d-grid gap-2 col-6 mx-auto"),
                html.Br(),
                dcc.Markdown('关于蛋蛋力:\n'
                    '如果第一食力非蛋蛋力，别忘记选择第一食力的属性。\n'
                    '如果需要蛋蛋力，建议将其作为第二食力。\n'
                    '因为蛋蛋力不对应属性，所以填不填都没关系哒！',
                    style={'white-space': 'pre'})
                ], width=6)
        ], justify='center'),

        dcc.Markdown('### 可用食谱', style={'textAlign': 'center'}),
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
        return('不用秘传调味料办不到啦！请更换属性。', '')
    if input_power1==input_power2:
        return('两个食力不能相同哦，请更换食力。', '')

    if input_power1 != 'egg_power':
        if not input_type1:
            return('请选择第一食力对应属性!', '')
        if input_power2 == 'egg_power':
            input_type2 = False
        recipeMessage = make_recipe_power(input_type1, input_type2, input_power1, input_power2)
    else:
        if not input_power2:
            input_power2 = 'encounter_power'
        recipeMessage = make_recipe_egg(args.type2, input_power2)
    if len(recipeMessage.strip())==0:
        recipeMessage = '啊哦！没有找到满足要求的食谱，试试放松要求？（如移除第二食力或属性限制）'
    return(recipeMessage, '')

# Run app
if __name__=='__main__':
    app.run_server()

