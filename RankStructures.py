
""" takes in a the query structure and a dictionary of the 'hit' structures
then returns an array of tuples with where the score is the first value and an
 array of structure ids is the second value.
"""
def orderStructures(querryStruct, structureDict):
    # Generate distance scores for each result
    scoreDictionary = {}

    for glycanID in structureDict.keys():
        dist = levenshtein(structureDict[glycanID], querryStruct)
        if dist not in scoreDictionary.keys():
            scoreDictionary[dist] = []
        scoreDictionary[dist].append(glycanID)

    orderedIDS = []
    for list in sorted(scoreDictionary.keys()):
        for value in scoreDictionary[list]:
            orderedIDS.append(value)

    return orderedIDS, scoreDictionary


# Taken from https://en.wikibooks.org/wiki/Algorithm_Implementation/Strings/Levenshtein_distance#Python
# A function to compute the levenshtein distance between two strings
def levenshtein(s1, s2):
    if len(s1) < len(s2):
        return levenshtein(s2, s1)

    # len(s1) >= len(s2)
    if len(s2) == 0:
        return len(s1)

    previous_row = range(len(s2) + 1)
    for i, c1 in enumerate(s1):
        current_row = [i + 1]
        for j, c2 in enumerate(s2):
            insertions = previous_row[
                             j + 1] + 1  # j+1 instead of j since previous_row and current_row are one character longer
            deletions = current_row[j] + 1  # than s2
            substitutions = previous_row[j] + (c1 != c2)
            current_row.append(min(insertions, deletions, substitutions))
        previous_row = current_row

    return previous_row[-1]
