# 🎵 Music Recommender Simulation

## Project Summary

In this project you will build and explain a small music recommender system.

Your goal is to:

- Represent songs and a user "taste profile" as data
- Design a scoring rule that turns that data into recommendations
- Evaluate what your system gets right and wrong
- Reflect on how this mirrors real world AI recommenders

My version is called **VibeMatch 1.0**. It takes a user's taste profile (favorite genre, favorite mood, target energy, and acoustic preference) and scores every song in a small catalog against it. Each song earns points for matching the genre, matching the mood, having similar energy, and fitting the acoustic preference. The songs are then sorted from best to worst, and the top five are shown with a short list of reasons for each pick. I tested it with three different listener profiles and a set of edge-case profiles to see where the scoring works well and where it breaks.

---

## How The System Works

Explain your design in plain language.

Some prompts to answer:

- What features does each `Song` use in your system
  - For example: genre, mood, energy, tempo
- What information does your `UserProfile` store
- How does your `Recommender` compute a score for each song
- How do you choose which songs to recommend

You can include a simple diagram or bullet list if helpful.

Songs in my system use genre, mood, energy, tempo/bpm, valence, and danceability. These features allow the system to compare songs to a user's taste profile. The UserProfile stores a few simple preferences: the user’s favorite genre, favorite mood, a preferred target energy level, and whether they prefer acoustic music. The recommender gives a song a higher score when it matches the user’s preferred genre and mood, and when its energy is close to the target energy value. It can also reward or penalize songs based on the user’s preference for acoustic sounds. In a simple version, this is done by adding points for matching attributes and using the energy difference as a penalty when a song is too far from the target. After scoring every song, the recommender sorts them by score from highest to lowest and picks the top results. This means the songs that best match the user’s profile are recommended first.

Algorithm Recipe (Finalized Point-Weighting Strategy)
The recommender computes a score for each song using a point-weighting system:

Criterion	Points	Condition
Genre Match	+2.0	Song genre = User's favorite genre
Mood Match	+1.0	Song mood = User's favorite mood
Energy Similarity	+0.0 to +1.5	Based on distance from target energy (max points at 0 distance)
Acousticness Preference	+0.5	Rewards matching acoustic preference (high or low)
Maximum Score	5.0 points	Normalized to 0.0–1.0 scale

Potential Biases & Limitations
Over-Prioritization of Genre (40% of max score):

Genre gets +2.0 out of 5.0 max points, meaning a perfect genre match can overshadow mood, energy, and acousticness.
Risk: A great pop song with low energy might rank higher than an amazing indie song with perfect energy match for a user who listens to both genres.

Binary Categorical Matching (Genre & Mood):

The system treats genre and mood as binary (match or no match) with no similarity gradation.
Risk: A user who likes "pop" won't get recommended "indie pop" or similar adjacent genres—they're scored as 0.

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

## Sample Recommendation Output

Paste a sample of your recommender's output here as a text block so a reader can see what it produces:

```
PS C:\Users\sanoj\OneDrive\Desktop\vs code\ai110-module3show-musicrecommendersimulation-starter-ss> python -m src.main                        
Loading songs from data/songs.csv...                                        
Successfully loaded 16 songs.        
                                                            
============================================================
                    TOP RECOMMENDATIONS                                                                                                      
============================================================                     
                                                     
1. Sunrise City - Neon Echo
   Score: 0.98 / 1.00
   Reasons:
     - Genre match: pop
     - Mood match: happy
     - Energy alignment: 1.47 pts (target: 0.8, song: 0.82)
     - Non-acoustic preference: 0.41 pts

2. Gym Hero - Max Pulse
   Score: 0.76 / 1.00
   Reasons:
     - Genre match: pop
     - Energy alignment: 1.30 pts (target: 0.8, song: 0.93)
     - Non-acoustic preference: 0.47 pts

3. Rooftop Lights - Indigo Parade
   Score: 0.55 / 1.00
   Reasons:
     - Mood match: happy
     - Energy alignment: 1.44 pts (target: 0.8, song: 0.76)
     - Non-acoustic preference: 0.33 pts

4. Concrete Glow - Northside Crew
   Score: 0.37 / 1.00
   Reasons:
     - Energy alignment: 1.44 pts (target: 0.8, song: 0.84)
     - Non-acoustic preference: 0.42 pts

5. Golden Skyline - The Brass Line
   Score: 0.36 / 1.00
   Reasons:
     - Energy alignment: 1.38 pts (target: 0.8, song: 0.88)
     - Non-acoustic preference: 0.44 pts

============================================================
```

```
============================================================
           TOP RECOMMENDATIONS - High-Energy Pop            
============================================================

1. Sunrise City - Neon Echo
   Score: 0.96 / 1.00
   Reasons:
     - Genre match: pop
     - Mood match: happy
     - Energy alignment: 1.38 pts (target: 0.9, song: 0.82)
     - Non-acoustic preference: 0.41 pts

2. Gym Hero - Max Pulse
   Score: 0.79 / 1.00
   Reasons:
     - Genre match: pop
     - Energy alignment: 1.46 pts (target: 0.9, song: 0.93)
     - Non-acoustic preference: 0.47 pts

3. Rooftop Lights - Indigo Parade
   Score: 0.52 / 1.00
   Reasons:
     - Mood match: happy
     - Energy alignment: 1.29 pts (target: 0.9, song: 0.76)
     - Non-acoustic preference: 0.33 pts

4. Storm Runner - Voltline
   Score: 0.39 / 1.00
   Reasons:
     - Energy alignment: 1.48 pts (target: 0.9, song: 0.91)
     - Non-acoustic preference: 0.45 pts

5. Golden Skyline - The Brass Line
   Score: 0.38 / 1.00
   Reasons:
     - Energy alignment: 1.47 pts (target: 0.9, song: 0.88)
     - Non-acoustic preference: 0.44 pts

============================================================

============================================================
              TOP RECOMMENDATIONS - Chill Lofi              
============================================================

1. Library Rain - Paper Lanterns
   Score: 0.97 / 1.00
   Reasons:
     - Genre match: lofi
     - Mood match: chill
     - Energy alignment: 1.42 pts (target: 0.3, song: 0.35)
     - Acousticness bonus: 0.43 pts

2. Midnight Coding - LoRoom
   Score: 0.94 / 1.00
   Reasons:
     - Genre match: lofi
     - Mood match: chill
     - Energy alignment: 1.32 pts (target: 0.3, song: 0.42)
     - Acousticness bonus: 0.35 pts

3. Focus Flow - LoRoom
   Score: 0.75 / 1.00
   Reasons:
     - Genre match: lofi
     - Energy alignment: 1.35 pts (target: 0.3, song: 0.4)
     - Acousticness bonus: 0.39 pts

4. Spacewalk Thoughts - Orbit Bloom
   Score: 0.59 / 1.00
   Reasons:
     - Mood match: chill
     - Energy alignment: 1.47 pts (target: 0.3, song: 0.28)
     - Acousticness bonus: 0.46 pts

5. Midnight Sonata - Elara Quinn
   Score: 0.39 / 1.00
   Reasons:
     - Energy alignment: 1.48 pts (target: 0.3, song: 0.29)
     - Acousticness bonus: 0.47 pts

============================================================

============================================================
          TOP RECOMMENDATIONS - Deep Intense Rock           
============================================================

1. Storm Runner - Voltline
   Score: 0.97 / 1.00
   Reasons:
     - Genre match: rock
     - Mood match: intense
     - Energy alignment: 1.41 pts (target: 0.85, song: 0.91)
     - Non-acoustic preference: 0.45 pts

2. Gym Hero - Max Pulse
   Score: 0.57 / 1.00
   Reasons:
     - Mood match: intense
     - Energy alignment: 1.38 pts (target: 0.85, song: 0.93)
     - Non-acoustic preference: 0.47 pts

3. Concrete Glow - Northside Crew
   Score: 0.38 / 1.00
   Reasons:
     - Energy alignment: 1.48 pts (target: 0.85, song: 0.84)
     - Non-acoustic preference: 0.42 pts

4. Golden Skyline - The Brass Line
   Score: 0.38 / 1.00
   Reasons:
     - Energy alignment: 1.46 pts (target: 0.85, song: 0.88)
     - Non-acoustic preference: 0.44 pts

5. Sunrise City - Neon Echo
   Score: 0.37 / 1.00
   Reasons:
     - Energy alignment: 1.46 pts (target: 0.85, song: 0.82)
     - Non-acoustic preference: 0.41 pts

============================================================
```

**Screenshot or video** *(optional)*: <!-- Insert a screenshot or demo video link here -->

---

## Experiments You Tried

Here are the experiments I ran:

1. Three user profiles: I built three listener profiles (High-Energy Pop, Chill Lofi, Deep Intense Rock) and ran them all against the same 16 songs. Each one produced a clearly different top list, which showed the preferences were actually steering the results. See the sample output above.

2. Weight shift (energy vs. genre): I doubled the weight on energy (1.5 to 3.0) and halved the weight on genre (2.0 to 1.0) to see how sensitive the rankings were. I also updated the max score to 5.5 so the math stayed valid and scores stayed between 0 and 1. Result: the top picks mostly stayed the same, but the middle of the lists shuffled. For the Chill Lofi user, the #3 spot flipped from a lofi song to an ambient one, because a near-perfect energy match now mattered more than a genre match. I kept the original weights and saved this version as a commented-out experiment in `src/recommender.py`.

3. Edge-case / adversarial profiles: I tried to trick the scorer with impossible and contradictory tastes, for example a "metal / angry" genre that doesn't exist, and a "high energy but sad" profile. The system never errors and always returns five confident-looking songs, even when nothing truly matches. This is the biggest weakness I found and is documented in the model card.

4. Different user types: Clear tastes (loud happy pop) gave clean, obvious results. Opposite tastes (chill lofi vs. intense rock) almost never shared songs. Unusual tastes outside the catalog got weak, misleading matches.

---

## Limitations and Risks

Some limitations of VibeMatch:

- Tiny catalog: Only 16 songs, and most genres have just one song. A user with an uncommon taste may get only one real match, or none.
- No "no match" option: The system always returns five songs, even when nothing fits. It can't tell the user "I don't have anything good for you."
- All-or-nothing genre and mood: "pop" and "indie pop" count as a total mismatch, even though they're close.
- Energy and genre outweigh mood: Because of how the points are set, a song with the wrong mood can still rank near the top (the "Gym Hero" effect).
- It doesn't understand music: No lyrics, no language, no artist popularity, no release year. It only compares the numbers and labels it's given.

I go deeper on these in the [model card](model_card.md).

---

## Reflection

Read and complete `model_card.md`:

[**Model Card**](model_card.md)

Building this taught me that a recommender is really just a scoring rule. It doesn't understand music at all. It turns preferences and song details into numbers, adds up points for the things I told it to care about, and sorts the results. The "prediction" is simply whichever song scored highest. Once I saw that, recommendations felt a lot less magical and a lot more like a set of choices someone made about what counts.

Using AI helped me fast track writing code, deciding cases, building examples profiles, etc etc, but I often needed to double check to make sure the AI wasn't going overboard, esp when it came to using Claude (I noticed Copilot did not overdo as much as Claude did).



