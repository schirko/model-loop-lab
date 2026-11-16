# Model Loop Lab

Can AI build better AI? This project runs a model-search loop on Colorado forest data (Forest Covertype), measures how much each generation improves, races it against Optuna and random guessing, and then shows a loop that breaks: models trained only on earlier models' synthetic data.

The findings are published as a static site at https://schirko.com/scott/model-loop-lab/.

## Run it

```
python -m pip install -r requirements.txt
copy .env.example .env
python -m pytest
python scripts/build_site.py
```

## Project documents

- `Site-Milestones.md`: the plan and where each milestone stands
- `Enhancements-and-Bugs.md`: the working list of what to do next
- `Beginning-End-Development-Guide.md`: how to rebuild the project from scratch, plus the full change log
