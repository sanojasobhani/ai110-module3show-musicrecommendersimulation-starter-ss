# 🎧 Model Card: Music Recommender Simulation

## 1. Model Name  

VibeMatch 1.0

A small music recommender that matches songs to a listener's taste.

---

## 2. Intended Use  

VibeMatch takes a short list of a person's music preferences and suggests songs from a small catalog. It looks at the genre, mood, and energy a person likes, plus whether they want acoustic music. Then it ranks the songs and shows the top matches with reasons.

This is a classroom project, not a real product. It is meant to teach how recommender systems turn preferences into scores. It should not be used to make real recommendations for real listeners.

This system is designed for:
- Learning how scoring and ranking work.
- Testing how different user tastes change the results.
- Exploring where bias shows up in simple AI systems.

This system should not be used for:
- Real music apps or real users.
- Any decision that actually matters to a person.
- Judging the quality of a song or an artist.

---

## 3. How the Model Works  

The model gives each song a score, then sorts songs from highest to lowest. The top few are the recommendations.

It looks at four things about each song:
- Genre: does it match the genre the user likes? (worth the most, up to 2 points)
- Mood: does it match the mood the user likes? (up to 1 point)
- Energy: how close is the song's energy to what the user wants? (up to 1.5 points; closer is better)
- Acoustic: does the song fit the user's acoustic preference? (up to 0.5 points)

The user tells the system four things: their favorite genre, favorite mood, a target energy level, and whether they like acoustic music.

The system adds up the points for each song and then scales the total to a 0.0–1.0 score so it is easy to read. The highest max score is 5.0 points, which becomes 1.00.

The catalog stores extra details like tempo, valence (happiness), and danceability, but the scoring does not use them yet. Only genre, mood, energy, and acoustic feed into the score.

---

## 4. Data  

The catalog is a small CSV file with 16 songs. Each song has an id, title, artist, genre, mood, energy, tempo, valence, danceability, and acousticness.

The songs cover a wide spread of genres: pop, lofi, rock, ambient, jazz, synthwave, indie pop, folk, disco, classical, hip hop, country, and r&b. Moods include happy, chill, intense, relaxed, focused, moody, and more.

I did not add or remove songs. I used the starter dataset as-is.

Limits of the data:
- It is very small. Most genres have only one song, so there is not much to choose from.
- Because the catalog is spread thin, a user with a less common taste may only have one real match, or none.
- The data does not include lyrics, language, artist popularity, or release year. So the system cannot understand any of those.

---

## 5. Strengths  

The system works well when a user's taste lines up with songs that actually exist in the catalog. For the three main profiles (Happy Pop, Chill Lofi, Intense Rock), the top pick was always a strong, obvious match with a score near 0.96.

What it does well:
- Clear tastes get clear results. A user who wants loud, happy pop gets loud, happy pop at the top.
- It explains itself. Every recommendation lists the reasons (genre match, energy alignment, and so on), so you can see why a song was picked.
- Opposite tastes get opposite results. A chill listener and a rock listener almost never see the same songs, which is exactly what you'd hope for.
- Energy matching feels right. Songs close to the user's target energy rise to the top, and this matched my intuition in every test.

---

## 6. Limitations and Bias 

Where the system struggles or behaves unfairly. 

One clear weakness I found during my adversarial testing is that the model has no concept of not having a match. It always returns a confident-looking, ranked list of songs even when the user's preferences match nothing in the catalog. When I fed it a profile asking for a metal/angry song (a genre that does not exist in the dataset), it still returned Storm Runner and Gym Hero with scores around 0.39, because every song automatically earns partial credit from the energy and acousticness dimensions regardless of genre or mood. This happens because the four features are scored independently and simply summed, so the system never notices that the two most meaningful signals (genre and mood) both failed to match. The same flaw makes the model blind to contradictory tastes: a request for a high-energy but "sad" song still produces a top pick, because the energy score carries the result while the impossible mood is silently ignored. As a result, a user can never tell the difference between a genuinely great recommendation and the least-bad fallback, which is a fairness problem for anyone whose taste falls outside the pop/lofi/rock core of the dataset.

Prompts:  

- Features it does not consider  
- Genres or moods that are underrepresented  
- Cases where the system overfits to one preference  
- Ways the scoring might unintentionally favor some users  

---

## 7. Evaluation  

How you checked whether the recommender behaved as expected. 

Profiles I tested: I built three everyday listener profiles and ran them all against the same 16-song catalog:

- High-Energy Pop: wants pop, happy mood, high energy (0.9), no acoustic tracks.
- Chill Lofi: wants lofi, chill mood, low energy (0.3), likes acoustic tracks.
- Deep Intense Rock: wants rock, intense mood, high energy (0.85), no acoustic tracks.

I also ran a set of edge case profiles (impossible genres, contradictory tastes) to stress-test the scoring, which is what turned up the weakness described in Section 6.

What surprised me: The thing I did not expect was that a song with the wrong mood could still land at #2 on a list. For the Happy Pop listener, the song Gym Hero keeps showing up near the top even though it is labeled "intense," not "happy." Here is the plain-language reason: the model gives points for four separate things — matching genre, matching mood, having similar energy, and matching the acoustic preference — and then just adds them up. Gym Hero is a pop song (big points), it is very high energy just like the listener wanted (big points), and it is not acoustic (small bonus). It only misses on mood. Three out of four wins is more than enough to beat most of the catalog, so the one thing it gets "wrong" (the mood) is quietly outvoted by everything it gets right. In other words, the system isn't broken — it is doing exactly what we told it to do — but it reveals that "energy" and "genre" matter far more in our scoring than "mood" does.

Profile-by-profile comparisons: Comparing the outputs two at a time shows that each preference dictionary really is steering the results, and in ways that make sense:

- High-Energy Pop vs. Chill Lofi: These two are near opposites and the outputs prove it. Happy Pop's top picks (Sunrise City, Gym Hero) are loud, fast, non-acoustic pop tracks; Chill Lofi's top picks (Library Rain, Midnight Coding) are quiet, slow, acoustic lofi tracks. This makes sense because the two profiles ask for opposite energy levels (0.9 vs 0.3) and opposite acoustic preferences, so almost no song can score well on both lists. This is the clearest sign the energy and acoustic settings are actually working.

- High-Energy Pop vs. Deep Intense Rock: These two look similar on paper (both want high energy, both avoid acoustic), and their lists do overlap, for example Gym Hero and Storm Runner appear on both. The difference comes from genre and mood: the Pop profile puts pop songs on top, while the Rock profile puts Storm Runner (rock/intense) at #1 because it matches both its genre and its mood. This makes sense: when two listeners agree on energy, genre and mood become the tie-breakers that separate their tastes.

- Chill Lofi vs. Deep Intense Rock: Another near-opposite pair, and there is almost no overlap in their top results. Lofi surfaces low-energy, acoustic, mellow songs; Rock surfaces high-energy, electric, aggressive songs. This is the expected result and a good validity check. a listener who wants calm background music and a listener who wants intense rock should almost never get the same recommendations, and they don't.

Prompts:  

- Which user profiles you tested  
- What you looked for in the recommendations  
- What surprised you  
- Any simple tests or comparisons you ran  

No need for numeric metrics unless you created some.

---

## 8. Future Work  

If I kept building this, here are three things I would change:

1. Add a "no good match" cutoff. Right now the system always returns five songs, even when nothing really fits. I would set a minimum score so it can say "no strong matches found" instead of guessing.

2. Make genre and mood smarter. Genre and mood are all-or-nothing today, so "pop" and "indie pop" count as a total mismatch. I would let similar genres and moods earn partial points.

3. Use the features I'm ignoring. The catalog already has tempo, valence, and danceability, but the score doesn't use them. Adding them would give a fuller picture of each song and better recommendations.

---

## 9. Personal Reflection  

This project showed me that a recommender is really just a scoring rule. It doesn't "understand" music at all. It just counts up points for the things we told it to care about and sorts the results.

The most interesting thing I found was the "Gym Hero" surprise. A song with the wrong mood kept showing up high on the list, not because of a bug, but because the rules I wrote quietly valued energy and genre more than mood. That taught me that bias in these systems often comes from the choices of the designer, not from anything obviously broken.

Now when I use a real music app, I think about it differently. Every "recommended for you" is the result of someone's scoring choices, and those choices decide what I do and don't get to hear.
