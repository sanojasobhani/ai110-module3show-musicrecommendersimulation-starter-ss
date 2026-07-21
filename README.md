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

**Screenshot or video** *(optional)*: <!-- Insert a screenshot or demo video link here -->

---

## Experiments You Tried

Use this section to document the experiments you ran. For example:

- What happened when you changed the weight on genre from 2.0 to 0.5
- What happened when you added tempo or valence to the score
- How did your system behave for different types of users

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



