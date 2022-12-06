from utils import argmax_of_list, argmin_of_list, get_arg
import random
import math

# Number of Candidates = m, Candidates are 0,1,...,m-1

def iterative_plurality(L, m, tiebraking="Lexicographical", from_truth=False, initial_state=None):
    # Returns the winner(s) under iterative plurality voting, with optional tiebraking

    """
        L: List of preference profiles for each voter. Preference profiles are strict ranking of candidates (ints)
        m: Number of candidates
        tiebraking: Optional tiebraking. Can be "Lexicographical" or "Random"
        from_truth: True if want initial votes to be truthful, False if want initial votes to be random
        initial_state: Initial voting state if from_truth is False. If None, then randomized initial state is used. 

        returns: 
            votes: how each voter voted after convergence
            num_of_votes: number of votes each candidate received
            top_candidates: candidate(s) with most votes
            num_iterations: number of iterations until convergence
    """
    
    if from_truth:
        votes = [preference_profile[0] for preference_profile in L]
    else:
        if initial_state:
            votes = initial_state
        else:
            votes = [random.randint(0,m-1) for preference_profile in L]
        

    
    num_iterations = 0
    convergence = False
    num_unchanged_votes = 0
    while not convergence:
        for voter, preference_profile in enumerate(L):
            #print(votes)
            initial_vote = votes[voter]

            changed_vote = False
            for new_vote in range(m):
                if new_vote == initial_vote:
                    continue

                if is_DR_and_Better_Reply(initial_vote, new_vote, get_num_votes(votes,m), preference_profile, tiebraking):
                    votes[voter] = new_vote
                    changed_vote = True
                    break
            
            num_iterations += 1

            if not changed_vote:
                num_unchanged_votes += 1
            else:
                num_unchanged_votes = 0
            
            if num_unchanged_votes == len(votes):
                convergence = True
    
    return votes, get_num_votes(votes, m), get_winner(votes, tiebraking), num_iterations-len(votes)






def RCR_iterative_plurality(L, m, tiebraking="Lexicographical", from_truth=False, initial_state=None):
    # Returns the winner(s) under Randomized Candidate Removal iterative plurality voting, with optional tiebraking
    # After each round where every voter had the chance to change their vote, remove the least popular candidate.
    # If voter does not have a Direct and better reply after removing a candidate, randoly select their vote.

    """
        L: List of preference profiles for each voter. Preference profiles are strict ranking of candidates (ints)
        m: Number of candidates
        tiebraking: Optional tiebraking. Can be "Lexicographical" or "Random"
        from_truth: True if want initial votes to be truthful, False if want initial votes to be random
        initial_state: Initial voting state if from_truth is False. If None, then randomized initial state is used. 

        returns: 
            votes: how each voter voted after convergence
            num_of_votes: number of votes each candidate received
            top_candidates: candidate(s) with most votes
            num_iterations: number of iterations until convergence
    """
    
    if from_truth:
        votes = [preference_profile[0] for preference_profile in L]
    else:
        if initial_state:
            votes = initial_state
        else:
            votes = [random.randint(0,m-1) for preference_profile in L]
        

    
    num_iterations = 0
    convergence = False
    num_unchanged_votes = 0
    viable_candidates = [*range(m)]

    while not convergence:
        for voter, preference_profile in enumerate(L):
            changed_vote = False

            initial_vote = votes[voter]
            if initial_vote not in viable_candidates:
                initial_vote = viable_candidates[random.randint(0, len(viable_candidates)-1)]
                votes[voter] = initial_vote
                changed_vote = True          

            for new_vote in range(m):
                if new_vote == initial_vote or new_vote not in viable_candidates:
                    continue

                if is_DR_and_Better_Reply(initial_vote, new_vote, get_num_votes(votes,m), preference_profile, tiebraking):
                    votes[voter] = new_vote
                    changed_vote = True
                    break
            
            num_iterations += 1

            if not changed_vote:
                num_unchanged_votes += 1
            else:
                num_unchanged_votes = 0
            
            if num_unchanged_votes == len(votes):
                convergence = True
    
        loser = get_loser_RCR(get_num_votes(votes, m), tiebraking, viable_candidates)
        viable_candidates.remove(loser)

        if len(viable_candidates) == 1:
            break
    
    return votes, get_num_votes(votes, m), get_winner(votes, tiebraking), num_iterations


def get_num_votes(votes, m):
    num_votes = [0]*m

    for vote in votes:
        num_votes[vote] += 1
    
    return num_votes


def change_vote(initial_vote, new_vote, num_votes):
    # num_votes is number of votes each candidate has
    new_list = num_votes.copy()
    new_list[initial_vote] = new_list[initial_vote] - 1
    new_list[new_vote] = new_list[new_vote] + 1

    return new_list

def isDR(initial_vote, new_vote, num_votes):
    new_list = change_vote(initial_vote, new_vote, num_votes)

    return new_list[new_vote] == max(new_list)

def is_DR_and_Better_Reply(initial_vote, new_vote, num_votes, preference_profile, tiebraking="Lexicographical"):
    new_list = change_vote(initial_vote, new_vote, num_votes)

    if new_list[new_vote] != max(new_list):
        return False
    
    old_winner = get_winner(num_votes, tiebraking=tiebraking)
    new_winner = get_winner(new_list, tiebraking=tiebraking)

    return get_arg(preference_profile, new_winner) < get_arg(preference_profile, old_winner)

         

def get_winner(votes, tiebraking):

    top_candidates = argmax_of_list(votes)

    if tiebraking == "Lexicographical":
        top_candidate = min(top_candidates)
    
    else:
        top_candidate = top_candidates[random.randint(0, len(top_candidates)-1)]
    
    return top_candidate

def get_loser(votes, tiebraking):

    worst_candidates = argmin_of_list(votes)

    if tiebraking == "Lexicographical":
        worst_candidate = max(worst_candidates)
    
    else:
        worst_candidate = worst_candidates[random.randint(0, len(worst_candidates)-1)]
    
    return worst_candidate

def get_loser_RCR(votes, tiebraking, viable_candidates):

    votes2 = votes.copy()
    for i in range(len(votes2)):
        if i not in viable_candidates:
            votes2[i] = math.inf

    worst_candidates = argmin_of_list(votes2)

    if tiebraking == "Lexicographical":
        worst_candidate = max(worst_candidates)
    
    else:
        worst_candidate = worst_candidates[random.randint(0, len(worst_candidates)-1)]
    
    return worst_candidate



def plurality(L, m, tiebraking=None):
    # Returns the winner(s) under plurality voting, with optional tiebraking
    # Winner is candidate with most 1st preference ranks
    # NOT majority rules. Winner can be candidate with less than 50% 

    """
        L: List of preference profiles for each voter. Preference profiles are strict ranking of candidates (ints)
        m: Number of candidates
        tiebraking: Optional tiebraking. Can be "Lexicographical", "Random", or None

        returns: 
            num_of_votes: number of votes each candidate received
            top_candidates: candidate(s) with most votes
            worst_candidates: candidate(s) with least votes
    """

    votes = [preference_profile[0] for preference_profile in L]
    num_of_votes = get_num_votes(votes, m)

    top_candidates = argmax_of_list(num_of_votes)
    worst_candidates = argmin_of_list(num_of_votes)

    if tiebraking == "Lexicographical":
        top_candidates = min(top_candidates)
        worst_candidates = max(worst_candidates)
    
    elif tiebraking == "Random":
        top_candidates = [top_candidates[random.randint(0, len(top_candidates)-1)]]
        worst_candidates = [worst_candidates[random.randint(0, len(worst_candidates)-1)]]
    
    return num_of_votes, top_candidates, worst_candidates



