import re
import random
from itertools import combinations, permutations
from itertools import product
import timeit



pref = {

'j1':[[1,3,2],[2,1,3]], 
'j2':[[1,2,3],[3,1,2]], 
'j3':[[2,3,1],[1,2,3]], 
's1':[[1,2,3],[2,1,3]], 
's2':[[3,1,2],[3,2,1]], 
's3':[[1,3,2],[2,1,3]], 
'g1':[[1,3,2],[1,2,3]],
'g2':[[2,1,3],[3,2,1]], 
'g3':[[1,2,3],[1,2,3]],

}

pref_ = {

    'j1':[['s1','s3','s2'],['g2','g1','g3']], 
    'j2':[['s1','s2','s3'],['g3','g1','g2']], 
    'j3':[['s2','s3','s1'],['g1','g2','g3']], 
    's1':[['j1','j2','j3'],['g2','g1','g3']], 
    's2':[['j3','j1','j2'],['g3','g2','g1']], 
    's3':[['j1','j3','j2'],['g2','g1','g3']], 
    'g1':[['j1','j3','j2'],['s1','s2','s3']],
    'g2':[['j2','j1','j3'],['s3','s2','s1']], 
    'g3':[['j1','j2','j3'],['s1','s2','s3']],

}
'''
pref = {

'j1':[[1,2,3],[1,2,3]], 
'j2':[[1,2,3],[1,3,2]], 
'j3':[[1,2,3],[1,2,3]], 
's1':[[1,2,3],[1,2,3]], 
's2':[[1,2,3],[1,2,3]], 
's3':[[1,2,3],[1,2,3]], 
'g1':[[1,2,3],[1,2,3]],
'g2':[[1,2,3],[1,2,3]], 
'g3':[[1,2,3],[1,2,3]],

}

pref_ = {

    'j1':[['s1','s2','s3'],['g1','g2','g3']], 
    'j2':[['s1','s2','s3'],['g1','g2','g3']], 
    'j3':[['s1','s2','s3'],['g1','g2','g3']], 
    's1':[['j1','j2','j3'],['g1','g2','g3']], 
    's2':[['j1','j2','j3'],['g1','g2','g3']], 
    's3':[['j1','j2','j3'],['g1','g2','g3']], 
    'g1':[['j1','j2','j3'],['s1','s2','s3']],
    'g2':[['j1','j2','j3'],['s1','s2','s3']], 
    'g3':[['j1','j2','j3'],['s1','s2','s3']],

}'''



pairings = {
    "(j3, s2, g1), (j1, s3, g2), (j2, s1, g3)": False, 
    "(j3, s2, g1), (j1, s3, g3), (j2, s1, g2)": False, 
    "(j3, s2, g1), (j1, s1, g3), (j2, s3, g2)": False, 
    "(j3, s2, g2), (j1, s3, g1), (j2, s1, g3)": False, 
    "(j3, s2, g2), (j1, s3, g3), (j2, s1, g1)": False, 
    "(j3, s2, g2), (j1, s1, g3), (j2, s3, g1)": False,
    "(j3, s2, g3), (j1, s3, g1), (j2, s1, g2)": False,
    "(j3, s2, g3), (j1, s3, g2), (j2, s1, g1)": False,
    "(j3, s2, g3), (j1, s1, g2), (j2, s3, g1)": False,
    "(j3, s1, g1), (j1, s3, g2), (j2, s2, g3)": False,
    "(j3, s1, g1), (j1, s3, g3), (j2, s2, g2)": False,
    "(j3, s1, g1), (j1, s1, g3), (j2, s3, g2)": False,
    "(j3, s1, g2), (j1, s3, g1), (j2, s2, g3)": False,
    "(j3, s1, g2), (j1, s3, g3), (j2, s2, g1)": False,
    "(j3, s1, g2), (j1, s1, g3), (j2, s3, g1)": False,
    "(j3, s1, g3), (j1, s3, g1), (j2, s2, g2)": False,
    "(j3, s1, g3), (j1, s3, g2), (j2, s2, g1)": False,
    "(j3, s1, g3), (j1, s1, g2), (j2, s3, g1)": False,
    "(j1, s1, g1), (j2, s2, g2), (j3, s3, g3)": False,
    "(j1, s1, g1), (j3, s2, g2), (j2, s3, g3)": False,
    "(j1, s1, g1), (j2, s3, g2), (j3, s2, g3)": False,
    "(j1, s1, g2), (j2, s2, g1), (j3, s3, g3)": False,
    "(j1, s1, g2), (j3, s2, g1), (j2, s3, g3)": False,
    "(j1, s1, g2), (j2, s3, g1), (j3, s2, g3)": False,
    "(j1, s1, g3), (j2, s2, g1), (j3, s3, g2)": False,
    "(j1, s1, g3), (j3, s2, g1), (j2, s3, g2)": False,
    "(j1, s1, g3), (j2, s3, g1), (j3, s2, g2)": False,
}

def generate_combinations(n):
    pairings = {}

    # Generate all permutations of indices
    indices = list(range(1, n + 1))
    perms = permutations(indices)

    # Generate pairings based on permutations
    for perm in perms:
        pairing = []
        for i, idx in enumerate(perm, start=1):
            pairing.append(f'(j{i}, s{idx}, g{idx})')
        pairings[", ".join(pairing)] = False

    return pairings


group_pref = {}

def generate_random_pref():
    # Initialize an empty dictionary to store preferences
    pref = {}

    # Generate random preferences for each person
    for i in range(1, 4):
        pref[f'j{i}'] = [random.sample([1, 2, 3], 3) for _ in range(2)]  # Random permutation for each group
    for i in range(1, 4):
        pref[f's{i}'] = [random.sample([1, 2, 3], 3) for _ in range(2)]  # Random permutation for each group
    for i in range(1, 4):
        pref[f'g{i}'] = [random.sample([1, 2, 3], 3) for _ in range(2)]  # Random permutation for each group
    

    return pref

def generate_pref():
    # Generate random preferences for individuals
    pref = generate_random_pref()

    # Initialize an empty dictionary to store group preferences
    pref_ = {}

    # Generate group preferences based on individual preferences
    for key, value in pref.items():
        if key.startswith('j'):
            group_pref_s = [f"s{rank}" for rank in value[0]]
            group_pref_g = [f"g{rank}" for rank in value[1]]
            pref_[key] = [group_pref_s, group_pref_g]
        elif key.startswith('s'):
            group_pref_j = [f"j{rank}" for rank in value[0]]
            group_pref_g = [f"g{rank}" for rank in value[1]]
            pref_[key] = [group_pref_j, group_pref_g]
        elif key.startswith('g'):
            group_pref_j = [f"j{rank}" for rank in value[0]]
            group_pref_s = [f"s{rank}" for rank in value[1]]
            pref_[key] = [group_pref_j, group_pref_s]

    return pref, pref_


pref, pref_ = generate_pref()

counter = 0

def group_prefereces(pref):

    group_pref = {}
    for key1 in pref:
        for key2 in pref:
            if key2[0] != key1[0]: 

                index1, index2 = 0,0

                if key1[0] == "j" and key2[0] == "s":

                    index1 = 1
                    index2 = 1

                if key1[0] == "j" and key2[0] == "g":

                    index1 = 0
                    index2 = 1

                if key1[0] == "s" and key2[0] == "g":

                    index1 = 0
                    index2 = 0
                
                first = [pref[key1][index1].index(x) + 1 for x in range(1, len(pref[key1][index1]) + 1)]
                second = [pref[key2][index2].index(x) + 1 for x in range(1, len(pref[key2][index2]) + 1)]

                result = [x + y for x, y in zip(first, second)]
                result = [index for index, _ in sorted(enumerate(result), key=lambda x: x[1])]
                result = [index + 1 for index in result]

                group_pref["(" + str(key1) + ", " + str(key2) + ")"] = result
    

def extract_groupings(input_string):
    # Define a regular expression pattern to match bracketed groupings
    pattern = r'\((.*?)\)'
    
    # Use regular expression to find all bracketed groupings
    groupings = re.findall(pattern, input_string)
    
    return groupings

def combine_rankings(ranking1, ranking2):
    combined_rankings = []

    # Generate all possible pairs from the rankings of the two sets
    pairs = list(product(ranking1, ranking2))

    # Sort the pairs based on the combined ranking
    sorted_pairs = sorted(pairs, key=lambda x: (x[0], x[1]))

    # Convert pairs to strings and append to combined_rankings
    for pair in sorted_pairs:
        combined_rankings.append(f"({pair[0]}, {pair[1]})")

    return combined_rankings

def generate_pairs(input):
    # Split each element into its components
    elements = input.split(", ")
    
    # Generate all possible pairs
    pairs = list(combinations(elements, 2))
    
    # Generate strings for each pair with the remaining element
    pair_strings = []
    for pair in pairs:
        remaining_element = [element for element in elements if element not in pair][0]
        pair_strings.append(f"({pair[0]}, {pair[1]}), ({remaining_element})")
    
    return pair_strings

single_pref = {}

def combine_rankings(list1, list2):
    combined_rankings = []
    
    # Generate all possible pairs from the rankings of the two lists
    pairs = list(product(enumerate(list1, start=1), enumerate(list2, start=1)))
    
    # Calculate the combined score for each pair
    for (idx1, val1), (idx2, val2) in pairs:
        combined_score = idx1 + idx2
        combined_rankings.append((val1, val2, combined_score))
    
    # Sort the pairs based on the combined score
    sorted_rankings = sorted(combined_rankings, key=lambda x: x[2])
    converted_rankings = [f"({tup[0]}, {tup[1]})" for tup in sorted_rankings]
    return converted_rankings

for key in pref_:

    single_pref[key] = combine_rankings(pref_[key][0], pref_[key][1])


def matching3D(pairings, group_pref, single_pref):

    print("---------")
    for res in pairings:

        groups = extract_groupings(res)

        all_pairs_1 = generate_pairs(groups[0])
        all_pairs_2 = generate_pairs(groups[1])
        all_pairs_3 = generate_pairs(groups[2])

        all = all_pairs_1 + all_pairs_2 + all_pairs_3
    
        stable = True

        for pair1 in all:

            for pair2 in all:
                
              if str(pair1[1]) + str(pair1[5]) == str(pair2[1]) + str(pair2[5]) and pair1 != pair2:
    
                if group_pref[pair1[:8]][group_pref[pair1[:8]][:8].index(int(pair2[-2]))] < group_pref[pair1[:8]][group_pref[pair1[:8]][:8].index(int(pair1[-2]))]:
                    if single_pref[pair2[-3:-1]].index(pair1[:8]) < single_pref[pair2[-3:-1]].index(pair2[:8]):

                        stable = False
                        #print(f"{pair1} and {pair2} form an instability\n")
                    
                        break
        
        if stable == True:
            pairings[res] = True

    for key in pairings:

        if pairings[key] == True:

            print(f"{key} is a stable matching")

        
    print("--------")

group_pref = group_prefereces(pref)
single_pref = dict()
group_pref = dict()
group_pref = {}
for key1 in pref:
        for key2 in pref:
            if key2[0] != key1[0]: 

                index1, index2 = 0,0

                if key1[0] == "j" and key2[0] == "s":

                    index1 = 1
                    index2 = 1

                if key1[0] == "j" and key2[0] == "g":

                    index1 = 0
                    index2 = 1

                if key1[0] == "s" and key2[0] == "g":

                    index1 = 0
                    index2 = 0
                
                first = [pref[key1][index1].index(x) + 1 for x in range(1, len(pref[key1][index1]) + 1)]
                second = [pref[key2][index2].index(x) + 1 for x in range(1, len(pref[key2][index2]) + 1)]

                result = [x + y for x, y in zip(first, second)]
                result = [index for index, _ in sorted(enumerate(result), key=lambda x: x[1])]
                result = [index + 1 for index in result]

                group_pref["(" + str(key1) + ", " + str(key2) + ")"] = result

for key in pref_:
     single_pref[key] = combine_rankings(pref_[key][0], pref_[key][1])

print(single_pref)
print(group_pref)
matching3D(pairings, group_pref, single_pref)


def timed():

    pref, pref_ = generate_pref()

    single_pref = dict()

    for key in pref_:
        single_pref[key] = combine_rankings(pref_[key][0], pref_[key][1])

    group_pref = {}
    for key1 in pref:
        for key2 in pref:
            if key2[0] != key1[0]: 

                index1, index2 = 0,0

                if key1[0] == "j" and key2[0] == "s":

                    index1 = 1
                    index2 = 1

                if key1[0] == "j" and key2[0] == "g":

                    index1 = 0
                    index2 = 1

                if key1[0] == "s" and key2[0] == "g":

                    index1 = 0
                    index2 = 0
                
                first = [pref[key1][index1].index(x) + 1 for x in range(1, len(pref[key1][index1]) + 1)]
                second = [pref[key2][index2].index(x) + 1 for x in range(1, len(pref[key2][index2]) + 1)]

                result = [x + y for x, y in zip(first, second)]
                result = [index for index, _ in sorted(enumerate(result), key=lambda x: x[1])]
                result = [index + 1 for index in result]

                group_pref["(" + str(key1) + ", " + str(key2) + ")"] = result

    stable = matching3D(pairings, group_pref, single_pref)

print(group_pref)
print(single_pref)
execution_time = timeit.timeit(timed, number=10)
print(f"Execution time: {execution_time} seconds")










