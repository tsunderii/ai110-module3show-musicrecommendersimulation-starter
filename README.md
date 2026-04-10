# 🎵 Music Recommender Simulation

## Project Summary

In this project you will build and explain a small music recommender system.

Your goal is to:

- Represent songs and a user "taste profile" as data
- Design a scoring rule that turns that data into recommendations
- Evaluate what your system gets right and wrong
- Reflect on how this mirrors real world AI recommenders

Replace this paragraph with your own summary of what your version does.

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

## Experiments You Tried

### Experiment 1 — Default pop/happy profile

![Recommendations 1-2](Screenshot%202026-04-09%20at%205.35.14%20PM.png)
![Recommendations 3-5](Screenshot%202026-04-09%20at%205.35.22%20PM.png)
![Song 5 detail](Screenshot%202026-04-09%20at%205.35.26%20PM.png)

Running the recommender with a `pop / happy / energy 0.8` profile ranked Sunrise City #1 with a near-perfect 6.20/6.25 because it hit both the genre and mood bonus (+3.50 combined), which almost no numeric score alone can overcome. Gym Hero ranked #2 despite having an "intense" mood — it still won the genre match (+2.00) and its energy/valence were close enough to hold second place, showing how a single categorical match can carry a song high even when mood is wrong. Rooftop Lights at #3 is the most interesting result: it's labeled "indie pop" not "pop" so it earned zero genre points, but its happy mood and strong numeric proximity still beat out every fully unmatched song. Songs #4 and #5 scored below 2.60 with no categorical matches at all, confirming that the system rarely surfaces a track without at least one genre or mood hit.

---

## Limitations and Risks

Summarize some limitations of your recommender.

Examples:

- It only works on a tiny catalog
- It does not understand lyrics or language
- It might over favor one genre or mood

You will go deeper on this in your model card.

---

## Reflection

Read and complete `model_card.md`:

[**Model Card**](model_card.md)

Write 1 to 2 paragraphs here about what you learned:

- about how recommenders turn data into predictions
- about where bias or unfairness could show up in systems like this


---

## 7. `model_card_template.md`

Combines reflection and model card framing from the Module 3 guidance. :contentReference[oaicite:2]{index=2}  

```markdown
# 🎧 Model Card - Music Recommender Simulation

## 1. Model Name

Give your recommender a name, for example:

> VibeFinder 1.0

---

## 2. Intended Use

- What is this system trying to do
- Who is it for

Example:

> This model suggests 3 to 5 songs from a small catalog based on a user's preferred genre, mood, and energy level. It is for classroom exploration only, not for real users.

---

## 3. How It Works (Short Explanation)

Describe your scoring logic in plain language.

- What features of each song does it consider
- What information about the user does it use
- How does it turn those into a number

Try to avoid code in this section, treat it like an explanation to a non programmer.

---

## 4. Data

Describe your dataset.

- How many songs are in `data/songs.csv`
- Did you add or remove any songs
- What kinds of genres or moods are represented
- Whose taste does this data mostly reflect

---

## 5. Strengths

Where does your recommender work well

You can think about:
- Situations where the top results "felt right"
- Particular user profiles it served well
- Simplicity or transparency benefits

---

## 6. Limitations and Bias

Where does your recommender struggle

Some prompts:
- Does it ignore some genres or moods
- Does it treat all users as if they have the same taste shape
- Is it biased toward high energy or one genre by default
- How could this be unfair if used in a real product

---

## 7. Evaluation

How did you check your system

Examples:
- You tried multiple user profiles and wrote down whether the results matched your expectations
- You compared your simulation to what a real app like Spotify or YouTube tends to recommend
- You wrote tests for your scoring logic

You do not need a numeric metric, but if you used one, explain what it measures.

---

## 8. Future Work

If you had more time, how would you improve this recommender

Examples:

- Add support for multiple users and "group vibe" recommendations
- Balance diversity of songs instead of always picking the closest match
- Use more features, like tempo ranges or lyric themes

---

## 9. Personal Reflection

A few sentences about what you learned:

- What surprised you about how your system behaved
- How did building this change how you think about real music recommenders
- Where do you think human judgment still matters, even if the model seems "smart"

