# Fickle Ferrets: A/B Testing Framework Assignment

## 📋 Assignment Overview

**Role:** Backend Engineer
**Time Estimate:** 2-3 hours (feel free to go beyond or stop at any time, switch to pseudo-code, etc)
**Focus Areas:** API Design, Backend Architecture, Thinking, Communication

## 🎯 What You're Building

You'll build an A/B testing framework that tests new affirmation phrases against the current champion phrase. The system currently uses a default "champion phrase" for all affirmations, but we need to discover if better phrases exist that spark more joy in our ferrets. When a new phrase wins an experiment, it becomes the new champion.

## 📧 The Scenario

You've received an email from Francine Finkletop, the Product Manager (see `INITIAL_EMAIL.md`), requesting an A/B testing framework. Read that email first.

## 🛠️ Your Task

Build a system that can:

1. **Create A/B test experiments** with 2 variants (variant A and variant B)
2. **Modify the `/affirmation` endpoint** to randomly pick variant A or B when an experiment is active
3. **Execute N affirmations** via a run endpoint that splits traffic roughly 50/50 between variants
4. **Store all results** in the database and calculate win rates for each variant
5. **Determine the winning phrase** and update the champion phrase when the experiment completes
6. **Provide API endpoints** to create experiments, run tests, and view results (JSON dump is great, no UI/UX)

## 📦 What You're Working With

**Existing Codebase:**
- FastAPI application with modular architecture
- SQLAlchemy 2.0 + SQLite database
- Async/await patterns throughout
- **Champion phrase system already implemented** - stored in database, seeds on startup
- Existing affirmation endpoint returns immediately (202) and processes in background
- Database already logs individual affirmation results to a local sqlite file. Data persistance isn't a point of focus.
- `GET /champion` endpoint available to view current champion phrase

**Key Files to Understand:**
- `app/api/routes.py` - API endpoints (including `/affirmation` and `/champion`)
- `app/services/ferret_service.py` - Business logic
- `app/db/models.py` - Database models
- `app/schemas/models.py` - Pydantic request/response models

## ✅ Requirements

### Functional Requirements

1. **Experiment Creation**
   - Accept 2 phrases: variant A and variant B
   - For the first test, variant A should be the current champion phrase
   - For subsequent tests, the current champion (winner of previous test) should be variant A
   - Generate unique experiment ID
   - Store experiment metadata (name, variant_a_phrase, variant_b_phrase, status, target_runs, etc)
   - Auto-activate experiment if no other experiment is currently active
   - Only one experiment can be active at a time

2. **Affirmation Endpoint Modification**
   - Modify the existing `POST /affirmation` endpoint to support A/B testing
   - **When NO active experiment exists:** Use the champion phrase from the database (current behavior)
   - **When an active experiment EXISTS:** Randomly select variant A or B (aim for roughly 50/50 split)
   - Track results in the existing `affirmation_results` table

3. **Experiment Execution**
   - Setup a way to run a given experiment N times
   - This should call the `/affirmation` endpoint N times
   - All use existing Spark Joy API integration (`ferret_service.process_affirmation_and_callback`). See Spark Joy API under resources.
   - Process asynchronously / as quickly as possible
   - Experiment automatically completes when target_runs is reached

4. **Results & Analysis**
   - Calculate win rate for each variant
   - Winner = variant with highest win rate
   - When experiment completes, update the champion phrase in the database with the winning phrase

### Technical Constraints

- ✅ Use existing FastAPI + SQLAlchemy stack
- ✅ Maintain async patterns
- ✅ SQLite is acceptable for database
- ✅ Follow existing code style and architecture
- ✅ Use existing `process_affirmation_and_callback` or adapt as needed, but use the same external API already in place

### Non-Requirements (Out of Scope)

- ❌ Authentication/authorization
- ❌ Advanced statistical tests
- ❌ Web UI (API-only is fine)
- ❌ Production deployment concerns
- ❌ Extensive test coverage

## 📝 Deliverables

### 1. Code Implementation

Submit your code as:
- **A new GitHub repository** (make it public or provide access to kyle.holgate@homesolutions.com)
- The repo should contain all your code changes
- The repo should also contain a `RESULTS_REPORT.md` file (see below)

**What we want to see:**
- Database schema changes/additions
- New API endpoints
- Business logic for experiments
- Proper async handling
- Code that's easy to understand and maintain

### 2. Email Report

Write an email response to Francine (the PM) with what we learned from all 5 experiments and recommendations for next steps.

**Your report should include:**
- Summary of all 5 A/B tests
- The final champion phrase after all tests
- Analysis: Did we meaningfully improve from the original? Can we trust the results?
- Any patterns or insights you noticed
- Recommendations for next steps

Write as if you were communicating with a real business user. I would strongly recommend against using an LLM to write this response. We want to see how you actually communicate in a business setting and your personality can be part of that. You don't have to communicate in corporate-speak, just be authentic.

**Save this as a markdown file** (e.g., `RESULTS_REPORT.md`) in the root of your GitHub repository.

## 🎓 Evaluation Criteria

We'll be looking at 

1. Does the code work?
2. Does it avoid complexity? Is it easy to understand and maintain? (note - this is not the same thing as code being as concise as possible)
3. Is the email response communicated well?

"Your job as a developer is not just to create code that you can work with easily, but to create code that others can also work with easily."

## 💡 Hints & Tips

**You may use any and all code-assist tools**. ChatGPT, Claude, Gemini, etc. Everything is fair game.

The goal of this case is to simulate a real working environment where you will have access to these tools. You'll be judged on the quality of your solution. Guiding an LLM to creating an elegant solution is just as valuable as manually typing it yourself. We're looking to hire someone to solve problems more than we are "writing code".

## 🚀 Getting Started

View the `README.md` file for more details on starting the existing app. Here's a recommended path for tackling this case - 

1. **Setup the codebase**
   ```bash
   git clone <repo-url>
   cd fickle-ferrets
   uv sync
   uv run python -m app.main
   ```

2. **Explore existing endpoints**
   - Visit http://localhost:8000/docs
   - Try the existing `/affirmation` endpoint
   - Try the `/champion` endpoint to see the current champion phrase
   - Check `/affirmations/history` to see stored results

3. **Read the code**
   - Understand how current affirmations flow through the system
   - Look at the `ChampionPhrase` model and how it's seeded on startup
   - See how `/affirmation` endpoint pulls from the champion phrase
   - Check how background tasks work

4. **Design your solution**
   - Sketch out your API endpoints for experiments
   - Plan your database schema (Experiment model, how to track which variant was used, etc)
   - Think about how to modify `/affirmation`

6. **Run the actual experiments**
   - **First Test:** Test the current champion ("Whoosa good ferret!") as variant A vs a new phrase you pick as variant B
   - Execute 100 affirmations (roughly 50 for variant A, 50 for variant B)
   - Analyze the results (which variant won?)
   - Verify the winning phrase became the new champion
   - **Run 4 more tests:** For each test, use the current champion as variant A and test against a new phrase as variant B
   - After completing all 5 tests, you should have a clear progression of winners
   - Write your email report summarizing all 5 experiments

## ❓ Questions & Assumptions

If something is unclear, make a reasonable assumption and document it in your email. We're interested in seeing how you think through ambiguity.

## 📚 Resources

- FastAPI Docs: https://fastapi.tiangolo.com
- SQLAlchemy 2.0 Docs: https://docs.sqlalchemy.org
- Current API Docs: http://localhost:8000/docs (when running)
- Spark Joy API: This is an endpoint setup specifically for this case. You can POST a string to `https://spark-joy.local-services.workers.dev/spark` and get a result. The API works as follows - 
   1. Takes a string input and converts it to a probability 0-1
   2. Do a random draw of that given probability and return a result (True for sparked joy, False for not)

   So the same string passed in will always have the same probability, but the results will vary unless the probability ends up being 0 or 1 (very unlikely). If a string's probability is 0.5, you would expect an even split between true and false responses given a big enough sample.

## 🎉 Good Luck!

We're excited to see your solution!

Remember: There's no single "right answer" - we want to see your thought process and technical decision-making.

---

**Questions?** Email: kyle.holgate@homesolutions.com

