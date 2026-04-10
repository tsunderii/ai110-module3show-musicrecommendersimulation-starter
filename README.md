# 🎵 Music Recommender Simulation

## Project Summary

In this project you will build and explain a small music recommender system.

Your goal is to:

- Represent songs and a user "taste profile" as data
- Design a scoring rule that turns that data into recommendations
- Evaluate what your system gets right and wrong
- Reflect on how this mirrors real world AI recommenders

This version scores every song in an 18-song catalog against a user's declared preferences — genre, mood, energy, valence, acousticness, studyability, and niche score — using a weighted formula that rewards exact label matches and numeric proximity. It runs six different user profiles including three adversarial edge cases to stress-test the scoring logic, and outputs a ranked table with the full score breakdown for each result. A diversity penalty was also added so the same artist or genre can't dominate the top 5.

---

## How The System Works

In real-world reccomendation systems such as Spotify or YouTube, they combine collborative filtering, neutral audio enbeddedings, and natural language process on playlist names. These systems digest billions of implicit signals such as skips or replays and personalizes each user's sessions per listening session.

The music reccomender's priority is to focus on pure content based filter, not taking into account user history but instead just the individual the device is running on. It should be able to score each song directly against a declared preference profile -- being able to explain each score.

Song uses: genre, mood, energy, tempo_bpm, valence, danceability, and acousticness as its scoring features.

UserProfile stores: favorite_genre, favorite_mood, target_energy, and likes_acoustic — the declared preferences the recommender scores against.

Recommender computes a weighted score per song (exact-match bonus for genre/mood + proximity formula 1 - |difference| for numeric features), then sorts all songs by score descending and returns the top K.

The algorithm awards +2.00 for a genre match, +1.50 for a mood match, and up to +1.00/+0.75/+0.50 for energy, valence, and acousticness proximity respectively (max score: 6.25). A known bias is that the categorical matches dominate — a song nailing genre and mood (+3.50) will almost always outrank one that is a near-perfect numeric fit but misses both labels, which means great songs from adjacent genres (e.g., ambient when the user prefers lofi) tend to be underranked.


         data/songs.csv
               │
               ▼
    ┌─────────────────────┐
    │  List[Song] objects │  ← 10 songs, all attributes loaded
    └─────────────────────┘
               │
               │  + UserProfile (genre, mood, energy target)
               ▼
    ┌─────────────────────┐
    │   score_song()      │  ← runs once per song
    │   weighted formula  │  → float score + reason list
    └─────────────────────┘
               │
               ▼
    ┌─────────────────────┐
    │  recommend_songs()  │  ← sort all scores, slice top K
    └─────────────────────┘
               │
               ▼
    Top K (song, score, explanation) tuples → printed in main.py


---

## Getting Started

### Setup

1. Create a virtual environment (optional but recommended):

   ```bash
   python -m venv .venv
   source .venv/bin/activate      # Mac or Linux
   .venv\Scripts\activate         # Windows

2. Install dependencies

```bash
pip install -r requirements.txt
```

3. Run the app:

```bash
python -m src.main
```

### Running Tests

Run the starter tests with:

```bash
pytest
```

You can add more tests in `tests/test_recommender.py`.

---

## Sensitivity Test — Weight Shift (genre ÷2, energy ×2)

Changed in [src/recommender.py](src/recommender.py): genre bonus `2.00 → 1.00`, energy weight `1.00 → 2.00`. Max score stays 6.25.

**Key ranking changes:**

| Profile | Before | After | Better or just different? |
|---------|--------|-------|--------------------------|
| High-Energy Pop | #2 Gym Hero (pop/intense) | #2 Rooftop Lights (indie pop/happy) | **Better** — a happy song now beats an intense one |
| Chill Lofi | #3 Focus Flow (lofi/focused) | #3 Spacewalk Thoughts (ambient/chill) | Mixed — mood match wins over genre match |
| Acoustic Metalhead | Iron Cathedral wins by 3.74 pts | Iron Cathedral wins by 2.76 pts | Slightly better but still broken |
| Blank Slate | scores 2.30–2.43 | scores 3.18–3.38 | Same songs, just wider spread |

**Verdict:** The change made Profile 1 more intuitive (Rooftop Lights correctly jumps Gym Hero because energy and mood now matter more than an exact genre label). But it didn't fix the core problem in the Acoustic Metalhead case — the two label bonuses combined (2.50) still dwarf any numeric mismatch. The change is *more accurate* for the happy-pop listener, and *just different* everywhere else.

---

## Experiments You Tried

Three standard profiles and three adversarial/edge-case profiles were run. Results below show terminal output for each.

---
(Screenshots did not fit the entire output so I copy-pasted it instead)
### Profile 1 — High-Energy Pop

```
  PROFILE: High-Energy Pop
  Genre: pop  |  Mood: happy  |  Energy: 0.9

  #1  Sunrise City — Neon Echo         Score: 6.08 / 6.75  (pop / happy)
  #2  Gym Hero — Max Pulse             Score: 4.61 / 6.75  (pop / intense)
  #3  Rooftop Lights — Indigo Parade   Score: 3.83 / 6.75  (indie pop / happy)
  #4  Block Party — The Groove Coll.   Score: 2.60 / 6.75  (hip-hop / energetic)
  #5  Frequency Drop — Bass Theory     Score: 2.52 / 6.75  (electronic / energetic)
```

Sunrise City (#1) hit both genre and mood bonuses (+3.50) and nearly matched on every numeric axis, scoring 6.08/6.75. Gym Hero (#2) kept its genre match despite the wrong mood, confirming that a single categorical hit dominates numeric proximity. Rooftop Lights (#3) earned zero genre points ("indie pop" ≠ "pop") but its happy mood and strong numerics still outranked all unmatched tracks.

---

### Profile 2 — Chill Lofi

```
  PROFILE: Chill Lofi
  Genre: lofi  |  Mood: chill  |  Energy: 0.35

  #1  Library Rain — Paper Lanterns    Score: 6.21 / 6.75  (lofi / chill)
  #2  Midnight Coding — LoRoom         Score: 6.10 / 6.75  (lofi / chill)
  #3  Focus Flow — LoRoom              Score: 4.67 / 6.75  (lofi / focused)
  #4  Spacewalk Thoughts — Orbit Bloom Score: 4.04 / 6.75  (ambient / chill)
  #5  Coffee Shop Stories — Slow Stereo Score: 2.56 / 6.75 (jazz / relaxed)
```

The lofi catalog is well-represented (3 songs), so the top 2 slots are dominated by exact matches. Focus Flow at #3 gets genre points but misses mood ("focused" ≠ "chill"). Spacewalk Thoughts (#4) shows the ambiguity between "ambient" and "lofi" — it wins the mood match but loses the genre bonus, landing just below Focus Flow.

---

### Profile 3 — Deep Intense Rock

```
  PROFILE: Deep Intense Rock
  Genre: rock  |  Mood: intense  |  Energy: 0.92

  #1  Storm Runner — Voltline          Score: 6.15 / 6.75  (rock / intense)
  #2  Gym Hero — Max Pulse             Score: 3.86 / 6.75  (pop / intense)
  #3  Iron Cathedral — Vortex Hammer   Score: 2.52 / 6.75  (metal / angry)
  #4  Frequency Drop — Bass Theory     Score: 2.40 / 6.75  (electronic / energetic)
  #5  Block Party — The Groove Coll.   Score: 2.33 / 6.75  (hip-hop / energetic)
```

Only one rock song in the catalog (Storm Runner) gets the full genre+mood bonus. Gym Hero (#2) earns second purely on mood match — a pop song beating every metal/electronic track, illustrating how sparse catalog coverage can push adjacent genres to the top.

---

### [ADVERSARIAL] Profile 4 — Conflicted Energy (energy=0.9, mood=sad)

This profile requests high energy (0.9) but mood="sad" — a contradictory ask since high-energy songs in the catalog are tagged "intense," "energetic," or "happy," never "sad."

```
  PROFILE: Conflicted Energy (energy=0.9, mood=sad)
  Genre: pop  |  Mood: sad  |  Energy: 0.9

  #1  Gym Hero — Max Pulse             Score: 4.12 / 6.75  (pop / intense)
  #2  Sunrise City — Neon Echo         Score: 4.10 / 6.75  (pop / happy)
  #3  Storm Runner — Voltline          Score: 2.39 / 6.75  (rock / intense)
  #4  Iron Cathedral — Vortex Hammer   Score: 2.34 / 6.75  (metal / angry)
  #5  Night Drive Loop — Neon Echo     Score: 2.18 / 6.75  (synthwave / moody)
```

**Finding:** The mood bonus is completely wasted (no "sad" songs exist), so the system falls back on genre match only. The result is tonally incorrect — the recommender surfaces the two happiest pop songs (#1 Gym Hero, #2 Sunrise City) for a listener who asked for sad content. The genre weight dominates and overrides the mood signal entirely.

---

### [ADVERSARIAL] Profile 5 — Acoustic Metalhead (genre=metal, acousticness=0.95)

This profile wants metal + angry mood but also very high acousticness (0.95). The only metal song (Iron Cathedral) has acousticness=0.06 — a direct conflict.

```
  PROFILE: Acoustic Metalhead (genre=metal, acousticness=0.95)
  Genre: metal  |  Mood: angry  |  Energy: 0.95

  #1  Iron Cathedral — Vortex Hammer   Score: 5.75 / 6.75  (metal / angry)
  #2  Storm Runner — Voltline          Score: 2.01 / 6.75  (rock / intense)
  #3  Night Drive Loop — Neon Echo     Score: 1.88 / 6.75  (synthwave / moody)
  #4  Rainy Season Blues — The Hollow  Score: 1.85 / 6.75  (folk / melancholic)
  #5  Frequency Drop — Bass Theory     Score: 1.78 / 6.75  (electronic / energetic)
```

**Finding:** Iron Cathedral still ranks #1 despite scoring only +0.06 on acousticness, because the genre+mood bonuses (+3.50) massively outweigh the acousticness penalty (-0.89 × 0.50 = -0.45 from max). The gap between #1 (5.75) and #2 (2.01) is enormous — the categorical weights have "tricked" the system into recommending a song that almost perfectly contradicts the user's acousticness preference.

---

### [ADVERSARIAL] Profile 6 — Blank Slate (all 0.5, no genre/mood)

No genre, no mood, all numerics at 0.5. Tests whether the system degrades gracefully when it has no taste signal.

```
  PROFILE: Blank Slate (all 0.5, no genre/mood)
  Genre: (none)  |  Mood: (none)  |  Energy: 0.5

  #1  Velvet Evenings — Soulstice      Score: 2.43 / 6.75  (r&b / romantic)
  #2  Midnight Coding — LoRoom         Score: 2.40 / 6.75  (lofi / chill)
  #3  Dreamweaver — Pastel Haze        Score: 2.40 / 6.75  (dreampop / dreamy)
  #4  Focus Flow — LoRoom              Score: 2.31 / 6.75  (lofi / focused)
  #5  Golden Hour — Marigold           Score: 2.30 / 6.75  (soul / uplifting)
```

**Finding:** With no categorical bonuses available, scores compress into a narrow 2.30–2.43 band. The top 5 are essentially tied, and the winners are mid-energy, mid-valence tracks — a bias toward the "center" of the numeric space. The system does not crash but the recommendations are essentially random within that band; a real system would need fallback diversity logic here.

---

## Musical Intuition Check — Does Profile 1 Feel Right?

**Profile: High-Energy Pop** (`pop / happy / energy 0.9`)

Mostly yes — Sunrise City at #1 is exactly what you'd expect. But Gym Hero at #2 feels off: it's an intense gym track, not a happy pop song. Rooftop Lights at #3 actually sounds more like what a happy-pop listener would want, but it ranks lower because "indie pop" ≠ "pop" in exact-string matching, so it gets zero genre points.

### Why Sunrise City Ranked #1

It's the only song that hits **both** the genre and mood bonus at once:

```
Genre match  (pop == pop)      +2.00
Mood match   (happy == happy)  +1.50
Energy proximity               +0.92   (|0.82 - 0.90| = 0.08)
Valence proximity              +0.74   (|0.84 - 0.85| = 0.01)
Acousticness proximity         +0.46
Studyability + Niche           +0.45
──────────────────────────────────────
TOTAL                           6.08 / 6.75
```

The two label bonuses alone add up to 3.50 — more than half the max score — so any song that nails both labels is almost impossible to beat on numerics alone.

### Is the Genre Weight Too Strong?

A little. With genre at 2.00, Gym Hero (wrong mood, right genre) consistently beats Rooftop Lights (right mood, wrong genre label). If genre were dropped to 1.00, Rooftop Lights would jump above Gym Hero — which feels more intuitive for someone who asked for happy music. The bigger problem is the 18-song catalog: with only 1–2 songs per genre, the #1 slot is often locked in by whoever holds the exact label match.

---

## Limitations and Risks

- Only 18 songs across 14 genres — rarely more than 2 songs per genre, so variety is almost impossible
- Exact string matching treats "indie pop," "pop," and "dance pop" as completely different genres
- Mood labels aren't standardized — "relaxed," "chill," and "calm" would score as total mismatches even if they feel the same
- Categorical bonuses make up ~52% of the max score, so label accuracy matters more than numeric fit
- No diversity logic — same songs dominate every run of the same profile

---

## Reflection

Read and complete `model_card.md`:

[**Model Card**](model_card.md)

The biggest thing I learned is that recommenders don't actually "understand" music — they just do math on labeled data, so if the labels are wrong or missing, the whole result falls apart. Bias shows up really easily when certain genres or moods have more songs in the catalog, because that genre will almost always win even if it's not actually the best match. Building this made me realize that Spotify isn't recommending you songs so much as it's predicting what you won't skip, which is a completely different problem.


---

## 7. `model_card_template.md`

Combines reflection and model card framing from the Module 3 guidance. :contentReference[oaicite:2]{index=2}  

```markdown
# 🎧 Model Card - Music Recommender Simulation

## 1. Model Name

Music Estoric-ness Detector

---

## 2. Intended Use

This system suggests the top 5 songs from an 18-song catalog based on what a user says they like — genre, mood, and energy level. It's designed for classroom exploration to show how content-based filtering works. It's not meant for real users or production use.

---

## 3. How It Works (Short Explanation)

You tell the system your favorite genre, mood, and how high-energy you want the music to be. It goes through every song in the catalog and gives each one a score based on how closely it matches — songs that share your genre or mood get a flat bonus, and songs that are close to your energy and vibe get extra points too. Then it sorts everything highest to lowest and shows the top 5 with a breakdown of exactly why each song ranked where it did.

---

## 4. Data

The catalog has 18 songs in a CSV file covering 15 genres and 12 moods. Most genres only have one song — lofi has 3 and pop has 2, everything else is a single entry. The data reflects a general Western music taste but is missing moods people actually use a lot like sad, calm, or upbeat.

---

## 5. Strengths

The system works best when the user's preferences match cleanly to something in the catalog — the Chill Lofi and High-Energy Pop profiles both returned results that felt genuinely right. It's also fully transparent since every score is explained line by line so you can see exactly why a song ranked where it did. That level of explainability is something real recommenders like Spotify don't offer.

---

## 6. Limitations and Bias

Genre matching is exact string only so "indie pop" and "pop" score as completely unrelated even though they sound similar, which creates a filter bubble for anyone with hybrid taste. Most genres also only have one song so the genre bonus basically locks in a winner before any other features even matter. If this were a real product it would be unfair to listeners who don't fit neatly into a single label, which is most people.

---

## 7. Evaluation

Six profiles were tested — three normal ones and three adversarial edge cases designed to stress-test the logic. The adversarial profiles found two real issues: a user asking for sad music got the happiest songs in the catalog, and a user wanting acoustic metal still got a loud distorted track at #1 because the label bonuses were too strong. A weight shift experiment (genre ÷2, energy ×2) was also run which made some results more intuitive but didn't fix the core label-matching problem.

---

## 8. Future Work

- Switch to fuzzy genre matching so "indie pop," "pop," and "synth pop" share partial credit instead of scoring as completely different
- Expand the catalog to 5–10 songs per genre so numeric features actually determine the ranking within a genre instead of the label alone
- Add a mood fallback so if a user asks for "sad" and nothing matches, the system picks the closest available mood instead of silently ignoring it

---

## 9. Personal Reflection

The most surprising thing was how confident the output looked even when it was wrong — the Conflicted Energy profile returned solid-looking scores for songs that had nothing to do with what the user asked for, with no sign anything was off. Building this changed how I think about Spotify because I used to assume it matched songs to my taste, but really it's predicting what I won't skip, which is a way harder problem. Human judgment still matters a lot here because someone has to decide which features to measure and how much to weight them, and those choices shape every result the system ever gives.

