# 🎧 Model Card: Music Recommender Simulation

## 1. Model Name  

Give your model a short, descriptive name.  
Example: **VibeFinder 1.0**  

---

## 2. Intended Use  

Describe what your recommender is designed to do and who it is for. 

Prompts:  

- What kind of recommendations does it generate  
- What assumptions does it make about the user  
- Is this for real users or classroom exploration  

---

## 3. How the Model Works  

Explain your scoring approach in simple language.  

Prompts:  

- What features of each song are used (genre, energy, mood, etc.)  
- What user preferences are considered  
- How does the model turn those into a score  
- What changes did you make from the starter logic  

Avoid code here. Pretend you are explaining the idea to a friend who does not program.

---

## 4. Data  

Describe the dataset the model uses.  

Prompts:  

- How many songs are in the catalog  
- What genres or moods are represented  
- Did you add or remove data  
- Are there parts of musical taste missing in the dataset  

---

## 5. Strengths  

Where does your system seem to work well  

Prompts:  

- User types for which it gives reasonable results  
- Any patterns you think your scoring captures correctly  
- Cases where the recommendations matched your intuition  

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

Ideas for how you would improve the model next.  

Prompts:  

- Additional features or preferences  
- Better ways to explain recommendations  
- Improving diversity among the top results  
- Handling more complex user tastes  

---

## 9. Personal Reflection  

A few sentences about your experience.  

Prompts:  

- What you learned about recommender systems  
- Something unexpected or interesting you discovered  
- How this changed the way you think about music recommendation apps  
