def search_food(query:str):
    food_dict = load_food()
    results = []
    query = query.lower().strip()
    for item in food_dict.keys():
        item = item.lower().strip()
        if not item.find(query) == -1:
            results.append(item)
    return results
    

def calorie_parser(calorie: str):
    calorie = calorie.strip()
    explorer = calorie.__iter__()
    current_char = next(explorer)
    calorie_count = ''
    unit_calorie = ''
    while current_char.isdigit():
        calorie_count += current_char
        current_char = next(explorer)
    try:
        while not current_char == '(':
            current_char = next(explorer)

        while not current_char == ')':
            unit_calorie += current_char
            current_char = next(explorer)
    except StopIteration:
        unit_calorie = "100 g"
    return int(calorie_count), unit_calorie.lstrip('(')




_food_cache = dict()

def load_food():
    global _food_cache
    if len(_food_cache) == 0:
        with open('food.csv', 'r') as food:
            food_base = food.readlines()
        food_dict = {}
        mode_read = False
        mode = ""
        for line in food_base:
            line = line.strip('\n')
            if line == '--':
                mode_read = True
            elif mode_read:
                mode = line
                mode_read = False
            elif not line == '':
                cols = line.split(',')
                new_food = dict()
                new_food["Unit Calorie"], new_food["Unit"] = calorie_parser(cols[1])
                new_food["Status"] = cols[3]
                new_food["Mode"] = mode
                name = cols[0]
                food_dict[name] = new_food
        _food_cache = food_dict
    # Load cache if not empty
    else:
        food_dict = _food_cache
        
    return food_dict

