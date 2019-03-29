conversion_lexicon = {
    'lb': 0.45,
    'ft': 0.3,
    "'": 0.3,
    '"': 0.00393700787,
    'in': 0.00393700787
}


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
    print(tokens)
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