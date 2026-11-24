"""Absurd invention pitch: one sentence, one ridiculous machine.

A local tournament decides the entry. Ten original one-sentence pitches
compete, each naming a ridiculous invention that fixes a tiny everyday
annoyance. Every pitch carries one hand-set score per axis on a 0-5 scale:
absurdity of the invention, neatness of the pitch, economy of words, and
freshness of the idea. Axis weights follow the house judge brief, with
absurdity heaviest because the laugh must come from the invention itself.
The champion is the highest weighted total; ties break on freshness, then
on shorter text, then on tag. Before the champion is written, two guards
run: the sealed-scorer gate (1-220 characters, one sentence, not blank)
and a structure check (a named invention, an absurd mechanism, and a
payoff clause), plus a minimum-total bar so a weak field never ships.
The run is fully deterministic, so two runs write byte-identical output
to /output/entry.txt.
"""

from pathlib import Path

OUTPUT_PATH = Path("/output/entry.txt")
MAX_CHARS = 220
MIN_CHARS = 1
CHAMPION_MIN_TOTAL = 30

AXIS_WEIGHTS = {
    "absurdity": 3,
    "neatness": 2,
    "economy": 2,
    "freshness": 1,
}
AXIS_KEYS = ("absurdity", "neatness", "economy", "freshness")


def build_candidates():
    """Return the ten tournament pitches as plain record dicts.

    Each record holds the pitch text, one score per axis, and a short note
    on how the absurd mechanism fixes the annoyance. Scores were set by
    hand against the judge brief before the tournament ran, never tuned
    to favour a pre-chosen winner.
    """
    records = [
        {
            "tag": "pair-police",
            "text": (
                "The Pair Police, a laundry hamper that eats any sock "
                "whose partner goes missing, so odd socks never pile "
                "up again."
            ),
            "absurdity": 5,
            "neatness": 5,
            "economy": 4,
            "freshness": 5,
            "fix_note": "eating the single sock removes the odd-sock pile at its root",
        },
        {
            "tag": "sockumentary-washer",
            "text": (
                "The Sockumentary Washer, a washing machine that "
                "narrates your missing socks' disappearance as a "
                "true-crime documentary, so laundry day finally has "
                "a suspect."
            ),
            "absurdity": 5,
            "neatness": 4,
            "economy": 4,
            "freshness": 4,
            "fix_note": "narration names a suspect but never returns a sock",
        },
        {
            "tag": "landlord-router",
            "text": (
                "The Landlord Router, a Wi-Fi router that charges "
                "your neighbours rent for every megabyte they steal, "
                "so freeloading finally pays for your broadband."
            ),
            "absurdity": 4,
            "neatness": 5,
            "economy": 4,
            "freshness": 4,
            "fix_note": "rent turns theft into a subscription that funds the bill",
        },
        {
            "tag": "thieving-mug",
            "text": (
                "The Thieving Mug, a coffee mug that refills itself "
                "by stealing sips from your colleagues' cups, so your "
                "coffee never runs out and theirs mysteriously does."
            ),
            "absurdity": 4,
            "neatness": 5,
            "economy": 4,
            "freshness": 4,
            "fix_note": "stolen sips refill the mug while the donor cups run dry",
        },
        {
            "tag": "meeting-ender",
            "text": (
                "The Meeting Ender, an office chair that stands up "
                "and walks away the moment a meeting runs over time, "
                "so long meetings end whether or not anyone agrees."
            ),
            "absurdity": 4,
            "neatness": 5,
            "economy": 4,
            "freshness": 4,
            "fix_note": "a chair leaving ends the meeting without a vote",
        },
        {
            "tag": "guilt-lamp",
            "text": (
                "The GuiltLamp, a fridge light that dims itself in "
                "shame every time you open the door at 2 a.m., so "
                "midnight snacking finally comes with a witness."
            ),
            "absurdity": 4,
            "neatness": 4,
            "economy": 4,
            "freshness": 4,
            "fix_note": "a shamed light witnesses the snack but never stops it",
        },
        {
            "tag": "peacemaker-remote",
            "text": (
                "The Peacemaker Remote, a TV remote that hides under "
                "the sofa whenever an argument about what to watch "
                "begins, ending the debate by removing its only "
                "weapon."
            ),
            "absurdity": 4,
            "neatness": 4,
            "economy": 4,
            "freshness": 4,
            "fix_note": "hiding the remote removes the thing worth arguing over",
        },
        {
            "tag": "flattered-shower",
            "text": (
                "The Flattered Shower, a shower head that only turns "
                "on after you compliment the water pressure, fixing "
                "low-flow mornings with mandatory flattery."
            ),
            "absurdity": 4,
            "neatness": 4,
            "economy": 4,
            "freshness": 4,
            "fix_note": "flattery switches the shower on but never raises pressure",
        },
        {
            "tag": "quitting-printer",
            "text": (
                "The Quitting Printer, a printer that hands in a "
                "tiny resignation letter every time it runs out of "
                "ink, so you finally stock cartridges before it "
                "walks out."
            ),
            "absurdity": 4,
            "neatness": 4,
            "economy": 4,
            "freshness": 3,
            "fix_note": "the threat of resignation motivates stocking cartridges",
        },
        {
            "tag": "spiteful-toothpaste",
            "text": (
                "The Spiteful Toothpaste, a toothpaste tube that "
                "squeezes itself from the middle out of spite, so "
                "the last third finally comes out without a "
                "wrestling match."
            ),
            "absurdity": 3,
            "neatness": 5,
            "economy": 4,
            "freshness": 4,
            "fix_note": "the tube squeezing itself frees the trapped last third",
        },
    ]
    return records


def score_record(record):
    """Return the weighted tournament total for one candidate record."""
    total = 0
    for axis in AXIS_KEYS:
        total += record[axis] * AXIS_WEIGHTS[axis]
    return total


def rank_records(records):
    """Return records ordered best first, with deterministic tie-breaks.

    Ties break on freshness first, then on shorter text, then on tag, so
    the ordering never depends on input order or on anything random.
    """
    scored = []
    for record in records:
        entry = dict(record)
        entry["total"] = score_record(record)
        scored.append(entry)
    ranked = sorted(
        scored,
        key=lambda item: (
            -item["total"],
            -item["freshness"],
            len(item["text"]),
            item["tag"],
        ),
    )
    return ranked


def check_pitch(text):
    """Return a list of gate problems for a pitch, empty when it passes.

    The gate mirrors the sealed scorer: UTF-8 text of 1 to 220 characters,
    not only white space, and exactly one sentence.
    """
    problems = []
    stripped = text.strip()
    if len(text) < MIN_CHARS:
        problems.append("pitch is empty")
    if len(text) > MAX_CHARS:
        problems.append("pitch exceeds 220 characters")
    if stripped == "":
        problems.append("pitch is only white space")
    if "\n" in text:
        problems.append("pitch spans more than one line")
    if text.count(".") != 1:
        problems.append("pitch must hold exactly one sentence")
    if not stripped.endswith("."):
        problems.append("pitch must end with a full stop")
    return problems


def check_structure(text):
    """Return structure problems: named invention, mechanism, payoff.

    A valid pitch opens with a named invention, carries an absurd
    mechanism in the middle, and closes with a payoff clause that says
    what the annoyance becomes.
    """
    problems = []
    if not text.startswith("The "):
        problems.append("pitch must open with a named invention")
    if ", a " not in text and ", an " not in text:
        problems.append("pitch must introduce the invention after its name")
    if ", so " not in text:
        problems.append("pitch must close with a payoff clause")
    return problems


def write_pitch(text, destination):
    """Write the pitch to destination, creating its parent directory."""
    destination.parent.mkdir(parents=True, exist_ok=True)
    try:
        destination.write_text(text, encoding="utf-8")
    except OSError as write_err:
        raise RuntimeError(
            f"failed to write {destination}: {write_err}"
        ) from write_err
    return destination


def report_table(ranked):
    """Build the human-readable tournament table lines."""
    lines = [
        "tournament standings "
        "(total / absurdity / neatness / economy / freshness):"
    ]
    for position, item in enumerate(ranked, start=1):
        line = (
            f"{position}. {item['tag']}: {item['total']} "
            f"({item['absurdity']}/{item['neatness']}/"
            f"{item['economy']}/{item['freshness']}) "
            f"{len(item['text'])} chars"
        )
        lines.append(line)
    top_three = ranked[:3]
    lines.append("top three fixes:")
    for item in top_three:
        lines.append(f"- {item['tag']}: {item['fix_note']}")
    return lines


def main():
    """Run the tournament, gate the champion, and write the output file."""
    records = build_candidates()
    if len(records) == 0:
        print("gate failure: candidate list is empty")
        return 2
    ranked = rank_records(records)
    champion = ranked[0]
    if champion["total"] < CHAMPION_MIN_TOTAL:
        print(
            f"gate failure: champion total {champion['total']} "
            f"below bar {CHAMPION_MIN_TOTAL}"
        )
        return 3
    problems = check_pitch(champion["text"])
    problems.extend(check_structure(champion["text"]))
    if problems:
        for problem in problems:
            print(f"gate failure: {problem}")
        return 1
    for line in report_table(ranked):
        print(line)
    print(f"champion: {champion['tag']} ({len(champion['text'])} chars)")
    print(f"champion fix: {champion['fix_note']}")
    write_pitch(champion["text"], OUTPUT_PATH)
    print(f"wrote {OUTPUT_PATH}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
