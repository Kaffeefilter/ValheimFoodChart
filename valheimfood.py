import json
from itertools import combinations
from tabulate import tabulate
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import PySimpleGUI as sg
import matplotlib
matplotlib.use('TkAgg')


def sortFoodKey(food, healthweight = 100, staminaweight = 100, healingweight = 1):
    #baseline wolf jerky: hp = 33, stamina = 33, hpptick = 3 => hp == stamina == hpptick * 11
    health_weighted = (food[0]['health'] + food[1]['health'] + food[2]['health']) * healthweight
    stamina_weighted = (food[0]['stamina'] + food[1]['stamina'] + food[2]['stamina']) * staminaweight 
    hpptick_weighted = (food[0]['healing'] + food[1]['healing'] + food[2]['healing']) * 11 * healingweight
    return health_weighted + stamina_weighted + hpptick_weighted

def biomeKeyToName(key):
    match key:
        case '_CBMEADOWS_':
            return 'Meadows'
        case '_CBBLACKFOREST_':
            return 'Black Forest'
        case '_CBSWAMP_':
            return 'Swamp'
        case '_CBMOUNTAIN_':
            return 'Mountains'
        case '_CBPLAIN_':
            return 'Plains'
        case '_CBOCEAN_':
            return 'Ocean'

def checkHealth(foodcomb, minhealth):
    return (foodcomb[0]['health'] + foodcomb[1]['health'] + foodcomb[2]['health']) >= minhealth

def checkStamina(foodcomb, minstamina):
    return (foodcomb[0]['stamina'] + foodcomb[1]['stamina'] + foodcomb[2]['stamina']) >= minstamina


def generateGraph(foods, n = 5, healthweight = 100, staminaweight = 100, healingweight = 1, biomes = None, minstamina = 0, minhealth = 0):
    if biomes is None or not biomes:
        biomes = ['Meadows', 'Black Forest', 'Swamp', 'Mountains', 'Plains', 'Ocean']
    else:
        biomes = [biomeKeyToName(key) for key in biomes]

    filteredFoods = [food for food in foods if food['biome'] in biomes]

    #combinedFood = []
    #for foodcomb in combinations(filteredFoods, 3):
    #    combinedFood.append([foodcomb[0], foodcomb[1], foodcomb[2]])
    combinedFood = [[foodcomb[0], foodcomb[1], foodcomb[2]] for foodcomb in combinations(filteredFoods, 3) if checkHealth(foodcomb, minhealth) if checkStamina(foodcomb, minstamina)]

    combinedFood.sort(key=lambda x: sortFoodKey(x, healthweight, staminaweight, healingweight), reverse=True)
    #print(tabulate(combinedFood[:10]))

    if(0 < len(combinedFood) < n):
        n = len(combinedFood)
    elif(not combinedFood):
        combinedFood = [[{key: 0 for key in ('name', 'health', 'stamina', 'healing')} for j in range(0, 3)] for i in range(0, n)]
        n = 0

    hpBars1 = [combination[0]['health'] for combination in combinedFood][:n]
    hpBars2 = [combination[1]['health'] for combination in combinedFood][:n]
    hpBars3 = [combination[2]['health'] for combination in combinedFood][:n]
    # Heights of bars1 + bars2
    hpBars = np.add(hpBars1, hpBars2).tolist()

    staBars1 = [combination[0]['stamina'] for combination in combinedFood][:n]
    staBars2 = [combination[1]['stamina'] for combination in combinedFood][:n]
    staBars3 = [combination[2]['stamina'] for combination in combinedFood][:n]
    staBars = np.add(staBars1, staBars2).tolist()

    tickBars1 = [combination[0]['healing'] for combination in combinedFood][:n]
    tickBars2 = [combination[1]['healing'] for combination in combinedFood][:n]
    tickBars3 = [combination[2]['healing'] for combination in combinedFood][:n]
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

    return (plt.gcf(), combinedFood[:n], n)


def drawFigure(canvas, figure):
    figure_canvas_agg = FigureCanvasTkAgg(figure, canvas)
    figure_canvas_agg.draw()
    figure_canvas_agg.get_tk_widget().pack(side='top', fill='both', expand=1)
    return figure_canvas_agg


def createCell(key, i, size):
    return sg.Text(text=f"{i if key == 'NUM' else ''}", key=f"_TABLE_{key}_{i}_", size=size, justification='left')
    #return sg.Text(text=f"{i if key == 'NUM' else f'_TABLE_{key}_{i}_'}", key=f"_TABLE_{key}_{i}_")


def updateGraph(window, foods, n = 5, healthweight = 100, staminaweight = 100, healingweight = 1, biomes = None, minstamina = 0, minhealth = 0):
    graph, combinedFood, n = generateGraph(foods, n, healthweight, staminaweight, healingweight, biomes, minstamina, minhealth)
    if n == 0:
        for i in range(1, 21):
            for key in ('NUM', 'NAME', 'HEALTH', 'STAMINA', 'HEALING'):
                window[f'_TABLE_{key}_{i}_'].update("")
        window['_TABLE_NAME_1_'].update("No Matches found")
        return graph

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
                        window[f'_TABLE_{key}_{i}_'].update(combinedFood[i-1][0]['healing'] + combinedFood[i-1][1]['healing'] + combinedFood[i-1][2]['healing'])
    return graph

def delete_figure_agg(figure_agg):
    figure_agg.get_tk_widget().forget()
    plt.close('all')


def main():
    with open("food.json") as f:
        foods = json.load(f)
    
    #graph = generateGraph(foods)

    sizes = {
        'NUM': 2,
        'NAME': 41,
        'HEALTH': 3,
        'STAMINA': 6,
        'HEALING': 5
    }

    table = [ [ sg.Text(text="#", size=sizes['NUM'], justification='left'), 
                sg.Text(text="Name", size=sizes['NAME'], justification='left'), 
                sg.Text(text="HP", size=sizes['HEALTH'], justification='left'), 
                sg.Text(text="Stamina", size=sizes['STAMINA'], justification='left'), 
                sg.Text(text="Healing", size=sizes['HEALING'], justification='left')] ]
    #table += [ [sg.Text(text=f"{i}", key=f"_TABLE_NUM_{i}_"), sg.Text(key=f"_TABLE_NAME_{i}_"), sg.Text(key=f"_TABLE_HEALTH_{i}_"), sg.Text(key=f"_TABLE_STAMINA_{i}_"), sg.Text(key=f"_TABLE_HEALING_{i}_")] for i in range(1, 21)]
    #table += [ [createCell(key, i) for i in range(1, 21) for key in ('NUM', 'NAME', 'HEALTH', 'STAMINA', 'HEALING')] ]
    table += [ [createCell(key, i, sizes[key]) for key in ('NUM', 'NAME', 'HEALTH', 'STAMINA', 'HEALING')] for i in range(1, 21) ]

    canvas = sg.Canvas(key='_CANVAS_', size=(640, 480))
    cb_meadows = sg.Checkbox(key='_CBMEADOWS_', text='Meadows', default=True)
    cb_blackforest = sg.Checkbox(key='_CBBLACKFOREST_', text='Black Forest', default=True)
    cb_swamp = sg.Checkbox(key='_CBSWAMP_', text='Swamp', default=True)
    cb_mountain = sg.Checkbox(key='_CBMOUNTAIN_', text='Mountain', default=True)
    cb_plains = sg.Checkbox(key='_CBPLAIN_', text='Plains', default=True)
    cb_ocean = sg.Checkbox(key='_CBOCEAN_', text='Ocean', default=True)

    text_slider_left = sg.Text(text="Stamina")
    text_slider_middle = sg.Text(text="1.00:1.00", key="_TEXT_SLIDER_")
    text_slider_right = sg.Text(text="Health")
    text_slider_healing = sg.Text(text="Healing 0", key="_TEXT_HEALING_")
    text_number = sg.Text(key='_TEXT_NUMBER_', text="Anzahl 5")

    slider_preference = sg.Slider(key="_SLIDER_PREFERENCE_", range=(0, 180), default_value=90, orientation='horizontal', disable_number_display=True, enable_events=True)
    #cb_healing = sg.Checkbox(key='_CBHEALING_', text="Healing", enable_events=True)
    slider_healing = sg.Slider(key='_SLIDER_HEALING_', range=(0, 2), default_value=0, orientation='horizontal', size=(5, 20), disable_number_display=True, enable_events=True)
    slider_elements = sg.Slider(key="_SLIDER_ELEMENTS_", range=(1, 20), default_value=5, orientation='horizontal', disable_number_display=True, enable_events=True)

    text_min_stamina = sg.Text(text="min Stamina")
    spin_min_stamina = sg.Spin(values=[i for i in range(1,200)], initial_value=0, size=4, key='_MIN_STAMINA_')
    text_min_health = sg.Text(text="min Health")
    spin_min_health = sg.Spin(values=[i for i in range(1,200)], initial_value=0, size=4, key='_MIN_HEALTH_')

    layout_preference = [
        [text_slider_left, text_slider_middle, text_slider_right, text_slider_healing],
        [slider_preference, slider_healing]
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
            [text_min_stamina, spin_min_stamina, text_min_health, spin_min_health],
            [sg.Button('Update'), sg.Button('Reset'), sg.Button('Size')]
        ]), sg.Column(table, vertical_alignment='top')]
    ]

    window = sg.Window("Vallheim Foods", layout, finalize=True)

    graph = updateGraph(window, foods)
    fig_canvas_agg = drawFigure(window['_CANVAS_'].TKCanvas, graph)

    healthweight = 1
    staminaweight = 1
    healingweight = 0.1
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
                biomes = [key for key, value in values.items() if key in ('_CBMEADOWS_', '_CBBLACKFOREST_', '_CBSWAMP_', '_CBMOUNTAIN_', '_CBPLAIN_', '_CBOCEAN_') if value]
                minstamina = int(values['_MIN_STAMINA_'])
                minhealth = int(values['_MIN_HEALTH_'])
                delete_figure_agg(fig_canvas_agg)
                graph = updateGraph(window, foods, int(numbers), healthweight, staminaweight, healingweight, biomes, minstamina, minhealth)
                fig_canvas_agg = drawFigure(window['_CANVAS_'].TKCanvas, graph)
            case "Reset":
                window['_CBMEADOWS_'].update(True)
                window['_CBBLACKFOREST_'].update(True)
                window['_CBSWAMP_'].update(True)
                window['_CBMOUNTAIN_'].update(True)
                window['_CBPLAIN_'].update(True)
                window['_CBOCEAN_'].update(True)
                window['_TEXT_SLIDER_'].update("1.00:1.00")
                window['_SLIDER_PREFERENCE_'].update(90)
                window['_SLIDER_ELEMENTS_'].update(5)
                window['_TEXT_NUMBER_'].update("Anzahl 5")
                #window['_CBHEALING_'].update(False)
                window['_SLIDER_HEALING_'].update(0)
                window['_TEXT_HEALING_'].update("Healing 0")
                window['_CBMEADOWS_'].update(True)
                window['_CBBLACKFOREST_'].update(True)
                window['_CBSWAMP_'].update(True)
                window['_CBMOUNTAIN_'].update(True)
                window['_CBPLAIN_'].update(True)
                window['_CBOCEAN_'].update(True)
                window['_MIN_STAMINA_'].update('0')
                window['_MIN_HEALTH_'].update('0')
                healthweight = 1
                staminaweight = 1
                healingweight = 0.1
                numbers = 5
            case "_SLIDER_PREFERENCE_":
                slider_value = values['_SLIDER_PREFERENCE_'] + 10
                healthweight = 1 if slider_value > 100 else slider_value / 100
                staminaweight = 1 if slider_value < 100 else (100 - (slider_value - 100)) / 100
                window['_TEXT_SLIDER_'].update(f"{staminaweight:.2f}:{healthweight:.2f}")
            case "_SLIDER_ELEMENTS_":
                window['_TEXT_NUMBER_'].update(f"Anzahl {values['_SLIDER_ELEMENTS_']:n}")
                numbers = values['_SLIDER_ELEMENTS_']
            case "_CBHEALING_":
                healingweight = 0.5 if values['_CBHEALING_'] else 0.1
            case "_SLIDER_HEALING_":
                window['_TEXT_HEALING_'].update(f"Healing {values['_SLIDER_HEALING_']:n}")
                if values['_SLIDER_HEALING_'] == 0:
                    healingweight = 0.1
                elif values['_SLIDER_HEALING_'] == 1:
                    healingweight = 0.5
                else:
                    healingweight = 1
            case 'Size':
                print(window['_TABLE_NAME_14_'].get_size())


    window.close()




if __name__ == '__main__':
    main()