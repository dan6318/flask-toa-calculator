# Formulas for calculation go here

class RaidInputs:
    def __init__(self, input_dict):
        self.raid_level = input_dict.get("raid_level")
        self.team_size = input_dict.get("team_size")
        self.personal_points = input_dict.get("personal_points")
        self.party_points = input_dict.get("party_points")

class UniqueCalculations:
    def points_per_percent(raid_level: int):
        # Points needed per 1% chance at a unique
        pass

    def scaled_raid_level(raid_level: int):
        # Scaled rate level for expert completions over 300 raid level
        # Wiki states 310 <= just return original level
        # For over 310, interpolate linearly at 1/3 slope
        # E.g - rl = 400 -> RL_s = 310 + (410-310)/3 = 340
        pass

    def probability_calculator(inp: RaidInputs):
        # Final calculation function
        # Should return as JSON format for front end
        pass