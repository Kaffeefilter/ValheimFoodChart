import json
from itertools import combinations
from tabulate import tabulate
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import PySimpleGUI as sg
import matplotlib
matplotlib.use('TkAgg')


def sortFoodKey(food, healthweight = 100, staminaweight = 100, tickweight = 1):
    #baseline wolf jerky: hp = 33, stamina = 33, hpptick = 3 => hp == stamina == hpptick * 11
    health_weighted = (food[0]['health'] + food[1]['health'] + food[2]['health']) * healthweight
    stamina_weighted = (food[0]['stamina'] + food[1]['stamina'] + food[2]['stamina']) * staminaweight 
    hpptick_weighted = (food[0]['hp/tick'] + food[1]['hp/tick'] + food[2]['hp/tick']) * 11 * tickweight
    return health_weighted + stamina_weighted + hpptick_weighted
    

def generateGraph(foods, n = 5, healthweight = 100, staminaweight = 100, tickweight = 1):

    combinedFood = []
    for foodcomb in combinations(foods, 3):
        combinedFood.append([foodcomb[0], foodcomb[1], foodcomb[2]])

    combinedFood.sort(key=lambda x: sortFoodKey(x, healthweight, staminaweight, tickweight), reverse=True)
    #print(tabulate(combinedFood[:10]))

    hpBars1 = [combination[0]['health'] for combination in combinedFood][:n]
    hpBars2 = [combination[1]['health'] for combination in combinedFood][:n]
    hpBars3 = [combination[2]['health'] for combination in combinedFood][:n]
    # Heights of bars1 + bars2
    hpBars = np.add(hpBars1, hpBars2).tolist()

    staBars1 = [combination[0]['stamina'] for combination in combinedFood][:n]
    staBars2 = [combination[1]['stamina'] for combination in combinedFood][:n]
    staBars3 = [combination[2]['stamina'] for combination in combinedFood][:n]
    staBars = np.add(staBars1, staBars2).tolist()

    tickBars1 = [combination[0]['hp/tick'] for combination in combinedFood][:n]
    tickBars2 = [combination[1]['hp/tick'] for combination in combinedFood][:n]
    tickBars3 = [combination[2]['hp/tick'] for combination in combinedFood][:n]
    tickBars = np.add(tickBars1, tickBars2).tolist()

    """ names = []
    for combination in combinedFood[:n]:
        names.append(f"{combination[0]['name']} + {combination[1]['name']} + {combination[2]['name']}") """
    numbers = list(range(1, n+1))

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

    plt.xticks(r2, numbers)

    return (plt.gcf(), combinedFood[:n])


def drawFigure(canvas, figure):
    figure_canvas_agg = FigureCanvasTkAgg(figure, canvas)
    figure_canvas_agg.draw()
    figure_canvas_agg.get_tk_widget().pack(side='top', fill='both', expand=1)
    return figure_canvas_agg


def createCell(key, i):
    return sg.Text(text=f"{i if key == 'NUM' else ''}", key=f"_TABLE_{key}_{i}_")
    #return sg.Text(text=f"{i if key == 'NUM' else f'_TABLE_{key}_{i}_'}", key=f"_TABLE_{key}_{i}_")


def updateGraph(window, foods, n = 5, healthweight = 100, staminaweight = 100, healingweight = 1):
    graph, combinedFood = generateGraph(foods, n, healthweight, staminaweight, healingweight)

    for i in range(1, 21):
        for key in ('NUM', 'NAME', 'HEALTH', 'STAMINA', 'HEALING'):
            window[f'_TABLE_{key}_{i}_'].update("")
            if(i <= n):
                match key:
                    case 'NUM':
                        window[f'_TABLE_{key}_{i}_'].update(i)
                    case 'NAME':
                        window[f'_TABLE_{key}_{i}_'].update(f"{combinedFood[i-1][0]['name']} + {combinedFood[i-1][1]['name']} + {combinedFood[i-1][2]['name']}")
                    case 'HEALTH':
                        window[f'_TABLE_{key}_{i}_'].update(combinedFood[i-1][0]['health'] + combinedFood[i-1][1]['health'] + combinedFood[i-1][2]['health'])
                    case 'STAMINA':
                        window[f'_TABLE_{key}_{i}_'].update(combinedFood[i-1][0]['stamina'] + combinedFood[i-1][1]['stamina'] + combinedFood[i-1][2]['stamina'])
                    case 'HEALING':
                        window[f'_TABLE_{key}_{i}_'].update(combinedFood[i-1][0]['hp/tick'] + combinedFood[i-1][1]['hp/tick'] + combinedFood[i-1][2]['hp/tick'])
    return graph

def delete_figure_agg(figure_agg):
    figure_agg.get_tk_widget().forget()
    plt.close('all')


def main():
    with open("food.json") as f:
        foods = json.load(f)
    
    #graph = generateGraph(foods)

    table = [ [sg.Text(text="#"), sg.Text(text="Name"), sg.Text(text="HP"), sg.Text(text="Stamina"), sg.Text(text="Healing")] ]
    #table += [ [sg.Text(text=f"{i}", key=f"_TABLE_NUM_{i}_"), sg.Text(key=f"_TABLE_NAME_{i}_"), sg.Text(key=f"_TABLE_HEALTH_{i}_"), sg.Text(key=f"_TABLE_STAMINA_{i}_"), sg.Text(key=f"_TABLE_HEALING_{i}_")] for i in range(1, 21)]
    #table += [ [createCell(key, i) for i in range(1, 21) for key in ('NUM', 'NAME', 'HEALTH', 'STAMINA', 'HEALING')] ]
    table += [ [createCell(key, i) for key in ('NUM', 'NAME', 'HEALTH', 'STAMINA', 'HEALING')] for i in range(1, 21) ]

    canvas = sg.Canvas(key='_CANVAS_', size=(640, 480))
    cb_meadows = sg.Checkbox(key='_CBMEADOWS_', text='Meadows', default=True)
    cb_blackforest = sg.Checkbox(key='_CBBLACKFOREST_', text='Black Forest', default=True)
    cb_swamp = sg.Checkbox(key='_CBSWAMP_', text='Swamp', default=True)
    cb_mountain = sg.Checkbox(key='_CBMOUNTAIN_', text='Mountain', default=True)
    cb_plains = sg.Checkbox(key='_CBPLAIN_', text='Plains', default=True)
    cb_ocean = sg.Checkbox(key='_CBOCEAN_', text='Ocean', default=True)

    text_slider_left = sg.Text(text="Health")
    text_slider_middle = sg.Text(text="1.00:1.00", key="_TEXT_SLIDER_")
    text_slider_right = sg.Text(text="Stamina")
    text_number = sg.Text(key='_TEXT_NUMBER_', text="Anzahl 5")

    slider_preference = sg.Slider(key="_SLIDER_PREFERENCE_", range=(0, 180), default_value=90, orientation='horizontal', disable_number_display=True, enable_events=True)
    cb_healing = sg.Checkbox(key='_CBHEALING_', text="Healing", enable_events=True)
    slider_elements = sg.Slider(key="_SLIDER_ELEMENTS_", range=(1, 20), default_value=5, orientation='horizontal', disable_number_display=True, enable_events=True)

    layout_preference = [
        [text_slider_left, text_slider_middle, text_slider_right],
        [slider_preference, cb_healing]
    ]

    layout_element_numbers = [
        [text_number],
        [slider_elements]
    ]

    layout = [
        [sg.Column([
            [canvas],
            [cb_meadows, cb_blackforest, cb_swamp, cb_mountain, cb_plains, cb_ocean],
            [sg.Column(layout_preference), sg.Column(layout_element_numbers)],
            [sg.Button('Update'), sg.Button('Reset')]
        ]), sg.Column(table, vertical_alignment='top')]
    ]

    window = sg.Window("Vallheim Foods", layout, finalize=True)

    graph = updateGraph(window, foods)
    fig_canvas_agg = drawFigure(window['_CANVAS_'].TKCanvas, graph)

    healthweight = 100
    staminaweight = 100
    healingweight = 1
    numbers = 5

    running = True
    while running:
        event, values = window.read()
        #print(event)

        match event:
            case sg.WIN_CLOSED:
                running = False
                #break      #would work but coud be mistaken for switch case break
            case "Update":
                graph = updateGraph(window, foods, int(numbers), healthweight, staminaweight, healingweight)
                delete_figure_agg(fig_canvas_agg)
                fig_canvas_agg = drawFigure(window['_CANVAS_'].TKCanvas, graph)
            case "Reset":
                window['_TEXT_SLIDER_'].update("1.00:1.00")
                window['_SLIDER_PREFERENCE_'].update(90)
                window['_SLIDER_ELEMENTS_'].update(5)
                window['_TEXT_NUMBER_'].update("Anzahl 5")
                window['_CBHEALING_'].update(False)
                window['_CBMEADOWS_'].update(True)
                window['_CBBLACKFOREST_'].update(True)
                window['_CBSWAMP_'].update(True)
                window['_CBMOUNTAIN_'].update(True)
                window['_CBPLAIN_'].update(True)
                window['_CBOCEAN_'].update(True)
                healthweight = 100
                staminaweight = 100
                healingweight = 1
                numbers = 5
            case "_SLIDER_PREFERENCE_":
                slider_value = values['_SLIDER_PREFERENCE_'] + 10
                healthweight = 1 if slider_value > 100 else slider_value / 100
                staminaweight = 1 if slider_value < 100 else (100 - (slider_value - 100)) / 100
                window['_TEXT_SLIDER_'].update(f"{healthweight:.2f}:{staminaweight:.2f}")
            case "_SLIDER_ELEMENTS_":
                window['_TEXT_NUMBER_'].update(f"Anzahl {values['_SLIDER_ELEMENTS_']:n}")
                numbers = values['_SLIDER_ELEMENTS_']
            case "_CBHEALING_":
                healingweight = 50 if values['_CBHEALING_'] else 1

    window.close()




if __name__ == '__main__':
    main()