from cogs.rules.base_rule import BaseRule

class PirateRule(BaseRule):
    """Rule requiring messages to include pirate-themed language"""
    
    @property
    def name(self):
        return "Pirate Rule"
    
    @property
    def description(self):
        return f"For the next {self.duration} minutes, everyone must speak like a pirate. [Pirate Glossary](<https://www.pirateglossary.com/>)"
    
    async def check_message(self, message):
        # Pirate terms to check for - normalized to lowercase without punctuation
        pirate_terms = [
            "ahoy",
            "arr",
            "avast",
            "aye",
            "becalmed",
            "belay",
            "bilged on her anchor",
            "blimey",
            "blow the man down",
            "boom about",
            "bring a spring upon her cable",
            "careen",
            "chase",
            "code of conduct",
            "come about",
            "crack jennys tea cup",
            "crimp",
            "dance the hempen jig",
            "davy jones locker",
            "dead men tell no tales",
            "deadlights",
            "fire in the hole",
            "furl",
            "give no quarter",
            "handsomely",
            "haul wind",
            "heave down",
            "heave",
            "ho",
            "letter of marque",
            "list",
            "long clothes",
            "marooned",
            "me",
            "no prey no pay",
            "overhaul",
            "parley",
            "piracy",
            "quarter",
            "reef sails",
            "run a shot across the bow",
            "sail ho",
            "scupper that",
            "sea legs",
            "shiver me timbers",
            "show a leg",
            "sink me",
            "smartly",
            "take a caulk",
            "to go on account",
            "warp",
            "weigh anchor",
            "ye",
            "admiral of the black",
            "bilge rat",
            "boatswain",
            "brethren of the coast",
            "buccaneer",
            "bucko",
            "carouser",
            "chandler",
            "corsair",
            "coxswain",
            "hands",
            "hearties",
            "interloper",
            "jack ketch",
            "jack tar",
            "knave",
            "lad",
            "landlubber",
            "lass",
            "lookout",
            "matey",
            "picaroon",
            "pirate",
            "pressgang",
            "privateer",
            "provost",
            "quartermaster",
            "rapscallion",
            "scallywag",
            "scourge of the seven seas",
            "strumpet",
            "sutler",
            "swab",
            "swashbuckler",
            "swing the lead",
            "wench",
            "aft",
            "amidship",
            "ballast",
            "beam",
            "bilge",
            "bilge water",
            "bittacle",
            "boom",
            "boom chain",
            "bow",
            "bowsprit",
            "broadside",
            "bulkhead",
            "crows nest",
            "focsle",
            "gangplank",
            "gangway",
            "gunwale",
            "helm",
            "hold",
            "hull",
            "jacobs ladder",
            "keel",
            "killick",
            "lee",
            "mizzenmast",
            "poop deck",
            "main",
            "port",
            "prow",
            "quarterdeck",
            "reef",
            "rigging",
            "rudder",
            "scuppers",
            "scuttle",
            "spyglass",
            "stern",
            "starboard",
            "sternpost",
            "tack",
            "transom",
            "yardarm",
            "black jack",
            "black spot",
            "bumbo",
            "bung hole",
            "cackle fruit",
            "clap of thunder",
            "draught",
            "gout",
            "grog blossom",
            "the golden age of piracy",
            "grog",
            "hang the jib",
            "hempen halter",
            "hardtack",
            "hogshead",
            "holystone",
            "hornswoggle",
            "keelhaul",
            "loaded to the gunwales",
            "maroon",
            "measured fer yer chains",
            "mutiny",
            "nelsons folly",
            "nipperkin",
            "parrot",
            "pillage",
            "ropes end",
            "rum",
            "run a rig",
            "scurvy",
            "salmagundi",
            "spirits",
            "splice the mainbrace",
            "squiffy",
            "tankard",
            "walk the plank",
            "barkadeer",
            "barque",
            "brigantine",
            "clipper",
            "cog",
            "galleon",
            "gally",
            "hulk",
            "jolly boat",
            "long boat",
            "lugger",
            "man of war",
            "pink",
            "pinnace",
            "pirogue",
            "plate fleet",
            "schooner",
            "sloop",
            "snow",
            "tender",
            "wherry",
            "yawl",
            "anne bonny",
            "black bart",
            "black sam",
            "blackbeard",
            "calico jack",
            "captain william kidd",
            "mary read",
            "stede bonnet",
            "booty",
            "bounty",
            "coffer",
            "doubloon",
            "kings shilling",
            "loot",
            "motherload",
            "pieces of eight",
            "plunder",
            "real",
            "jack",
            "jolly roger",
            "red ensign",
            "strike colors",
            "yellow jack"
        ]
        
        # Convert message to lowercase for case-insensitive matching
        message_lower = message.content.lower()
        
        # Check if message contains any pirate terms
        if not any(term in message_lower for term in pirate_terms):
            return "Arr! That don't sound like pirate speak to me! Add some 'arr' or 'ahoy' to yer message, ye scallywag!"
        return None