#stage2
#implement function that determines highest score(not counting gap) given a input weight
#change function to take the gap into account,kind of like a adjustment factor
#add in combinations, see how that changes answers
#stage 3
#add in invalid combinations

from pulp import LpMaximize, LpProblem, LpVariable
import stage1 
from itertools import combinations
#assign stage1 variable as new var
gear_data = stage1.gear_data

# Create a linear programming problem
problem = LpProblem("SurvivalAndCombatMaximization", LpMaximize)

# Get the user's input for the maximum weight constraint
max_weight = float(input("Enter the maximum weight constraint: "))

# Define variables for each item (0 or 1 indicating whether to select the item)
item_vars = LpVariable.dicts("Item", gear_data.keys(), 0, 1, cat = "Binary")

# Define the objective function to maximize the combined combat and survival scores
problem += sum((gear_data[item_name]['CombatUsefulness'] + gear_data[item_name]['SurvivalUsefulness']) * item_vars[item_name] for item_name in gear_data.keys()), "Combined Score"

# Define the weight constraint
problem += sum(gear_data[item_name]['Weight'] * item_vars[item_name] for item_name in gear_data.keys()) <= max_weight, "Weight Constraint"

# Solve the linear programming problem
problem.solve()

# Extract the selected items
selected_items = [item for item, var in item_vars.items() if var.varValue == 1]


# Define the number of top combinations to print
top_combinations_to_print = 5

# Generate and evaluate combinations of items
combinations_list = []
for r in range(1, len(selected_items) + 1):
    for combo in combinations(selected_items, r):
        total_weight = sum(gear_data[item]['Weight'] for item in combo)
        if total_weight <= max_weight:
            # Calculate the combined score for the combination
            combined_score = sum(gear_data[item]['CombatUsefulness'] + gear_data[item]['SurvivalUsefulness'] for item in combo)
            combinations_list.append((combo, total_weight, combined_score))

# Sort the combinations by combined score 
combinations_list.sort(key=lambda x: x[2], reverse=True)

total_combo_list = []
combo_1 = []
for i, (combo, total_weight, combined_score) in enumerate(combinations_list[:top_combinations_to_print]):
    for item in combo:
        total_combo_list.append(item)
    total_combo_list.append(' ')

sublists = []
current_sublist = []

for item in total_combo_list:
    if item == ' ':
        if current_sublist:  # Check if the sublist is not empty
            sublists.append(current_sublist)
        current_sublist = []  # Start a new sublist
    else:
        current_sublist.append(item)

# Add the last sublist (if not empty)
if current_sublist:
    sublists.append(current_sublist)

combo_1= sublists[0]
combo_2 = sublists[1]
combo_3 = sublists[2]
combo_4 = sublists[3]
combo_5 = sublists[4]

temp_gap = 1000
min_gap = 1000
gap_index = 0
for i in range(0,4):
    for object_name in sublists[i]:
        total_survival_score = 0
        total_combat_score = 0
        gap = 0
        total_survival_score += gear_data[object_name]['SurvivalUsefulness']
        total_combat_score += gear_data[object_name]['CombatUsefulness']
        gap = abs(total_combat_score-total_survival_score)
        if gap < min_gap:
            min_gap = gap
            gap_index = i

print("The optimal combo is " , sublists[gap_index])
