# Vaishnavi Ladda PRN:21610076
assembly = [
    ("trike", "wheel", 3),
    ("trike", "seat", 1),
    ("trike", "pedal", 2),
    ("wheel", "rim", 1),
    ("wheel", "tube", 1),
    ("pedal", "spoke", 10),
    ("seat", "cushion", 1)
]

def components():
    components_set = set()

    for part, subpart, qty in assembly:
        components_set.add((part, subpart))

    new_tuples = True
    while new_tuples:
        new_tuples = False
        components_copy = components_set.copy()  
        for part, part2, qty in assembly:
            for p2, subpart in components_copy: 
                if part2 == p2:
                    new_tuple = (part, subpart)
                    if new_tuple not in components_set:
                        components_set.add(new_tuple)
                        new_tuples = True

    return components_set

components_relation = components()

print("Components Relation:")
for component in components_relation:
    print(component)

# print("\nComponents of 'wheel':")
# for component in components_relation:
#     if component[0] == 'wheel':
#         print(component)