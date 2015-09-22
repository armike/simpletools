"""
Matching algorithms
"""


class Matcher(object):

    MATCH_QUALITY_HIGH = 100
    MATCH_QUALITY_WAY_HIGHER = 200
    MATCH_SPEED_FAST = 10
    MATCH_SPEED_REASONABLY_FAST = 1999

    def match_drivers_and_pa(self, passengers, drivers):
        match_quality = Matcher.MATCH_QUALITY_WAY_HIGHER
        match_speed =  Matcher.MATCH_SPEED_REASONABLY_FAST
        for passenger in passengers:
            ...

    def find_matches(self):
        ...
