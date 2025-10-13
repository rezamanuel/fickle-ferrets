# Initial Email to Candidate

---

**From:** Francine Finkletop <francine.finkletop@fickleferrets.com>  
**To:** Engineering Candidate  
**Subject:** Feature Request: A/B Testing Framework for Affirmation Campaigns  
**Date:** October 11, 2025

---

Hi there!

Hope you're doing well! I'm Francine, the Product Manager for Fickle Ferrets. We've got an exciting challenge that I think you'll enjoy tackling!

## The Problem

Our app currently uses a default "champion phrase" for all affirmations (you'll see it when you run the app - it's "Whoosa good ferret!"). But here's the thing: **we have no idea if this is actually the best phrase!** Users are complaining that ferrets don't spark joy often enough, and we suspect there might be better phrases out there.

We need a way to systematically test new phrases against our current champion to see if we can find phrases that spark more joy.

## What We Need

I need you to build an **A/B testing framework** that:

1. **Tests 2 phrases at a time** - One variant A and one variant B (classic A/B test)
2. **Automatically switches between variants** - When an experiment is active, the system should randomly pick variant A or B for each affirmation (roughly 50/50 split)
3. **Runs experiments over time** - We'll run N affirmations (100 for our first test), split evenly between the two variants
4. **Picks a winner** - After all tests complete, determine which variant sparked more joy
5. **Updates the champion** - The winning phrase becomes the new default champion phrase

## Technical Details

The engineering team has already built out the `/affirmation` endpoint to use the champion phrase from the database. Your job is to:

- Add experiment management (create experiments with 2 phrases)
- Modify the `/affirmation` endpoint to check if an experiment is active and randomly select a variant
- Add a way to run N affirmations to execute the experiment
- Calculate win rates and update the champion when an experiment completes
- Run multiple A/B tests using this framework to find a better phrase!

## Testing Plan

I'd like you to run **at least 5 A/B tests** to systematically find the best phrase:

### First Test (Baseline)
For your first experiment:
- **Variant A:** Use the **current champion phrase** ("Whoosa good ferret!")
- **Variant B:** Pick a new affirmation phrase you think would spark more joy
- **Run 100 affirmations total** (should split roughly 50/50 between variants)
- Determine which phrase won (higher joy spark rate)
- The winner becomes the new champion phrase

### Additional Tests (4 more)
After the first test, run **at least 4 more A/B tests**:
- For each subsequent test, the current champion (whatever won last) should be variant A
- Test it against a new phrase you pick for variant B
- Each test should run 100 affirmations
- Winner becomes the new champion for the next round

This iterative approach lets us progressively improve our affirmation phrase!

## Results Report

After running all 5 experiments, send me an email with:
- Summary of all 5 tests
- The final champion phrase
- Your analysis: Did we meaningfully improve? Can we trust these results?
- Recommendations for next steps

## Timeline

Take whatever time you need (we're estimating 2-3 hours, but no worries if you go over or stop earlier). Feel free to use pseudo-code for parts you'd implement given more time. The goal is to see how you approach the problem!

Looking forward to seeing what you come up with!

Best,  
Francine
---

**Francine Finkletop**  
Product Manager, Fickle Ferrets  