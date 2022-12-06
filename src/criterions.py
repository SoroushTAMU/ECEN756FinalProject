
# Number of Candidates = m, Candidates are 0,1,...,m-1

def condorcet(L, m):
    # Return Condorcent winner(s) if there exists one(or multiple)

    """
        L: List of preference profiles for each voter. Preference profiles are strict ranking of candidates (ints)
        m: Number of candidates
    """

    head_to_head =[[0 for i in range(m)] for j in range(m)]

    # Calculate the head to heads
    for preference_profile in L:
        for index, candidate in enumerate(preference_profile):
            less_preferred_candidates = preference_profile[index+1:]

            for lpc in less_preferred_candidates:
                head_to_head[candidate][lpc] += 1

    condorcet_winners = []

    # Strict Condorcet winners need to be preferred to every other candidate
    # Weak Condorcet winners preferred or indifferent to every other candidate
    for i in range(m):
        wins = 0
        for j in range(m):
            if i == j:
                continue
            if head_to_head[i][j] >= head_to_head[j][i]:
                wins += 1
        
        if wins == m - 1:
            condorcet_winners.append(i)
    
    return condorcet_winners

            