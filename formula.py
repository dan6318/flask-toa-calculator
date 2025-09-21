# Formulas for calculation go here

class RaidInputs:
    def __init__(self, input_dict):
        self.raid_level = input_dict.get("raid_level")
        self.team_size = input_dict.get("team_size")
        self.personal_points = input_dict.get("personal_points")
        self.party_points = input_dict.get("party_points")

class UniqueCalculations:
    @staticmethod
    def points_per_percent(raid_level: int):
        # Points needed per 1% chance at a unique
        RLs = UniqueCalculations.scaled_raid_level(raid_level)
        res = 10500 - int(round(20 * RLs))
        if res > 500:
            return res
        else:
            return 500 # 500 point floor, cannot be lower

    @staticmethod
    def scaled_raid_level(raid_level: int):
        # Scaled rate level for expert completions over 300 raid level
        # Wiki states 310 <= just return original level
        # For over 310, interpolate linearly at 1/3 slope
        # E.g - rl = 400 -> RL_s = 310 + (410-310)/3 = 340
        if raid_level <= 310:
            return raid_level
        return 310 + ((raid_level - 310) / 3)
    
    @staticmethod
    def calculate_unique_table(raid_level: int, pct_chance: float):
        # Formulas here are impacted by summer-sweepup update.
        # In future, will need to be changed to interpolate linearly.
        if raid_level < 350:
            return {
                "Osmumtens_fang": (1/3.43) * pct_chance,
                "Lightbearer": (1/3.43) * pct_chance,
                "Elidnis_ward": (1/8) * pct_chance,
                "Masori_mask": (1/12) * pct_chance,
                "Masori_body": (1/12) * pct_chance,
                "Masori_chaps": (1/12) * pct_chance,
                "Tumekens_shadow": (1/24) * pct_chance,
            }
        elif raid_level < 400:
            return {
                "Osmumtens_fang": (1/3.67) * pct_chance,
                "Lightbearer": (1/3.67) * pct_chance,
                "Elidnis_ward": (1/7.34) * pct_chance,
                "Masori_mask": (1/11) * pct_chance,
                "Masori_body": (1/11) * pct_chance,
                "Masori_chaps": (1/11) * pct_chance,
                "Tumekens_shadow": (1/22) * pct_chance,
            }
        elif raid_level < 450:
            return {
                "Osmumtens_fang": (1/4.1) * pct_chance,
                "Lightbearer": (1/4.1) * pct_chance,
                "Elidnis_ward": (1/6.48) * pct_chance,
                "Masori_mask": (1/9.72) * pct_chance,
                "Masori_body": (1/9.72) * pct_chance,
                "Masori_chaps": (1/9.72) * pct_chance,
                "Tumekens_shadow": (1/20.47) * pct_chance,
            }
        elif raid_level < 500:
            return {
                "Osmumtens_fang": (1/4.5) * pct_chance,
                "Lightbearer": (1/4.5) * pct_chance,
                "Elidnis_ward": (1/6) * pct_chance,
                "Masori_mask": (1/9) * pct_chance,
                "Masori_body": (1/9) * pct_chance,
                "Masori_chaps": (1/9) * pct_chance,
                "Tumekens_shadow": (1/18) * pct_chance,
            }
        elif raid_level < 600:
            return {
                "Osmumtens_fang": (1/5.24) * pct_chance,
                "Lightbearer": (1/5.24) * pct_chance,
                "Elidnis_ward": (1/5.4) * pct_chance,
                "Masori_mask": (1/8.11) * pct_chance,
                "Masori_body": (1/8.11) * pct_chance,
                "Masori_chaps": (1/8.11) * pct_chance,
                "Tumekens_shadow": (1/15.72) * pct_chance,
            }

    def probability_calculator(self, inp: RaidInputs):
        # Final calculation function
        # Should return as JSON format for front end
        if inp.team_size == 1:
            party_pts = inp.personal_points
            estimation = False
        elif inp.party_points:
            party_pts = inp.party_points
            estimation = False
        else: # If not 1 party size and no party points listed, estimation carried out
            estimation = True
            party_pts = inp.personal_points * inp.team_size
        ppp = self.points_per_percent(inp.raid_level)
        party_pct = party_pts / ppp
        party_prob = min(party_pct / 100.0, 0.55) # 55% is party cap per raid
        p_share = inp.personal_points / party_pts
        personal_prob = party_prob * p_share
        unique_table_personal = self.calculate_unique_table(inp.raid_level, personal_prob)
        unique_table_party = self.calculate_unique_table(inp.raid_level, party_prob)
        return {
            "party_prob": party_prob,
            "personal_prob": personal_prob,
            "points_per_percent": ppp,
            "party_points": party_pts,
            "party_points_estimation": estimation,
            "personal_points": inp.personal_points,
            "team_size": inp.team_size,
            "unique_table_personal": unique_table_personal,
            "unique_table_party": unique_table_party
        }


