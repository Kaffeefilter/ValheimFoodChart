import json
from itertools import combinations
from tabulate import tabulate
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd


def sortFoodKey(food, healthweight = 5, staminaweight = 5, tickweight = 1):
    #baseline wolf jerky: hp = 33, stamina = 33, hpptick = 3 => hp == stamina == hpptick * 11
    health_weighted = (food[0]['health']+ food[1]['health'] + food[2]['health']) * healthweight
    stamina_weighted = (food[0]['stamina']+ food[1]['stamina'] + food[2]['stamina']) * staminaweight 
    hpptick_weighted = (food[0]['hp/tick']+ food[1]['hp/tick'] + food[2]['hp/tick']) * 11 * tickweight
    return health_weighted + stamina_weighted + hpptick_weighted
    

def main():
    with open("food.json") as f:
        foods = json.load(f)
    
    combinedFood = []
    healthweight = 10
    staminaweight = 1
    tickweight = 10
    
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

    tickBars1 = [combination[0]['hp/tick'] for combination in combinedFood][:5]
    tickBars2 = [combination[1]['hp/tick'] for combination in combinedFood][:5]
    tickBars3 = [combination[2]['hp/tick'] for combination in combinedFood][:5]

    barWidth = 0.25

    r1 = np.arange(len(hpBars1))

    plt.bar(r1, hpBars1, color='#7f6d5f', edgecolor='white', width=barWidth)
    plt.bar(r1, hpBars2, bottom=hpBars1, color='#557f2d', edgecolor='white', width=barWidth)
    plt.bar(r1, hpBars3, bottom=hpBars, color='#2d7f5e', edgecolor='white', width=barWidth)

    plt.show()



if __name__ == '__main__':
    main()