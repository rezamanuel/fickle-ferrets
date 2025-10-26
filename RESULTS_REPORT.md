---

**From:** Engineering Candidate
**To:** Francine Finkletop <francine.finkletop@fickleferrets.com>
**Subject:** RE: Feature Request: A/B Testing Framework for Affirmation Campaigns
**Date:** October 26, 2025

---

Hi Francine,

I've completed the A/B testing framework and run 5 experiments as requested. Here are the results:

## Experiment Summary

### Test 1: Baseline
- **Variant A:** "Whoosa good ferret!" (38.6% joy spark rate - 17/44)
- **Variant B:** "You Rock!" (80.4% joy spark rate - 45/56)
- **Winner:** Variant B - "You Rock!"
- **Total Affirmations:** 100

### Test 2
- **Variant A:** "You Rock!" (80.9% joy spark rate - 203/251)
- **Variant B:** "BOOOOOOOOOOOOOOOOO" (36.9% joy spark rate - 92/249)
- **Winner:** Variant A - "You Rock!"
- **Total Affirmations:** 500

### Test 3
- **Variant A:** "You Rock!" (79.4% joy spark rate - 189/238)
- **Variant B:** "Reza is an Excellent Choice for Home Solutions" (0.8% joy spark rate - 2/262)
- **Winner:** Variant A - "You Rock!"
- **Total Affirmations:** 500

### Test 4
- **Variant A:** "You Rock!" (82.6% joy spark rate - 228/276)
- **Variant B:** "Hi!" (80.8% joy spark rate - 181/224)
- **Winner:** Variant A - "You Rock!"
- **Total Affirmations:** 500

### Test 5
- **Variant A:** "You Rock!" (77.3% joy spark rate - 194/251)
- **Variant B:** "hbu-3jnja-c2ldsfa" (44.6% joy spark rate - 111/249)
- **Winner:** Variant A - "You Rock!"
- **Total Affirmations:** 500

## Final Champion Phrase

**"You Rock!"**

It looks like "You Rock!" really did well with the ferrets -- it had around an 80% rate of joy, and consistently outperformed other phrases. I noticed that longer phrases seemed to do worse in general, but we likely need a lot more testing to confirm this. I think our current sample size is too small.


A couple of observations: 
1. I initially tried asking the ferrets 1000 times instead of 500 per experiment, which ended up yielding errors. I might've overwhelemed the joy sparking API, so I ended up going with smaller experiments.

2. The initial requirements say that we don't want to run more than 1 experiment at once -- so if an experiment is running, let it finish before submitting a new one; the API will not accept experiment requests while one is underway. 

3. Feel free to reach out if you'd like me to walk you through how the system works! We probably want to compile a large dataset of phrases we think could spark joy, and queue up experiments to run through the data set. Let's make sure we leverage our ferret joy experts to contribute their knowledge!



Assumptions:

  - I modified the /affirmation endpoint to still switch to 50/50 while an experiment is running, but I opted to call its underlying service layer directly for the /experiment endpoint instead of calling the externally facing api.
  
   I think this makes the logic cleaner and easier to maintain. As a follow up, I would recommend actually not having the /affirmation endpoint switch to 50/50, since our company mission is to deliver joy to ferrets. Instead, I'd recommend using the best champion phrase so far, not whatever we happen to be testing at the moment in an experiment. This approach will result in more overall ferret joy.
   
   Let me know your thoughts!

   Best,
   - Reza

   PS: The Ferrets really did not like the phrase: 'Reza is an Excellent Choice for Home Solutions'. This is a little concerning -- can we setup a meeting with them? I'd like to hear any feedback they have.
