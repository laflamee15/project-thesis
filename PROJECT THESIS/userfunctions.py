def validate_age_input(new_value: str) -> bool:
    if new_value == "":
        return True
    if new_value.isdigit() and len(new_value) <= 2:
        return True
    return False


def validate_weight_input(new_value: str) -> bool:
    if new_value == "":
        return True
    if new_value.isdigit() and len(new_value) <= 3:
        return True
    return False


def validate_name_input(new_value: str) -> bool:
    
    if new_value == "":
        return True  # Allow empty string (user can delete)
    # Check if all characters are letters or spaces
    if all(char.isalpha() or char.isspace() for char in new_value):
        return True
    return False


def calculate_protein(food_data: dict, food: str, amount: float) -> float:
    protein_per_100 = food_data.get(food)
    if protein_per_100 is None:
        return 0.0
    protein = protein_per_100 * (amount / 100)
    return round(protein, 2)


def calculate_protein_goal(weight: float, goal: str) -> float:
    goal = goal.upper()
    if goal == "BULKING":
        multiplier = 2.0
    elif goal == "CUTTING":
        multiplier = 1.8
    else:
        multiplier = 1.6
    return round(weight * multiplier, 2)
