conversion_lexicon = {
    'lb': 1/2.2,
    'ft': 0.3,
    "'" : 0.3,
    '"' : 1/254,
    'in': 1/254
}


def lexical_metric_conversion(value: str):
    result = 0
    tokens = []
    running_digit = ""
    running_unit = ""
    # Split value to token
    for c in value:
        if c.isdigit() or c == '.':
            running_digit += c
            if len(running_unit) > 0:
                tokens.append(running_unit)
        else:
            running_unit += c
            if len(running_digit) > 0:
                tokens.append(float(running_digit))

    for index, token in enumerate(tokens):
        if isinstance(token, str):
            tokens[index - 1] *= conversion_lexicon[token]
    return ''.join(tokens)


def calculate_bmi(weight, height):
    height = float(height)
    weight = float(weight)
    return weight / height ** 2


def calculate_bmr(weight, height, sex, age):
    height = float(height)
    weight = float(weight)
    age = int(age)
    if sex == 'M':
        BMR = (10 * weight) + (6.25 * height) - (5 * age) + 5
    elif sex == 'F':
        BMR = (10 * weight) + (6.25 * height) - (5 * age) - 161
    else:
        raise ValueError("Invalid sex")
    return BMR