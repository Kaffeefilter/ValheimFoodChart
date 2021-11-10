import json
from itertools import combinations
from tabulate import tabulate
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import PySimpleGUI as sg
import matplotlib
matplotlib.use('TkAgg')


def sortFoodKey(food, healthweight = 5, staminaweight = 5, tickweight = 1):
    #baseline wolf jerky: hp = 33, stamina = 33, hpptick = 3 => hp == stamina == hpptick * 11
    health_weighted = (food[0]['health']+ food[1]['health'] + food[2]['health']) * healthweight
    stamina_weighted = (food[0]['stamina']+ food[1]['stamina'] + food[2]['stamina']) * staminaweight 
    hpptick_weighted = (food[0]['hp/tick']+ food[1]['hp/tick'] + food[2]['hp/tick']) * 11 * tickweight
    return health_weighted + stamina_weighted + hpptick_weighted
    

def generateGraph(foods, n = 5, healthweight = 1, staminaweight = 1, tickweight = 1):

    combinedFood = []

    for foodcomb in combinations(foods, 3):
        combinedFood.append([foodcomb[0], foodcomb[1], foodcomb[2]])

    combinedFood.sort(key=lambda x: sortFoodKey(x, healthweight, staminaweight, tickweight), reverse=True)
    #print(tabulate(combinedFood[:10]))

    hpBars1 = [combination[0]['health'] for combination in combinedFood][:5]
    hpBars2 = [combination[1]['health'] for combination in combinedFood][:5]
    hpBars3 = [combination[2]['health'] for combination in combinedFood][:5]
    # Heights of bars1 + bars2
    hpBars = np.add(hpBars1, hpBars2).tolist()

    staBars1 = [combination[0]['stamina'] for combination in combinedFood][:5]
    staBars2 = [combination[1]['stamina'] for combination in combinedFood][:5]
    staBars3 = [combination[2]['stamina'] for combination in combinedFood][:5]
    staBars = np.add(staBars1, staBars2).tolist()

    tickBars1 = [combination[0]['hp/tick'] for combination in combinedFood][:5]
    tickBars2 = [combination[1]['hp/tick'] for combination in combinedFood][:5]
    tickBars3 = [combination[2]['hp/tick'] for combination in combinedFood][:5]
    tickBars = np.add(tickBars1, tickBars2).tolist()

    names = []
    for combination in combinedFood[:5]:
        names.append(f"{combination[0]['name']} + {combination[1]['name']} + {combination[2]['name']}")

    barWidth = 0.25

    r1 = np.arange(len(hpBars1))
    r2 = [x + barWidth for x in r1]
    r3 = [x + barWidth for x in r2]

    plt.bar(r1, hpBars1, color='#7f6d5f', edgecolor='white', width=barWidth)
    plt.bar(r1, hpBars2, bottom=hpBars1, color='#557f2d', edgecolor='white', width=barWidth)
    plt.bar(r1, hpBars3, bottom=hpBars, color='#2d7f5e', edgecolor='white', width=barWidth)

    plt.bar(r2, staBars1, color='#7f6d5f', width=barWidth, edgecolor='white')
    plt.bar(r2, staBars2, bottom=staBars1, color='#557f2d', width=barWidth, edgecolor='white')
    plt.bar(r2, staBars3, bottom=staBars, color='#2d7f5e', width=barWidth, edgecolor='white')

    plt.bar(r3, tickBars1, color='#7f6d5f', width=barWidth, edgecolor='white')
    plt.bar(r3, tickBars2, bottom=tickBars1, color='#557f2d', width=barWidth, edgecolor='white')
    plt.bar(r3, tickBars3, bottom=tickBars, color='#2d7f5e', width=barWidth, edgecolor='white')

    plt.xticks(r2, names, rotation='vertical')

    return plt.gcf()


def drawFigure(canvas, figure):
    figure_canvas_agg = FigureCanvasTkAgg(figure, canvas)
    figure_canvas_agg.draw()
    figure_canvas_agg.get_tk_widget().pack(side='top', fill='both', expand=1)
    return figure_canvas_agg


def main():
    with open("food.json") as f:
        foods = json.load(f)
    
    graph = generateGraph(foods)

    layout = [
        [sg.Canvas(key='CANVAS')],
        [sg.Button('Ok')]
    ]

    window = sg.Window("Vallheim Foods", layout, finalize=True)

    drawFigure(window['CANVAS'].TKCanvas, graph)

    event, values = window.read()
    window.close()
    



if __name__ == '__main__':
    main()