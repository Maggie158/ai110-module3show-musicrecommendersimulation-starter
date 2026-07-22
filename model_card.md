# 🎧 Model Card: Music Recommender Simulation

## 1. Model Name  

**VibeMatch 1.0**

---

## 2. Intended Use  

VibeMatch is a small content-based recommender: you tell it a genre, mood,
target energy, and whether you like acoustic songs, and it hands back a
ranked shortlist from an 18-song catalog with a plain-English reason for each
pick. It assumes the user can state their taste as a few simple structured
preferences up front — it has no listening history, no login, and no idea
what you actually played yesterday. This is a classroom exploration project
built to learn how recommenders turn data into predictions, not a
production system — it should not be used to make real recommendations for
real users, and it should never be the only signal a real product relies on.

---

## 3. How the Model Works  

Every song carries a genre, a mood, a 0–1 energy rating, and how acoustic vs.
produced it sounds. The user's taste profile states what genre and mood they
want, how much energy they're looking for, and whether they lean acoustic.
For each song, the system checks: does the genre match exactly (worth the
most points), does the mood match exactly (worth about half as much), how
close is the song's energy to what was asked for (a sliding partial-credit
score, not all-or-nothing), and does the acoustic vibe agree (a small bonus).
All of that gets added into one number per song. Every song in the catalog
gets a number this way, then they're sorted highest to lowest and the top
handful are shown, each with the specific reasons that earned it points — so
a listener can see *why* a song was suggested, not just that it was. The
starter code only returned the first few songs in file order with a fake
placeholder explanation; the real version actually scores and ranks every
song and generates its explanations from what actually matched.

---

## 4. Data  

The catalog has 18 songs (started at 10 — I added 8 more to widen the
variety). It spans 15 genres (pop, lofi, rock, ambient, jazz, synthwave,
indie pop, hip-hop, disco, soul, reggae, classical, synth-pop, country, r&b)
and 11 moods (happy, chill, intense, relaxed, moody, focused, melancholy,
dreamy, energetic, playful, romantic), so most genres are represented by
exactly one song. Each song also has tempo, valence, danceability, and
acousticness, but only energy and acousticness are actually used in scoring
today — tempo/valence/danceability are recorded but ignored. Missing from
the data entirely: lyrics or language, artist popularity, release era, and
any real listener behavior (plays, skips, likes) — everything here is a
one-time content tag, not something that updates from how people react to
the song.

---

## 5. Strengths  

The system is most convincing when a profile's genre, mood, and energy all
point the same direction — "Chill Lofi" and "Deep Intense Rock" both produce
confident, intuitive top-5s with a real gap between the winners and the
rest. It correctly gives two opposite-taste profiles completely
non-overlapping recommendation lists, which is the basic thing a
recommender has to get right. It also degrades gracefully rather than
breaking: when a requested genre doesn't exist in the catalog, or isn't
specified at all, the system quietly falls back to mood + energy and still
returns a reasonable pick instead of an empty list or an error. And because
every recommendation comes with its scoring reasons attached, it's easy to
audit — you can always see exactly which signals a pick did and didn't
satisfy, which is more transparent than most real black-box recommenders.

---

## 6. Limitations and Bias 

Where the system struggles or behaves unfairly. 

Prompts:  

- Features it does not consider  
- Genres or moods that are underrepresented  
- Cases where the system overfits to one preference  
- Ways the scoring might unintentionally favor some users  

**What I found during testing:** the system over-prioritizes genre because it's
worth 2x a mood match and any amount of energy closeness. This shows up
clearly in the "High-Energy Pop" test below — "Gym Hero" (pop, but *intense*
mood) outranks "Get Lucky" (disco, but a *happy* mood match) purely because
"Gym Hero" shares the pop genre tag. A user who cares more about vibe than
genre label would see this as a wrong answer. Mood matching is also brittle:
it's an exact string comparison, so a request for `mood: "sad"` never matches
the catalog's `"melancholy"` tag even though they're near-synonyms, silently
losing what should be a strong signal. Finally, the catalog is tiny (18
songs, 15 genres), so most genres have only one representative — the system
can't actually tell whether it likes "rock" or just likes "Storm Runner,"
the only rock song in the data.

---

## 7. Evaluation  

How you checked whether the recommender behaved as expected. 

Prompts:  

- Which user profiles you tested  
- What you looked for in the recommendations  
- What surprised you  
- Any simple tests or comparisons you ran  

No need for numeric metrics unless you created some.

### Profiles tested

I ran six profiles through `src/main.py` (`python -m src.main`): three
everyday tastes and three adversarial/edge cases designed to try to break the
scoring logic (see `PROFILES` in `main.py`).

```
=== High-Energy Pop ===
user_prefs = {'genre': 'pop', 'mood': 'happy', 'energy': 0.85, 'likes_acoustic': False}

Sunrise City - Score: 4.47
Because: genre match (+2.0), mood match (+1.0), energy closeness (+0.97), acoustic fit (+0.5)

Gym Hero - Score: 3.42
Because: genre match (+2.0), energy closeness (+0.92), acoustic fit (+0.5)

Get Lucky - Score: 2.46
Because: mood match (+1.0), energy closeness (+0.96), acoustic fit (+0.5)

Rooftop Lights - Score: 2.41
Because: mood match (+1.0), energy closeness (+0.91), acoustic fit (+0.5)

Storm Runner - Score: 1.44
Because: energy closeness (+0.94), acoustic fit (+0.5)


=== Chill Lofi ===
user_prefs = {'genre': 'lofi', 'mood': 'chill', 'energy': 0.3, 'likes_acoustic': True}

Library Rain - Score: 4.45
Because: genre match (+2.0), mood match (+1.0), energy closeness (+0.95), acoustic fit (+0.5)

Midnight Coding - Score: 4.38
Because: genre match (+2.0), mood match (+1.0), energy closeness (+0.88), acoustic fit (+0.5)

Focus Flow - Score: 3.40
Because: genre match (+2.0), energy closeness (+0.90), acoustic fit (+0.5)

Spacewalk Thoughts - Score: 2.48
Because: mood match (+1.0), energy closeness (+0.98), acoustic fit (+0.5)

Someone Like You - Score: 1.48
Because: energy closeness (+0.98), acoustic fit (+0.5)


=== Deep Intense Rock ===
user_prefs = {'genre': 'rock', 'mood': 'intense', 'energy': 0.95, 'likes_acoustic': False}

Storm Runner - Score: 4.46
Because: genre match (+2.0), mood match (+1.0), energy closeness (+0.96), acoustic fit (+0.5)

Gym Hero - Score: 2.48
Because: mood match (+1.0), energy closeness (+0.98), acoustic fit (+0.5)

HUMBLE. - Score: 2.17
Because: mood match (+1.0), energy closeness (+0.67), acoustic fit (+0.5)

Sunrise City - Score: 1.37
Because: energy closeness (+0.87), acoustic fit (+0.5)

Get Lucky - Score: 1.36
Because: energy closeness (+0.86), acoustic fit (+0.5)


=== Adversarial: Sad but High-Energy ===
user_prefs = {'genre': 'soul', 'mood': 'sad', 'energy': 0.95, 'likes_acoustic': False}

Someone Like You - Score: 2.33
Because: genre match (+2.0), energy closeness (+0.33)

Gym Hero - Score: 1.48
Because: energy closeness (+0.98), acoustic fit (+0.5)

Storm Runner - Score: 1.46
Because: energy closeness (+0.96), acoustic fit (+0.5)

Sunrise City - Score: 1.37
Because: energy closeness (+0.87), acoustic fit (+0.5)

Get Lucky - Score: 1.36
Because: energy closeness (+0.86), acoustic fit (+0.5)


=== Adversarial: Genre Not In Catalog ===
user_prefs = {'genre': 'metal', 'mood': 'intense', 'energy': 0.9, 'likes_acoustic': False}

Storm Runner - Score: 2.49
Because: mood match (+1.0), energy closeness (+0.99), acoustic fit (+0.5)

Gym Hero - Score: 2.47
Because: mood match (+1.0), energy closeness (+0.97), acoustic fit (+0.5)

HUMBLE. - Score: 2.22
Because: mood match (+1.0), energy closeness (+0.72), acoustic fit (+0.5)

Sunrise City - Score: 1.42
Because: energy closeness (+0.92), acoustic fit (+0.5)

Get Lucky - Score: 1.41
Because: energy closeness (+0.91), acoustic fit (+0.5)


=== Adversarial: No Genre Preference ===
user_prefs = {'mood': 'chill', 'energy': 0.5}

Midnight Coding - Score: 1.92
Because: mood match (+1.0), energy closeness (+0.92)

Library Rain - Score: 1.85
Because: mood match (+1.0), energy closeness (+0.85)

Spacewalk Thoughts - Score: 1.78
Because: mood match (+1.0), energy closeness (+0.78)

Adorn - Score: 0.95
Because: energy closeness (+0.95)

No Woman No Cry - Score: 0.92
Because: energy closeness (+0.92)
```

### Does it match intuition?

**High-Energy Pop** matches my intuition at the top: "Sunrise City" is
genuinely a happy, energetic pop song, so #1 feels right. But #2, "Gym Hero,"
is an *intense* pop song, not a happy one — in plain language: the system
put a pop song about gym motivation ahead of "Get Lucky," a happy disco song
that's a much closer vibe match, just because both are tagged "pop." A
non-programmer would say "why is the gym song here, I asked for happy
music?" — the answer is that in `score_song` (`src/recommender.py`), a
genre match alone is worth +2.0, more than a mood match (+1.0) plus a decent
chunk of energy closeness combined. Genre is acting like a bigger vote than
it should for a listener who cares about mood first.

### Comparisons between profile pairs

- **High-Energy Pop vs. Chill Lofi:** completely different top-5s with zero
  overlap — the EDM-adjacent pop profile pulls high-tempo, high-valence
  tracks, while the lofi profile pulls low-energy, high-acousticness tracks.
  This is the expected, "easy" case from the design phase and it worked.
- **Chill Lofi vs. Deep Intense Rock:** also zero overlap, and the score gap
  between #1 and #5 is much wider for rock (4.46 → 1.36) than lofi (4.45 →
  1.48), because there's only one rock song in the catalog — everything past
  it is a fallback on mood/energy alone, not a real "close second."
- **High-Energy Pop vs. "Sad but High-Energy" (adversarial):** the
  contradictory profile (sad mood, but energy 0.95) still returns
  "Someone Like You" at #1 — a *slow, melancholy* soul ballad — purely
  because its genre matches. In plain language: the user said "sad, but
  hit me with energy," and the system handed back a quiet ballad because
  it happens to share a genre tag, ignoring that its energy (0.28) is the
  opposite of what was asked. This is the clearest bias I found: genre can
  override a directly contradicted numeric preference.
- **"Genre Not In Catalog" vs. "No Genre Preference":** both fall back to
  mood + energy only, and both produce sensible top picks ("Storm Runner"
  for intense/0.9, "Midnight Coding" for chill/0.5) — this was the pleasant
  surprise. When genre can't contribute (either because it's missing or
  because it doesn't exist in the data), the system degrades gracefully
  instead of breaking or returning garbage.

### Experiment: reweighting genre vs. energy

I temporarily halved the genre weight (2.0 → 1.0) and doubled the energy
weight (`energy_score * 2`) in `score_song`, reran `High-Energy Pop`, then
reverted. Result: "Get Lucky" (mood match) moved from #3 (2.46) to #2 (3.42),
overtaking "Gym Hero" (genre match only), which dropped from #2 to #3. This
directly fixed the "Gym Hero ahead of Get Lucky" issue above — it's *more
accurate* to my intuition for this profile. But it didn't come free: rerunning
the "Sad but High-Energy" adversarial case under the same weights dropped
"Someone Like You" out of the top 5 entirely, since its only strength (genre
match) mattered less and its energy mismatch (0.28 vs. 0.95) mattered more —
arguably a *more honest* failure (it no longer confidently returns a wrong
answer), but it also means genre-based recommendations get noticeably weaker
everywhere else. I kept the original 2.0/1.0/energy weights as the shipped
recipe since halving genre traded one bias for a different one rather than
removing bias — see the Limitations and Bias section above.

---

## 8. Future Work  

Ideas for how you would improve the model next.  

Prompts:  

- Additional features or preferences  
- Better ways to explain recommendations  
- Improving diversity among the top results  
- Handling more complex user tastes  

1. **Fuzzy mood matching** — right now `mood: "sad"` never matches
   `"melancholy"` because it's exact-string comparison. Grouping synonymous
   moods (or using a small similarity lookup) would stop the system from
   silently losing a strong signal just because of wording.
2. **A diversity penalty** — nothing stops the top 5 from being dominated by
   one artist or genre once the catalog grows; penalizing repeats already in
   the results (Optional Challenge 3) would make the list feel less
   repetitive.
3. **Use the unscored features** — tempo, valence, and danceability are
   already in the data but contribute nothing to the score today; folding
   them in (even at low weight) would let the system distinguish songs that
   currently tie on genre/mood/energy.
4. **Rebalance weight vs. catalog size** — genre dominates partly because
   most genres have only one song, so a "genre match" is almost always
   really a "this specific song" match. A bigger, denser catalog would make
   the current weights behave more like they're intended to.

---

## 9. Personal Reflection  

A few sentences about your experience.  

Prompts:  

- What you learned about recommender systems  
- Something unexpected or interesting you discovered  
- How this changed the way you think about music recommendation apps  

The biggest learning moment was watching the "Gym Hero ahead of Get Lucky"
result show up in testing — I'd designed the genre/mood/energy weights on
paper and they looked reasonable, but only running real profiles through the
system revealed that a +2.0 genre match can silently out-vote a much better
mood match. That's the same mechanism behind real "filter bubbles": nobody
decided to over-favor genre, it just fell out of picking round numbers that
felt intuitive without testing the edge cases. AI was most useful for
generating diverse catalog rows quickly and for pressure-testing my user
profile ("does this actually separate intense rock from chill lofi?") before
I'd written any scoring code — but I had to double-check its math claims
myself, especially when I reweighted genre vs. energy and needed to confirm
the score changes it predicted actually matched what the code produced.
What surprised me most is how "smart" four weighted numbers and a sort can
feel from the outside — the explanations make it feel deliberate, even
though it's really just arithmetic. It made me trust real recommendation
apps a little less and understand their weird suggestions a little more:
"why do I keep getting this" is often just "one feature is weighted too
high," not some deep understanding of taste. If I extended this, I'd want to
try the diversity penalty and fuzzy mood matching from Future Work first,
since those are the two things that produced the clearest wrong-feeling
results in testing.
