PATTERN_NAMES = {
    "CDL_2CROWS": "Two Crows",
    "CDL_3BLACKCROWS": "Three Black Crows",
    "CDL_3INSIDE": "Three Inside Up/Down",
    "CDL_3LINESTRIKE": "Three-Line Strike",
    "CDL_3OUTSIDE": "Three Outside Up/Down",
    "CDL_3STARSINSOUTH": "Three Stars In The South",
    "CDL_3WHITESOLDIERS": "Three Advancing White Soldiers",
    "CDL_ABANDONEDBABY": "Abandoned Baby",
    "CDL_ADVANCEBLOCK": "Advance Block",
    "CDL_BELTHOLD": "Belt-hold",
    "CDL_BREAKAWAY": "Breakaway",
    "CDL_CLOSINGMARUBOZU": "Closing Marubozu",
    "CDL_CONCEALBABYSWALL": "Concealing Baby Swallow",
    "CDL_COUNTERATTACK": "Counterattack",
    "CDL_DARKCLOUDCOVER": "Dark Cloud Cover",
    "CDL_DOJISTAR": "Doji Star",
    "CDL_DOJI_10_0.1": "Doji",
    "CDL_DRAGONFLYDOJI": "Dragonfly Doji",
    "CDL_ENGULFING": "Engulfing Pattern",
    "CDL_EVENINGDOJISTAR": "Evening Doji Star",
    "CDL_EVENINGSTAR": "Evening Star",
    "CDL_GAPSIDESIDEWHITE": "Up/Down-gap Side-by-side White Lines",
    "CDL_GRAVESTONEDOJI": "Gravestone Doji",
    "CDL_HAMMER": "Hammer",
    "CDL_HANGINGMAN": "Hanging Man",
    "CDL_HARAMI": "Harami Pattern",
    "CDL_HARAMICROSS": "Harami Cross Pattern",
    "CDL_HIGHWAVE": "High-Wave Candle",
    "CDL_HIKKAKE": "Hikkake Pattern",
    "CDL_HIKKAKEMOD": "Modified Hikkake Pattern",
    "CDL_HOMINGPIGEON": "Homing Pigeon",
    "CDL_IDENTICAL3CROWS": "Identical Three Crows",
    "CDL_INNECK": "In-Neck Pattern",
    "CDL_INSIDE": "Inside Bar",
    "CDL_INVERTEDHAMMER": "Inverted Hammer",
    "CDL_KICKING": "Kicking",
    "CDL_KICKINGBYLENGTH": "Kicking (by longer marubozu)",
    "CDL_LADDERBOTTOM": "Ladder Bottom",
    "CDL_LONGLEGGEDDOJI": "Long Legged Doji",
    "CDL_LONGLINE": "Long Line Candle",
    "CDL_MARUBOZU": "Marubozu",
    "CDL_MATCHINGLOW": "Matching Low",
    "CDL_MATHOLD": "Mat Hold",
    "CDL_MORNINGDOJISTAR": "Morning Doji Star",
    "CDL_MORNINGSTAR": "Morning Star",
    "CDL_ONNECK": "On-Neck Pattern",
    "CDL_PIERCING": "Piercing Pattern",
    "CDL_RICKSHAWMAN": "Rickshaw Man",
    "CDL_RISEFALL3METHODS": "Rising/Falling Three Methods",
    "CDL_SEPARATINGLINES": "Separating Lines",
    "CDL_SHOOTINGSTAR": "Shooting Star",
    "CDL_SHORTLINE": "Short Line Candle",
    "CDL_SPINNINGTOP": "Spinning Top",
    "CDL_STALLEDPATTERN": "Stalled Pattern",
    "CDL_STICKSANDWICH": "Stick Sandwich",
    "CDL_TAKURI": "Takuri (Dragonfly Doji with long lower shadow)",
    "CDL_TASUKIGAP": "Tasuki Gap",
    "CDL_THRUSTING": "Thrusting Pattern",
    "CDL_TRISTAR": "Tristar Pattern",
    "CDL_UNIQUE3RIVER": "Unique 3 River",
    "CDL_UPSIDEGAP2CROWS": "Upside Gap Two Crows",
    "CDL_XSIDEGAP3METHODS": "Upside/Downside Gap Three Methods",
}

_SUFFIXES = (" (Bullish)", " (Bearish)")


def replace_pattern_name(name):
    suffix = ""
    for s in _SUFFIXES:
        if name.endswith(s):
            name, suffix = name[: -len(s)], s
            break

    readable = PATTERN_NAMES.get(name)
    if readable is None:
        readable = name[len("CDL_"):].replace("_", " ").title() if name.startswith("CDL_") else name

    return f"{readable}{suffix}"
