# 🎧 Model Card: Music Recommender Simulation

---

## 1. Model Name

**VibeFinder 1.0**

---

## 2. Goal / Task

VibeFinder suggests songs from a small catalog based on what a user says they like. You tell it your favorite genre, mood, and energy level, and it scores every song in the catalog against those preferences. The goal is to return the 5 best matches in order.

It doesn't learn from your listening history. It just takes what you tell it and runs the math.

---

## 3. Data Used

The catalog has 18 songs stored in a CSV file. Each song has these features: genre, mood, energy, tempo (BPM), valence, danceability, acousticness, studyability, and niche score.

There are 15 different genres and 12 different moods represented. Most genres only have one song — lofi has 3, pop has 2, and everything else has 1. The catalog skews slightly toward mid-to-high energy (average energy is 0.60 out of 1.0). There are no songs tagged "sad," "calm," or "upbeat," which means users who ask for those moods get nothing back for that preference.

---

## 4. Algorithm Summary

For every song, the system adds up points based on how well it matches the user's preferences.

It gives a flat bonus if the genre matches exactly (+1.00) and another flat bonus if the mood matches exactly (+1.50). Then it calculates how close each song is to the user's target on energy, valence, acousticness, studyability, and niche score. The closer the song is to the target, the more points it earns on that feature.

All the points get added together and the songs are sorted highest to lowest. The top 5 are returned as recommendations. The max possible score is 6.25.

The mood bonus is intentionally the biggest single bonus because the vibe of a song matters more than the genre label — a chill listener probably won't enjoy an intense song even if it's the right genre.

---

## 5. Observed Behavior / Biases

The biggest weakness is how genre matching works — it's exact string only, so "indie pop" and "pop" score as completely different even though they sound similar. This creates a filter bubble where users with hybrid tastes consistently get worse results than users who fit a single clean label. It showed up clearly in testing: Rooftop Lights (indie pop / happy) kept ranking below Gym Hero (pop / intense) for a happy-pop listener, which makes no sense musically. The catalog also only has one song for 13 of 15 genres, so the genre bonus basically just picks a predetermined winner with no competition. The mood vocabulary has the same problem — "relaxed" and "chill" score as total mismatches even though most listeners wouldn't tell the difference.

---

## 6. Evaluation Process

Six profiles were tested: High-Energy Pop, Chill Lofi, Deep Intense Rock, and three adversarial cases — a conflicted user who wanted high energy but a sad mood, an acoustic metalhead (metal genre but very high acousticness), and a blank slate with no genre or mood set at all.

The most surprising result was the Acoustic Metalhead profile. Even though that user wanted songs with a very organic, quiet sound, Iron Cathedral — a loud, distorted metal track — still ranked #1 by a huge margin. It won because it was the only metal song with an angry mood, so the label bonuses stacked up faster than the acousticness mismatch could drag it down. The system technically followed its own rules, but the output made no musical sense.

The Conflicted Energy profile (high energy + sad mood) was also revealing. Since no songs in the catalog are tagged as "sad," the mood bonus was wasted entirely and the system just fell back on genre, surfacing the two happiest pop songs for someone who asked for sad music. That result confirmed that the system has no way to handle a mood that doesn't exist in its vocabulary — it just silently ignores the request.

One logic experiment was also run: the genre weight was cut in half (2.00 → 1.00) and the energy weight was doubled (1.00 → 2.00). The max score stayed the same at 6.25. The main effect was that Rooftop Lights (indie pop / happy) finally jumped above Gym Hero (pop / intense) for the happy-pop listener — which felt more accurate. But it didn't fix the Acoustic Metalhead problem, because the two label bonuses together (2.50) still overwhelmed any numeric mismatch.

---

## 7. Intended Use and Non-Intended Use

**Intended use:** This is a classroom project. It's meant to show how a simple content-based recommender works — how you turn user preferences into scores and use those scores to rank results. It's for learning, not for real users.

**Not intended for:** Giving anyone actual music recommendations they'd rely on. The catalog is too small (18 songs), the genre matching is too rigid, and there's no personalization based on listening history. It also shouldn't be used as a model for how to build a production recommender — it skips collaborative filtering, audio embeddings, and basically everything that makes Spotify work.

---

## 8. Ideas for Improvement

1. **Fuzzy genre matching.** Instead of exact string comparison, group similar genres together (pop, indie pop, dance pop → all get partial credit). This would fix the filter bubble problem for hybrid-taste users.

2. **Expand the catalog.** With only 1 song per genre for 13 of 15 genres, there's no variety within a genre match. Adding 5–10 songs per genre would make the numeric features actually matter for ranking within a genre.

3. **Handle missing moods gracefully.** Right now if a user asks for "sad" and no songs are tagged sad, the system silently ignores it. It should either warn the user or fall back to the closest available mood (like "melancholic") instead of pretending the preference doesn't exist.

---

## 9. Personal Reflection

**Biggest learning moment:**
My biggest learning moment was seeing Iron Cathedral rank #1 for the Acoustic Metalhead profile even though the user specifically wanted acoustic-sounding music. I didn't expect the genre and mood bonuses to be strong enough to completely override a preference that was that specific. It made me realize that how you weight things matters just as much as what you're weighing.

**How AI tools helped, and when I had to double-check:**
AI tools helped a lot with the boilerplate stuff like setting up the scoring logic and explaining what each weight was doing. But I had to double-check whenever it made a change to the weights because the math had to still add up to the same max score. I also had to verify the output myself since the AI would say something "felt right" but the actual terminal results told a different story.

**What surprised me about simple algorithms feeling like recommendations:**
I was surprised that something as basic as matching a genre label and adding up a few numbers could actually return results that felt like real recommendations most of the time. For profiles like Chill Lofi and High-Energy Pop, the top results genuinely made sense without any complex logic behind them. It made me understand why content-based filtering was the starting point for real recommender systems before collaborative filtering took over.

**What I'd try next:**
I'd want to try fuzzy genre matching so that "indie pop" and "pop" actually share some credit instead of being treated as completely unrelated. I'd also expand the catalog a lot because right now most genres only have one song, which basically makes the genre bonus a guaranteed winner with no competition. Adding more songs per genre would let the numeric features do more of the actual ranking work.
