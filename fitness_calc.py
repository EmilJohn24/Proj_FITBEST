conversion_lexicon = {
    'kg': 1,
    'm': 1,
    'cm': 0.01,
    'lb': 0.45,
    'ft': 0.3,
    "'": 0.3,
    '"': 0.00393700787,
    'in': 0.00393700787
}


def kilo_to_calorie(weight):
    """
        Important calculations:
            https://www.mayoclinic.org/healthy-lifestyle/weight-loss/in-depth/calories/art-20048065
            3500 calories per 0.45 kg
    """
    return weight * (3500 / 0.45)


def lexical_metric_conversion(value: str):
    tokens = []
    running_digit = ""
    running_unit = ""
    # Split value to token
    for c in value:
        if c.isdigit() or c == '.':
            running_digit += c
            if len(running_unit) > 0:
                tokens.append(running_unit)
                running_unit = ""
        else:
            running_unit += c
            if len(running_digit) > 0:
                tokens.append(float(running_digit))
                running_digit = ""
    tokens.append(running_unit)
    for index, token in enumerate(tokens):
        if isinstance(token, str):
            tokens[index - 1] *= conversion_lexicon[token]
            del tokens[index]
    return str(sum(tokens))


def calculate_bmi(weight, height):
    height = float(height)
    weight = float(weight)
    return weight / height ** 2


def calculate_bmr(weight, height, sex, age):
    height = float(height)
    weight = float(weight)
    age = int(age)
    if sex == 'M':
        bmr = (10 * weight) + (6.25 * height) - (5 * age) + 5
    elif sex == 'F':
        bmr = (10 * weight) + (6.25 * height) - (5 * age) - 161
    else:
        raise ValueError("Invalid sex")
    return bmr


def max_calories_per_day(days, bmr, initial_weight, final_weight):
    """
        Returns the maximum number of consumable calories per day to attain
        final weight within the number of days required

        Notes:
            BMR refers to the amount of calories a person naturally losses per day
    """
    delta_weight = final_weight - initial_weight
    req_calorie_loss = kilo_to_calorie(delta_weight) / days # disregarding BMR
    return bmr - req_calorie_loss

