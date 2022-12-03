

class Vote:
    def __init__(self, candidate, next_candidate, preference=0):
        """
            candidate: int representing candidate vote is cast for
            next_candidate: candidate that is ranked after candidate
            preference: strict (0: >), weak (1: >=), indifferent (2: ==)
        """
        self.candidate = candidate
        self.next_candidate = next_candidate
        self.preference = preference


class Vote:
    def __init__(self, candidate, next_candidate, preference=0):
        """
            candidate: int representing candidate vote is cast for
            next_candidate: candidate that is ranked after candidate
            preference: strict (0: >), weak (1: >=), indifferent (2: ==)
        """
        self.candidate = candidate
        self.next_candidate = next_candidate
        self.preference = preference
    