# Model Loop Lab: Findings

Every conclusion from the project in one place, newest notebook last. If you are new to the project or to data science, read "Start here" and the word list first. Each finding gives what we were looking for, the key numbers, what it means, and what's next. The notebook step behind each one is named in brackets, and every number comes from that step's saved output.

This document grows as each notebook is finished. **Status: notebook 01 of 4 finished.**

## Start here: the project in plain English

**The question.** New AI systems are increasingly built with help from older ones. Can a program design, test and improve its own models, getting better each round? And what happens when models learn from data that other models made up, instead of from the real world?

**The data.** The Forest Covertype dataset: 581,012 plots of the Roosevelt National Forest in northern Colorado, each a square about 30 meters on a side. Each plot is described only by map measurements (elevation, slope, distance to water, roads and past fires, wilderness area and soil type), and labeled with which of seven tree covers grows there.

**What's been built so far.** A fair way to test models (the same 5,000 plots, never seen during training, score everything) and a baseline: how well a plain decision tree does with no tuning at all.

**The answer so far.** A plain decision tree gets **77.2%** of new plots right, against 48.8% for always guessing the most common tree. It memorizes its training plots, and it mixes up trees that grow in the same places. Those two weaknesses are what the improvement loop in notebook 02 has to fix.

## Words used in this document

| Term | What it means here |
| --- | --- |
| **Model** | A set of rules learned from data that turns a plot's map measurements into a guess of which trees grow there. |
| **Decision tree** | A model that asks a chain of yes/no questions ("Is the elevation above 3,000 m?") until it reaches an answer. Each final answer is a **leaf**. |
| **Accuracy** | The share of plots the model labels correctly. |
| **Held-out plots** | 5,000 plots set aside and never shown to a model while it learns. Every score comes from these same plots. This is the fair test. |
| **Baseline** | The score of a plain model with no tuning: the number to beat. |
| **Overfitting** | Memorizing the training plots instead of learning patterns that carry over to new ones. Shows up as a big gap between the training score and the held-out score. |
| **Recall** | Of the plots that really are a given cover type, the share the model found. |
| **Precision** | Of the plots the model called a given cover type, the share that really were. |
| **Stratified sample** | A sample drawn so every cover type keeps the same share it has in the full data. |

## The short version, in numbers

A plain decision tree, scored on 5,000 forest plots it never saw, is right **77.2%** of the time. Always guessing the most common tree is right 48.8% of the time, so the map measurements are worth about 28 points. The tree scores 100% on its own training plots, a 23-point overfitting gap. It is weakest on Aspen (44% found) and Douglas-fir (52%), and its mistakes are mostly between neighbors: Spruce/fir and Lodgepole pine swap with each other, and Aspen is often called Lodgepole pine.

| # | Finding | Key number | Notebook |
| --- | --- | --- | --- |
| 1 | The forest is lopsided | 85% of plots are two cover types | 01, Step 2 |
| 2 | The test is fair | 15,000 training / 5,000 held-out plots, none in both | 01, Steps 3–4, 6 |
| 3 | Map measurements carry real information | 77.2% vs 48.8% for guessing | 01, Step 5 |
| 4 | The plain tree memorized its training plots | 100% on training plots vs 77.2% held out | 01, Step 7 |
| 5 | Aspen and Douglas-fir are the weak spots | 44% and 52% found | 01, Step 8 |
| 6 | The mistakes are between neighbors | 21% of Spruce/fir called Lodgepole pine | 01, Step 9 |

## Notebook 01: Data and baseline

### 1. The forest is lopsided

**What we were looking for.** How common each of the seven cover types is, because an uneven mix changes what an accuracy number means.

**Key numbers.** Lodgepole pine is 48.8% of all 581,012 plots and Spruce/fir is 36.5%: together 85%. Cottonwood/willow is 0.47% (2,747 plots).

**What it means.** A model can score well by getting the two big cover types right and ignoring the rest. Overall accuracy has to be read alongside results for each cover type (finding 5).

**What's next.** Take a smaller sample for the loops without losing the rare cover types. [Notebook 01, Step 2]

### 2. The test is fair

**What we were looking for.** A sample small enough to train hundreds of models quickly, a split where no plot is on both sides, and scoring that gives the same answer every time.

**Key numbers.** A 20,000-plot stratified sample: every cover type's share matches the full data to within a hundredth of a percent (Cottonwood/willow keeps its 0.47%, 94 plots). 15,000 training plots, 5,000 held out, 0 in both. Scoring the same model twice gives an identical number, and the model passed in is never changed.

**What it means.** Every model in every notebook is judged on exactly the same 5,000 plots. A better score means a better model, not a luckier split.

**What's next.** Score the simplest possible "model" and a plain tree. [Notebook 01, Steps 3, 4 and 6]

### 3. Map measurements carry real information

**What we were looking for.** The floor (always guessing the most common cover type) and how far a real model rises above it.

**Key numbers.** Always guessing Lodgepole pine: **48.8%**. A plain decision tree with every setting at its default: **77.2%**.

**What it means.** The 28-point gap is what elevation, soil and the other map features tell us about which trees grow where.

**What's next.** Look at how the tree got there, and whether it learned or memorized. [Notebook 01, Step 5]

### 4. The plain tree memorized its training plots

**What we were looking for.** The baseline, and whether the tree learned patterns that carry over to new plots.

**Key numbers.** **77.2%** on held-out plots (wrong on 1,141 of 5,000). **100%** on its own 15,000 training plots. The tree is 33 questions deep with 2,341 leaves, about one final answer for every six training plots.

**What it means.** The tree kept asking questions until every training plot was sorted, building many final answers for single, unusual plots. The 23-point drop to new plots is overfitting. Settings that stop a tree memorizing (a maximum depth, a minimum number of plots per leaf) and models that average many trees are exactly what the loop in notebook 02 can try.

**What's next.** Break the baseline down by cover type. [Notebook 01, Step 7]

### 5. Aspen and Douglas-fir are the weak spots

**What we were looking for.** Which cover types the baseline finds and which it misses.

**Key numbers.** Share of each cover type found (recall), on the held-out plots:

| Cover type | Held-out plots | Found | Recall |
| --- | --- | --- | --- |
| Lodgepole pine | 2,438 | 1,958 | 80.3% |
| Ponderosa pine | 308 | 239 | 77.6% |
| Krummholz | 177 | 136 | 76.8% |
| Spruce/fir | 1,823 | 1,397 | 76.6% |
| Cottonwood/willow | 23 | 15 | 65.2% |
| Douglas-fir | 149 | 78 | 52.3% |
| Aspen | 82 | 36 | 43.9% |

**What it means.** The common cover types sit near the overall score. Aspen is the clearest problem: the tree finds fewer than half of the real Aspen plots, and when it says Aspen it is right only 44% of the time. Rarity isn't the whole story, though: Krummholz is rare too and does as well as the common types. With only 23 Cottonwood/willow plots held out, each one moves its recall by more than 4 points, so its rate is rough.

**What's next.** See what each cover type is mistaken for. [Notebook 01, Step 8]

### 6. The mistakes are between neighbors

**What we were looking for.** Patterns in the mistakes: which cover types get called which.

**Key numbers.** 21% of Spruce/fir plots are called Lodgepole pine, and 16% of Lodgepole pine plots are called Spruce/fir. 44% of Aspen plots are called Lodgepole pine. 30% of Douglas-fir and 26% of Cottonwood/willow plots are called Ponderosa pine. Krummholz is only ever confused with Spruce/fir (20%).

**What it means.** The mistakes fall between cover types that share elevations and soils. Because Spruce/fir and Lodgepole pine are 85% of the forest, that one pair causes most of the 1,141 mistakes. Krummholz, the stunted trees at treeline, has a single look-alike just below it on the mountain, which is why it does well despite being rare. A model that separates Spruce/fir from Lodgepole pine even a little better will raise the overall score more than anything else.

**What's next.** Notebook 02: can an improvement loop beat 77.2% by fixing the overfitting and separating the neighbors? [Notebook 01, Step 9]

## Notebook 02: The evolution loop

Findings will be added here when notebook 02 is finished.

## Notebook 03: The search race

Findings will be added here when notebook 03 is finished.

## Notebook 04: Model collapse

Findings will be added here when notebook 04 is finished.
