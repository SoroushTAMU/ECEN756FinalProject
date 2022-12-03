

# Number of Candidates = m, Candidates are 0,1,...,m-1

def argmax_of_list(array):

    max_num=-1
    argmaxes = []

    for index, entry in enumerate(array):
        if entry > max_num:
            argmaxes = []
            argmaxes.append(index)
        elif entry == max_num:
            argmaxes.append(index)

    return argmaxes

def plurality(L, m):
    # Returns the winner(s) under plurality voting
    # Winner is candidate with most 1st preference ranks
    # NOT majority rules. Winner can be candidate with less than 50% 

    """
        L: List of preference profiles for each voter. Preference profiles are strict ranking of candidates (ints)
        m: Number of candidates
    """

    num_of_votes = [0]*m
    for preference_profile in L:
        num_of_votes[preference_profile[0]] += 1
    
    return argmax_of_list(num_of_votes)
    
def borda(L, m):
    # Gives m-1 points to a candidate if they are ranked 1st in a profile, m-2 if ranked 2nd, etc.
    # Winner is candidate with most points

    """
        L: List of preference profiles for each voter. Preference profiles are strict ranking of candidates (ints)
        m: Number of candidates
    """

    points = [0]*m

    for preference_profile in L:
        for rank, candidate in enumerate(preference_profile):
            points[candidate] += m - 1 - rank

    return argmax_of_list(points)


