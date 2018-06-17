import random
from typing import Iterator, List, Tuple

adjectives = (
    "abortive", "abounding", "abrasive", "absent", "acceptable", "adamant", "adhesive", "adjoining", "aggressive",
    "alike", "alleged", "aloof", "ambitious", "amused", "aspiring", "available", "awake", "axiomatic", "barbarous",
    "bashful", "beautiful", "befitting", "beneficial", "blushing", "boundless", "brawny", "certain", "childlike",
    "cluttered", "courageous", "crooked", "damp", "deadpan", "debonair", "decorous", "defiant", "delirious",
    "detailed", "disturbed", "divergent", "drab", "dramatic", "drunk", "electric", "enormous", "erect", "evanescent",
    "excellent", "exultant", "faded", "famous", "far-flung", "fascinated", "faulty", "festive", "fine", "fixed",
    "flaky", "flat", "fluttering", "foregoing", "frail", "fresh", "frightened", "funny", "furtive", "gainful", "glib",
    "godly", "half", "hallowed", "handsome", "hard", "heavenly", "hesitant", "high", "honorable", "hot", "hungry",
    "hurt", "hushed", "hypnotic", "ill-fated", "illegal", "important", "incompetent", "inconclusive", "infamous",
    "innocent", "insidious", "instinctive", "jazzy", "jumbled", "kind", "knowing", "late", "laughable", "lean",
    "loving", "madly", "majestic", "married", "materialistic", "measly", "mighty", "misty", "murky", "mushy",
    "mysterious", "needy", "next", "nice", "nondescript", "nutritious", "omniscient", "ossified", "overconfident",
    "panoramic", "parallel", "parched", "pastoral", "plant", "possible", "pricey", "prickly", "private", "productive",
    "pumped", "purple", "purring", "quixotic", "rabid", "rare", "real", "receptive", "resolute", "right", "rightful",
    "ritzy", "rough", "ruddy", "rude", "salty", "sassy", "satisfying", "scandalous", "sedate", "selective", "separate",
    "shrill", "sincere", "slow", "small", "smooth", "sordid", "sour", "spicy", "spiky", "spiteful", "spooky" "spotty",
    "steady", "subdued", "successful", "supreme", "sweltering", "synonymous", "talented", "tasty", "teeny", "telling",
    "temporary", "tender", "tense", "tenuous", "thinkable", "thoughtless", "tiny", "tough", "trashy", "two",
    "uncovered", "uninterested", "unruly", "unsuitable", "used", "useful", "vagabond", "verdant", "vivacious",
    "voiceless", "waggish", "wasteful", "wealthy", "whole", "wise", "woebegone", "workable", "wrong", "young",
)

nouns = (
    "actions", "activities", "additions", "advertisements", "afterthoughts", "airplanes", "amounts", "angles", "ants",
    "baskets", "baths", "battles", "bees", "beginners", "behaviors", "beliefs", "bells", "berries", "bikes",
    "birthdays", "bits", "boats", "boys", "breaths", "bubbles", "bulbs", "bursts", "butter", "cables", "camps", "cans",
    "captions", "cars", "carpenters", "cats", "cemeteries", "changes", "channels", "chickens", "classes", "clubs",
    "committees", "covers", "cracks", "crates", "crayons", "crowds", "decisions", "degrees", "details", "directions",
    "dresses", "drops", "dusts", "errors", "examples", "expansions", "falls", "fangs", "feelings", "firemen",
    "flowers", "fog", "feet", "fowls", "frogs", "glasses", "gloves", "grandmothers", "grounds", "guns", "haircuts",
    "halls", "harmonies", "hats", "hopes", "horns", "horses", "ideas", "inks", "insects", "interests", "inventions",
    "irons", "islands", "jails", "jeans", "jellyfish", "laborers", "lakes", "letters", "lockets", "matches", "measures",
    "mice", "milk", "motions", "moves", "nerves", "numbers", "pans", "pancakes", "persons", "pets", "pickles", "pies",
    "pizzas", "plantations", "plastics", "ploughs", "pockets", "potatoes", "powders", "properties", "reactions",
    "regrets", "riddles", "rivers", "rocks", "sails", "scales", "scarecrows", "scarves", "scenes", "schools",
    "sciences", "shakes", "shapes", "shirts", "silvers", "sinks", "snakes", "sneezes", "sofas", "songs", "sounds",
    "spades", "sparks", "stages", "stamps", "stars", "stations", "stews", "stomachs", "suggestions", "suits", "swings",
    "tables", "tents", "territories", "tests", "textures", "things", "thoughts", "threads", "tigers", "toads", "toes",
    "tomatoes", "trains", "treatments", "troubles", "tubs", "turkeys", "umbrellas", "uncles", "vacations", "veils",
    "voices", "volcanoes", "volleyballs", "walls", "wars", "waters", "waves", "wilderness", "women", "words", "works",
    "worms", "wounds", "writings", "yams", "yards", "yarns", "zebras"
)


def get_adjectives(num: int = 1) -> List[str]:
    """
    Get a list of random, unique adjectives
    """

    return random.sample(adjectives, num)


def get_nouns(num: int = 1) -> List[str]:
    """
    Get a list of random, unique nouns
    """

    return random.sample(nouns, num)


def get_word_pairs(num: int = 1) -> Iterator[Tuple[str, str]]:
    """
    Get an iterator over random, unique (adjective, noun) pairs
    """

    return zip(
        get_adjectives(num),
        get_nouns(num)
    )
