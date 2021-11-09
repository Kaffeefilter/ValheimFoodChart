import json
from itertools import combinations
from tabulate import tabulate

def sortFoodKey(food, healthweight = 5, staminaweight = 5, tickweight = 1):
    #baseline wolf jerky: hp = 33, stamina = 33, hpptick = 3 => hp == stamina == hpptick * 11
    health_weighted = food['health'] * healthweight
    stamina_weighted = food['stamina'] * staminaweight 
    hpptick_weighted = food['hp/tick'] * 11 * tickweight
    return health_weighted + stamina_weighted + hpptick_weighted


def sortFoodKey2(food, healthweight = 5, staminaweight = 5, tickweight = 1):
    #baseline wolf jerky: hp = 33, stamina = 33, hpptick = 3 => hp == stamina == hpptick * 11
    health_weighted = (food[0]['health']+ food[1]['health'] + food[2]['health']) * healthweight
    stamina_weighted = (food[0]['stamina']+ food[1]['stamina'] + food[2]['stamina']) * staminaweight 
    hpptick_weighted = (food[0]['hp/tick']+ food[1]['hp/tick'] + food[2]['hp/tick']) * 11 * tickweight
    return health_weighted + stamina_weighted + hpptick_weighted
    

def main():
    with open("food.json") as f:
        foods = json.load(f)
    
    combinedFood = []
    combinedFood2 = []
    healthweight = 10
    staminaweight = 1
    tickweight = 10
    
    for foodcomb in combinations(foods, 3):
        combinedFood.append({
            "name": f"{foodcomb[0]['name']} + {foodcomb[1]['name']} + {foodcomb[2]['name']}",
            "health": foodcomb[0]['health']+ foodcomb[1]['health'] + foodcomb[2]['health'],
            "stamina": foodcomb[0]['stamina'] + foodcomb[1]['stamina'] + foodcomb[2]['stamina'],
            "hp/tick": foodcomb[0]['hp/tick'] + foodcomb[1]['hp/tick'] + foodcomb[2]['hp/tick']
        })
        combinedFood2.append([foodcomb[0], foodcomb[1], foodcomb[2]])

    combinedFood.sort(key=lambda x: sortFoodKey(x, healthweight, staminaweight, tickweight), reverse=True)
    print(tabulate(combinedFood[:10]))

    combinedFood2.sort(key=lambda x: sortFoodKey2(x, healthweight, staminaweight, tickweight), reverse=True)
    print(tabulate(combinedFood2[:10]))



if __name__ == '__main__':
    main()