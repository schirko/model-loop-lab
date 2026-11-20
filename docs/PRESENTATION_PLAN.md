# Presentation plan: "Can AI build better AI?"

A story deck that walks through the whole project, one notebook at a time and one step at a time, for an audience that includes non-analysts: an interviewer, a hiring manager, a meetup. It is modeled on the Meat Price Explorer deck (`meat-prices/docs/PRESENTATION_PLAN.md` and `scott/meat-prices/presentation/`) and on the Life Expectancy Predictor's plain-English findings ("Start here" and the word list).

**Length:** 30 slides, about 20 minutes, plus a 4-slide appendix for questions. A 12-minute version uses only the slides marked **[core]**.

**Built in parts.** Part 1 (the opening and notebook 01, 13 slides including a "what's next" slide) is published now. Each notebook's slides are added when it is finished, so the deck always holds real results only.

**Formats:** one self-contained HTML page, PowerPoint with speaker notes, PDF, a zip of every slide as a PNG, and `cover.png` for the thumbnail. All live in `scott/model-loop-lab/presentation/` and are linked from a "The story, as a presentation" section on the project's overview page.

**Story arc:** the question → the words → the plan → **Notebook 01:** the data and a plain model → **Notebook 02:** a loop that builds better models → **Notebook 03:** is the loop better than the alternatives? → **Notebook 04:** a loop that makes models worse → the verdict → what's next.

**Numbers.** Notebook 01's numbers below are real (run on 2026-11-16). Numbers marked **[NB02 Step n]** and so on come from notebooks not yet run. They are filled in from the finished notebooks, never estimated, and every number is checked against its notebook before the deck is published.

---

## How every slide is built

Every slide follows the meat-prices pattern, so the audience always knows where they are:

| Part | What it is | Example |
|---|---|---|
| **Section label** | Small text at the top: the part of the talk and, inside a notebook, the step | `NOTEBOOK 01 · STEP 7` |
| **Headline** | One full sentence a non-analyst can read on its own. It states the finding, not the topic | "A plain decision tree gets 77% right, but it memorized its training plots." |
| **Visual** | One chart, diagram or table, taken from the notebook step named in the label | Step 7's score comparison |
| **Callouts** | Up to three big numbers, each with a one-line caption that says what the number means | **77.2%** / right on plots it has never seen |
| **Source line** | Small text at the bottom: data source and notebook step | "Forest Covertype (USFS/CSU); notebook 01, Step 7." |
| **Speaker notes** | What to say, in full sentences, written to be read aloud | (each slide below) |

**Section openers.** Each notebook opens with a slide showing a four-part progress bar (01 · 02 · 03 · 04) with the current notebook highlighted, the question it answers, and the list of its steps. This is how the audience follows the notebooks and steps through the talk.

**Look.** 16:9. The project site's palette: spruce green (`#2e6a4c`) for the project's own marks, the site's blue and orange chart series, light background. Newsreader for headlines, Public Sans for everything else, as on the site.

---

## Opening

### 1. Title **[core]**
- **Section label:** A DATA STORY · MACHINE LEARNING ON COLORADO FOREST DATA
- **Headline:** Can AI build better AI?
- **Subtitle:** A program that builds, tests and improves its own models, how far it gets, and where the idea breaks.
- **Byline:** Scott Schirkofsky · schirko.com/scott/model-loop-lab
- **Visual:** the overview page's generation strip (20 green bars rising), faint behind the title.
- **Say:** "You've probably heard that AI is now helping to build the next generation of AI. I wanted to see what that actually looks like, so I built a small version of it myself. Today I'll show you what happened, step by step: where it works, how well, and the one way it reliably falls apart."

### 2. The hook **[core]**
- **Section label:** THE QUESTION
- **Headline:** New AI models are increasingly built with help from older ones. Does that make them better, or worse?
- **Visual:** two small loop diagrams side by side. Left: "Build → Test on real data → Keep the best → Repeat" in green. Right: "Learn → Make up data → Learn from the made-up data → Repeat" in orange.
- **Callouts:** none.
- **Say:** "There are two very different loops hiding in that idea. In the first, a program keeps trying new models and keeps whichever scores best on real data. In the second, a model learns from data that an earlier model made up. The first should improve things. The second sounds harmless, but it isn't. This project builds both and measures them."

### 3. Words used in this talk
- **Section label:** WORDS USED
- **Headline:** Nine words you'll hear, in plain English.
- **Visual:** a two-column table:

| Word | What it means here |
|---|---|
| **Model** | A set of rules learned from data that turns a plot's map measurements into a guess of which trees grow there |
| **Decision tree** | A model that asks a chain of yes/no questions ("Is the elevation above 3,000 m?") until it reaches an answer |
| **Accuracy** | The share of plots the model labels correctly |
| **Held-out plots** | 5,000 plots set aside and never shown to a model while it learns; every score comes from these |
| **Baseline** | The score of a plain model with no tuning: the number to beat |
| **Overfitting** | Memorizing the training plots instead of learning patterns that carry over to new ones |
| **Generation** | One round of the loop: build several models, score them, keep the best |
| **Synthetic data** | Made-up data produced by a model, meant to look like the real thing |
| **Model collapse** | What happens when models learn only from earlier models' made-up data and lose touch with reality |

- **Say:** "I'll use these nine words throughout. If you remember only two, make them 'held-out plots' and 'overfitting'. Every honest score in this talk comes from plots the model never saw, and overfitting is the problem the loop ends up attacking."

### 4. The plan: four notebooks, four questions **[core]**
- **Section label:** HOW THE PROJECT IS ORGANIZED
- **Headline:** The project is four notebooks, each answering one question.
- **Visual:** four numbered cards in a row, which become the progress bar on every section opener:
  - **01 · Data and baseline:** What does the data look like, and how good is a plain model?
  - **02 · The evolution loop:** Can a program find better models on its own?
  - **03 · The search race:** Is the loop better than standard tools, or than guessing?
  - **04 · Model collapse:** What happens when models learn only from other models?
- **Say:** "Everything I'll show comes from four Jupyter notebooks, and every step in them shows the code, its result and a plain-language reading. I'll go through them in order. The label at the top of each slide tells you which notebook and which step we're on."

---

## Notebook 01: Data and baseline

### 5. Section opener: Notebook 01 **[core]**
- **Section label:** NOTEBOOK 01 OF 4
- **Headline:** What does the data look like, and how good is a plain model?
- **Visual:** progress bar with 01 highlighted; the notebook's steps as a list:
  1. Setup
  2. Load the full dataset
  3. Take a 20,000-plot sample
  4. Split into training and held-out plots
  5. Score guessing and a plain tree
  6. Check that scoring is repeatable
  7. Record the baseline
  8. Results by cover type
  9. What gets confused with what
  10. Save the baseline for the website
- **Say:** "Notebook 01 sets up everything the later notebooks depend on: the data, a fair way to test, and the number every later model has to beat."

### 6. The data (Steps 1 and 2) **[core]**
- **Section label:** NOTEBOOK 01 · STEPS 1–2
- **Headline:** 581,012 plots of Colorado forest, described by map measurements alone.
- **Visual:** horizontal bar chart of the seven cover types by share of plots, largest first.
- **Callouts:**
  - **581,012** / 30 × 30 m plots in the Roosevelt National Forest
  - **54** / map features per plot: elevation, slope, distance to water and roads, soil type and more
  - **85%** / of plots are just two cover types: Lodgepole pine (48.8%) and Spruce/fir (36.5%)
- **Source line:** Forest Covertype data, U.S. Forest Service and Colorado State University, via the UCI repository; notebook 01, Step 2.
- **Say:** "The data is a classic: every plot is a square of forest about the size of a few tennis courts, described only by what you'd find on a map. No photos, no field visits. The job is to say which of seven tree covers grows there. Notice how lopsided it is. Two cover types make up 85% of the forest, and Cottonwood/willow is under half a percent. That will matter."

### 7. A fair test (Steps 3 and 4)
- **Section label:** NOTEBOOK 01 · STEPS 3–4
- **Headline:** Every model is scored on the same 5,000 plots it never saw while learning.
- **Visual:** a 20,000-square diagram split 75/25: 15,000 training plots (gray) and 5,000 held-out plots (green), with "no plot in both" marked.
- **Callouts:**
  - **20,000** / plots sampled so each model trains in seconds
  - **0.47%** / Cottonwood/willow's share in both the forest and the sample: the rare types are kept
  - **0** / plots in both the training and held-out sets
- **Source line:** notebook 01, Steps 3–4; `src/evaluate.py`.
- **Say:** "To run a loop that trains hundreds of models, I needed a smaller sample. I took 20,000 plots, drawn so every cover type keeps its exact share, rare ones included. Then I held back 5,000 that no model ever learns from. Every score in this talk comes from those same 5,000 plots, so the comparisons are fair."

### 8. Guessing versus a plain tree (Steps 5 and 6) **[core]**
- **Section label:** NOTEBOOK 01 · STEPS 5–6
- **Headline:** Map measurements alone get a plain tree to 77%. Guessing gets 49%.
- **Visual:** two bars: "Always guess Lodgepole pine" 48.8% (gray) and "Plain decision tree" 77.2% (green).
- **Callouts:**
  - **48.8%** / always guessing the most common type, Lodgepole pine
  - **77.2%** / a decision tree with every setting left at its default
  - **28 points** / how much the map features tell us about which trees grow where
- **Source line:** notebook 01, Step 5. Step 6 confirms the same model scores identically every time.
- **Say:** "Here's the floor. If you always guess the most common tree, you're right about half the time. A plain decision tree, which actually reads elevation, soil and so on, gets 77%. So the data really does carry information. I also checked that scoring the same model twice gives exactly the same number, because the loop will depend on that."

### 9. The baseline (Step 7) **[core]**
- **Section label:** NOTEBOOK 01 · STEP 7
- **Headline:** The plain tree scores 77.2% on new plots, but 100% on the plots it learned from.
- **Visual:** two bars: "Its own training plots" 100% and "Held-out plots" 77.2%, with the 23-point gap bracketed and labeled "overfitting".
- **Callouts:**
  - **77.2%** / the baseline: right on 3,859 of 5,000 plots it never saw
  - **100%** / on its own 15,000 training plots
  - **2,341** / leaves in a tree 33 questions deep: about one final answer for every six training plots
- **Source line:** notebook 01, Step 7.
- **Say:** "This is the number every later model has to beat: 77.2%. But look at the other bar. On the plots it learned from, the tree is perfect. It kept asking questions until every training plot was sorted, which took 33 levels and over two thousand final answers, many of them for a single unusual plot. That's overfitting: it memorized instead of learning. The gap between these two bars is exactly what the loop in notebook 02 can work on."

### 10. Results by cover type (Step 8)
- **Section label:** NOTEBOOK 01 · STEP 8
- **Headline:** The tree handles the common trees well and struggles with Aspen and Douglas-fir.
- **Visual:** table of the seven cover types, sorted by recall, with recall shaded green to amber:

| Cover type | Held-out plots | Found | Recall |
|---|---|---|---|
| Lodgepole pine | 2,438 | 1,958 | 80.3% |
| Ponderosa pine | 308 | 239 | 77.6% |
| Krummholz | 177 | 136 | 76.8% |
| Spruce/fir | 1,823 | 1,397 | 76.6% |
| Cottonwood/willow | 23 | 15 | 65.2% |
| Douglas-fir | 149 | 78 | 52.3% |
| Aspen | 82 | 36 | 43.9% |

- **Source line:** notebook 01, Step 8. Recall: of the plots that really are this type, the share the tree found.
- **Say:** "Breaking the score down by tree type, the two big ones sit near 80%. Aspen is the weak spot: the tree finds fewer than half of the real Aspen plots. But rarity isn't the whole story. Krummholz is rare too, and the tree finds it just fine. The next slide shows why."

### 11. What gets confused with what (Step 9) **[core]**
- **Section label:** NOTEBOOK 01 · STEP 9
- **Headline:** The mistakes are between neighbors: trees that grow at the same elevations on the same soils.
- **Visual:** Step 9's confusion chart (seven by seven, green), with the four largest off-diagonal squares circled.
- **Callouts:**
  - **21% / 16%** / Spruce/fir called Lodgepole pine, and the reverse: the two biggest types swap places
  - **44%** / of Aspen plots called Lodgepole pine; Aspen grows mixed into lodgepole stands
  - **1** / look-alike for Krummholz (Spruce/fir, just below it on the mountain), which is why it does well despite being rare
- **Source line:** notebook 01, Step 9.
- **Say:** "Read each row as 'the real tree' and each column as 'the model's answer'. The dark diagonal is right answers. The mistakes cluster in neighbor pairs. Spruce/fir and Lodgepole pine swap with each other, and because those two are 85% of the forest, that pair causes most of the errors. Aspen gets called Lodgepole pine as often as it gets called Aspen. Krummholz, the stunted trees at treeline, has only one neighbor to be confused with, so it does well. If a better model can separate Spruce/fir from Lodgepole pine even a little, the overall score jumps."

### 12. What notebook 01 sets up (Step 10)
- **Section label:** NOTEBOOK 01 · STEP 10
- **Headline:** The target for the loop: beat 77.2% by fixing overfitting and separating the neighbor pairs.
- **Visual:** a summary card with three rows: "Number to beat: 77.2%", "Weakness 1: memorizes training plots (100% vs 77.2%)", "Weakness 2: confuses neighbor cover types". Small note: "Saved to `results/web/baseline.json`; the website reads it from there."
- **Say:** "Notebook 01 ends by saving the baseline where the website can read it, so the site and the notebook can never disagree. And it hands notebook 02 a clear brief: beat 77.2%, and the two ways to do it are to stop memorizing and to tell the neighbors apart."

---

## Notebook 02: The evolution loop

### 13. Section opener: Notebook 02 **[core]**
- **Section label:** NOTEBOOK 02 OF 4
- **Headline:** Can a program find better models on its own?
- **Visual:** progress bar with 02 highlighted; the notebook's steps, listed from the finished notebook **[NB02 step titles]**.
- **Say:** "Notebook 02 is the heart of the project: a loop that designs models, tests them, and improves them with no person choosing the settings."

### 14. How the loop works **[core]**
- **Section label:** NOTEBOOK 02 · THE LOOP
- **Headline:** Build ten models, keep the best three, change them a little, repeat.
- **Visual:** circular four-step diagram: **Build** (ten models with different settings) → **Score** (accuracy on the held-out plots) → **Keep** (the best three survive) → **Change** (copies of the survivors with small random changes) → back to Build. "× 20 generations" in the center.
- **Callouts:**
  - **10** / models per generation
  - **3** / survivors that become the parents of the next generation
  - **20** / generations, about 200 models in all
- **Source line:** notebook 02 **[step]**; `src/evolve.py`.
- **Say:** "This is evolution in miniature. Each round, ten models compete. The best three survive and become the parents of the next round, with small random changes, like mutations. Nobody chooses the settings. The only thing guiding the loop is the score on real held-out plots."

### 15. What the loop is allowed to change
- **Section label:** NOTEBOOK 02 · STEP [n]
- **Headline:** The loop tunes four settings, and can swap one kind of model for another.
- **Visual:** a table of the settings the loop can change, each with its range and a plain-English meaning, taken from the finished notebook. Expected rows: model type (single decision tree, random forest, extra trees), number of trees, maximum depth (how many questions a tree may ask), minimum leaf size (how many plots a final answer must cover).
- **Say:** "These are the dials the loop can turn. Two of them, maximum depth and minimum leaf size, directly limit memorizing: they stop a tree from building a final answer for a single plot. The model type matters too. A random forest averages many trees, which smooths out the quirks any single tree memorizes."

### 16. Generation 1: where the loop starts **[NB02]**
- **Section label:** NOTEBOOK 02 · STEP [n]
- **Headline:** [From the finished notebook: how generation 1's random models compare with the 77.2% baseline.]
- **Visual:** dot plot of generation 1's ten models against the dashed baseline line.
- **Callouts:** best, median and worst of generation 1 **[NB02 Step n]**.
- **Say:** [Written from the result. Point: the loop starts from random settings, some worse than the baseline, and has to find its own way up.]

### 17. Twenty generations **[core] [NB02]**
- **Section label:** NOTEBOOK 02 · STEP [n]
- **Headline:** [From the finished notebook, for example "In 20 generations the loop climbs from X% to Y%, with no person choosing a setting."]
- **Visual:** the site's generations chart: best and median model per generation, dashed baseline at 77.2%.
- **Callouts:**
  - **[Y%]** / best model after 20 generations
  - **[+n points]** / above the 77.2% baseline
  - **[generation g]** / where improvement levels off
- **Source line:** notebook 02, Step [n]; also on the site's "The loop works" page.
- **Say:** [Written from the result. Cover: how fast it climbed, when it leveled off, and why the median rising matters as well as the best.]

### 18. Inside the winning model **[NB02]**
- **Section label:** NOTEBOOK 02 · STEP [n]
- **Headline:** [From the result: which settings won and what they have in common.]
- **Visual:** side-by-side settings: the baseline tree versus the winning model.
- **Say:** [Written from the result. Connect the winning settings back to slide 9's overfitting.]

### 19. Did it fix the weaknesses? **[core] [NB02]**
- **Section label:** NOTEBOOK 02 · STEP [n]
- **Headline:** [From the result: whether the training-versus-held-out gap shrank and whether Aspen and the Spruce/fir–Lodgepole pair improved.]
- **Visual:** two panels. Left: training versus held-out score, baseline versus winner. Right: recall by cover type, baseline versus winner (the slide 10 table as paired bars).
- **Say:** [Written from the result. This answers the brief from slide 12.]

---

## Notebook 03: The search race

### 20. Section opener: Notebook 03 **[core]**
- **Section label:** NOTEBOOK 03 OF 4
- **Headline:** Is the loop actually better than the alternatives?
- **Visual:** progress bar with 03 highlighted; the notebook's steps **[NB03 step titles]**.
- **Say:** "An improving loop is only interesting if it beats simpler ways of searching. So notebook 03 puts it in a race."

### 21. The rules of the race
- **Section label:** NOTEBOOK 03 · STEP [n]
- **Headline:** Three methods, the same 200-model budget, the same held-out plots.
- **Visual:** three lanes with icons and one-line descriptions:
  - **Evolution loop:** the loop from notebook 02
  - **Optuna:** a widely used tuning library that learns from each try which settings look promising
  - **Random guessing:** 200 random settings, no learning at all
- **Say:** "Each method gets exactly 200 tries and is scored on the same 5,000 plots. Random guessing is the control: if the loop can't beat it, the loop isn't really learning anything."

### 22. The race **[core] [NB03]**
- **Section label:** NOTEBOOK 03 · STEP [n]
- **Headline:** [From the result, for example which method reached the best score first, and by how much.]
- **Visual:** the site's race chart: best score found so far against models tried, one line per method.
- **Callouts:** final best score for each method, and how many tries each needed to pass a fixed mark **[NB03 Step n]**.
- **Source line:** notebook 03, Step [n]; also on the site's "The loop works" page.
- **Say:** [Written from the result. Cover: who got there first, who ended highest, and how close random guessing came.]

### 23. What the race shows
- **Section label:** NOTEBOOK 03 · STEP [n]
- **Headline:** [From the result: the honest conclusion about the hand-built loop versus a professional tool.]
- **Visual:** a three-row comparison: final score, tries to reach the mark, time taken **[NB03]**.
- **Say:** [Written from the result. If Optuna wins, say so plainly: the point of building the loop was to understand it, and the race shows what the professional tools add.]

---

## Notebook 04: Model collapse

### 24. Section opener: Notebook 04 **[core]**
- **Section label:** NOTEBOOK 04 OF 4
- **Headline:** What happens when models learn only from other models?
- **Visual:** progress bar with 04 highlighted; the notebook's steps **[NB04 step titles]**.
- **Say:** "Now the second loop from slide 2, the one that sounds harmless."

### 25. The copy-of-a-copy loop **[core]**
- **Section label:** NOTEBOOK 04 · THE LOOP
- **Headline:** Each generation learns only from data the previous generation made up.
- **Visual:** a four-step diagram: **Learn** the shape of the data → **Make up** 20,000 new plots → **Test** a classifier trained on them against real held-out plots → **Hand off** the made-up plots to the next generation. "× 10 generations" in the center. A photocopier icon: "a copy of a copy".
- **Source line:** notebook 04 **[step]**; `src/collapse.py`.
- **Say:** "Generation 0 learns from the real forest. Every generation after that never sees real data again; it learns only from what the one before it made up. It's a photocopy of a photocopy. At each round, I train a classifier on the made-up data and test it on real plots, to see how well each generation still knows the real forest."

### 26. Accuracy drains away **[core] [NB04]**
- **Section label:** NOTEBOOK 04 · STEP [n]
- **Headline:** [From the result, for example "Accuracy on real plots falls from X% to Y% in ten generations."]
- **Visual:** the site's accuracy-by-generation line chart.
- **Callouts:** generation 0, generation 10, and the generation where the drop is steepest **[NB04 Step n]**.
- **Source line:** notebook 04, Step [n]; also on the site's "Where loops break" page.
- **Say:** [Written from the result.]

### 27. Variety disappears first **[NB04]**
- **Section label:** NOTEBOOK 04 · STEP [n]
- **Headline:** [From the result: how much of the real data's variety is left after ten generations.]
- **Visual:** two panels: the variety-left line chart, and the elevation histogram, real data against generation 10.
- **Say:** [Written from the result. Point: each copy drifts toward the average and loses the unusual plots: the highest and lowest ground, and with it the rare cover types.]

### 28. Which trees vanish **[NB04]**
- **Section label:** NOTEBOOK 04 · STEP [n]
- **Headline:** [From the result: which cover types disappear from the made-up data first, likely the rare ones from slide 10.]
- **Visual:** recall by cover type at generation 0 versus generation 10.
- **Say:** [Written from the result. Tie back to slide 6: the rare types are the first to go.]

---

## Closing

### 29. The verdict **[core]**
- **Section label:** THE VERDICT
- **Headline:** AI can build better AI, as long as every step is checked against real data.
- **Visual:** a two-row verdict table:

| Loop | Checked against | Result |
|---|---|---|
| Evolution loop (notebooks 02–03) | Real held-out plots, every generation | Improved **[+n points]** over the baseline |
| Copy-of-a-copy loop (notebook 04) | Nothing real after generation 0 | Lost **[n points]** and most of its variety |

- **Say:** "Both loops are 'AI building AI'. The difference is what keeps them honest. The first one is scored against the real forest every single round, and it improves. The second one stops looking at reality, and it degrades. That's the real lesson: improvement loops work when they're anchored to real data, and fall apart when they feed on themselves."

### 30. What I'd do next
- **Section label:** WHAT'S NEXT
- **Headline:** Three ways to take this further.
- **Visual:** three cards:
  - **Mix real and made-up data:** how much real data per generation stops the collapse?
  - **A live demo:** a button on the site that runs five more generations while you watch
  - **A harder question:** apply the same loop to satellite imagery of land change
- **Say:** "The obvious follow-up is the middle ground: if each generation keeps even a little real data, does the collapse stop? That's the question people building large AI models care about most."

---

## Appendix (for questions)

### A1. Data and method
- **Headline:** Free public data, one fixed seed, every score from the same held-out plots.
- **Content:** Forest Covertype (581,012 plots, 54 features, 7 cover types). A 20,000-plot stratified sample, 15,000 for training and 5,000 held out. One random seed (42) for every step, so every result repeats exactly. Python, pandas, scikit-learn, Optuna.

### A2. Honesty checks
- **Headline:** Built so the results can be trusted, and re-run.
- **Content:** every score on plots the model never saw; scoring checked for repeatability (notebook 01, Step 6); **[n]** automated tests run on every change; notebooks run top to bottom from the terminal so every output is saved; the website reads results straight from files the notebooks write, so the site and notebooks can't disagree.

### A3. Limits
- **Headline:** What this project does not show.
- **Content:** one dataset, one kind of model family, a small search space; accuracy as the single score (rare cover types count for little in it); the collapse experiment uses a simple generator, not a large language model, so it shows the mechanism, not the size of the effect in real AI systems.

### A4. Links
- **Headline:** Everything is online.
- **Content:** project site, notebooks and code: schirko.com/scott/model-loop-lab and github.com/schirko/model-loop-lab.

---

## Notes for building it

- **Charts:** each notebook saves its charts as PNG files for the deck (enhancement E-030), so slides use the exact figures from the notebooks. Simple visuals (the loop diagrams, the two-bar comparisons, the verdict table) are rebuilt natively on the slide so they stay sharp and editable in PowerPoint.
- **Numbers:** every number comes from a notebook step named on its slide. Before publishing, each one is checked against its notebook, and the **[NB02]**, **[NB03]** and **[NB04]** placeholders must all be gone.
- **Plain language:** headlines a non-analyst can read on their own; every technical word is either in the slide 3 word list or explained where it appears.
- **Speaker notes:** written out in full on every slide, in the PowerPoint file and in the HTML version.
- **Check before publishing:** open every format, read every slide at full size, confirm the HTML works offline, and confirm the slide count on the overview page matches the deck.
