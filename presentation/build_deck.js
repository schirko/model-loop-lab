// Builds presentation/out/model-loop-lab-story.pptx, the Model Loop Lab deck.
//
// The slide-by-slide plan is docs/PRESENTATION_PLAN.md. This file turns it into a
// PowerPoint with native text, native charts and full speaker notes. Every number
// below comes from a notebook step named on its slide. The deck grows as each
// notebook is finished; slides for notebooks 02 to 04 are added from their results.
//
// Run:  node presentation/build_deck.js   (then python presentation/make_formats.py)

const path = require("path");
const pptxgen = require("pptxgenjs");

const OUT = path.join(__dirname, "out", "model-loop-lab-story.pptx");
const ASSETS = path.join(__dirname, "assets");

const THEME = {
  name: "Model Loop Lab",
  headFontFace: "Cambria",
  bodyFontFace: "Calibri",
  colors: {
    dk1: "18201B", lt1: "FFFFFF", dk2: "1C2B23", lt2: "EEF3EF",
    accent1: "2E6A4C", accent2: "C98A1B", accent3: "8A928C",
    accent4: "7CC39D", accent5: "4A544D", accent6: "D9DED8",
    hlink: "2E6A4C", folHlink: "4A544D",
  },
};
// Hex copies for the options that only take hex (chart grid lines, chart colors).
const HEX = { spruce: "2E6A4C", amber: "C98A1B", gray: "8A928C", rule: "D9DED8", ink2: "4A544D", mint: "7CC39D" };

const pres = new pptxgen();
pres.layout = "LAYOUT_16x9"; // 10 x 5.625 in
pres.title = "Can AI build better AI?";
pres.author = "Scott Schirkofsky";
pres.subject = "Model Loop Lab: the story so far";
pres.theme = { headFontFace: THEME.headFontFace, bodyFontFace: THEME.bodyFontFace };
const C = pres.SchemeColor;

// ---------- Layouts ----------
pres.defineSlideMaster({
  title: "DARK",
  background: { color: C.text2 },
  objects: [],
  slideNumber: { x: 9.0, y: 5.2, w: 0.6, h: 0.3, color: C.accent4, fontSize: 10, align: "right" },
});
pres.defineSlideMaster({
  title: "CONTENT",
  background: { color: C.background1 },
  objects: [
    { placeholder: { options: { name: "label", type: "body", x: 0.5, y: 0.28, w: 9.0, h: 0.3, fontSize: 10, bold: true, color: C.accent1, charSpacing: 1, margin: 0 }, text: "" } },
    { placeholder: { options: { name: "title", type: "title", x: 0.5, y: 0.58, w: 9.0, h: 0.85, fontSize: 24, bold: true, color: C.text1, valign: "top", align: "left", margin: 0 }, text: "" } },
  ],
  slideNumber: { x: 9.0, y: 5.2, w: 0.6, h: 0.3, color: C.accent3, fontSize: 10, align: "right" },
});

let n = 0;
function content(section, label, title) {
  const s = pres.addSlide({ masterName: "CONTENT", sectionTitle: section });
  s.addText(label, { placeholder: "label" });
  s.addText(title, { placeholder: "title" });
  n += 1;
  return s;
}
function source(s, text) {
  s.addText(text, { x: 0.5, y: 5.17, w: 8.3, h: 0.3, fontSize: 10, color: C.accent3, margin: 0, isTextBox: true, objectName: "Source" });
}
// Big-number callouts stacked in a column on the right of a chart.
function callouts(s, items, x = 6.55, y = 1.6, w = 2.95) {
  const gap = 0.12;
  const h = (3.4 - gap * (items.length - 1)) / items.length;
  items.forEach(([big, caption], i) => {
    const yy = y + i * (h + gap);
    s.addShape(pres.shapes.ROUNDED_RECTANGLE, { x, y: yy, w, h, rectRadius: 0.08, fill: { color: C.background2 }, line: { color: C.background2 }, objectName: `Callout ${i + 1} card` });
    s.addText(big, { x: x + 0.18, y: yy + 0.1, w: w - 0.36, h: 0.5, fontFace: THEME.headFontFace, fontSize: 24, bold: true, color: C.accent1, margin: 0, isTextBox: true, objectName: `Callout ${i + 1} number` });
    s.addText(caption, { x: x + 0.18, y: yy + 0.6, w: w - 0.36, h: h - 0.7, fontSize: 11, color: C.text1, valign: "top", margin: 0, isTextBox: true, objectName: `Callout ${i + 1} caption` });
  });
}
const chartText = { catAxisLabelFontFace: "+mn-lt", valAxisLabelFontFace: "+mn-lt", dataLabelFontFace: "+mn-lt", titleFontFace: "+mn-lt",
  catAxisLabelColor: HEX.ink2, valAxisLabelColor: HEX.ink2, dataLabelColor: "18201B", catAxisLabelFontSize: 11, valAxisLabelFontSize: 10, dataLabelFontSize: 11 };

// ---------- 1. Title ----------
pres.addSection({ title: "Opening" });
{
  const s = pres.addSlide({ masterName: "DARK", sectionTitle: "Opening" }); n += 1;
  // the generation idea as a faint rising row of bars (a visual hint, not data)
  for (let i = 0; i < 20; i++) {
    const h = 0.35 + i * 0.05;
    s.addShape(pres.shapes.RECTANGLE, { x: 0.5 + i * 0.45, y: 5.35 - h, w: 0.36, h, fill: { color: C.accent1, transparency: 35 }, line: { color: C.accent1, transparency: 35 }, objectName: `Motif bar ${i + 1}` });
  }
  s.addText("A DATA STORY · MACHINE LEARNING ON COLORADO FOREST DATA", { x: 0.5, y: 0.55, w: 9, h: 0.3, fontSize: 11, bold: true, color: C.accent4, charSpacing: 1, margin: 0, isTextBox: true });
  s.addText("Can AI build better AI?", { x: 0.5, y: 0.95, w: 9, h: 1.0, fontFace: THEME.headFontFace, fontSize: 44, bold: true, color: C.background1, margin: 0, isTextBox: true });
  s.addText("A program that builds, tests and improves its own models, how far it gets, and where the idea breaks.", { x: 0.5, y: 2.0, w: 7.2, h: 0.8, fontSize: 16, color: C.background2, margin: 0, isTextBox: true });
  s.addText("Scott Schirkofsky · Part 1 of 4: the data and the baseline · schirko.com/scott/model-loop-lab", { x: 0.5, y: 2.95, w: 9, h: 0.35, fontSize: 12, color: C.accent4, margin: 0, isTextBox: true });
  s.addNotes("You've probably heard that AI is now helping to build the next generation of AI. I wanted to see what that actually looks like, so I built a small version of it myself, on real data: forest plots in Colorado. This version of the talk covers part 1 of 4: the data, a fair way to test models, and the number every later model has to beat. The rest of the story is added as each notebook is finished.");
}

// ---------- 2. The hook ----------
{
  const s = content("Opening", "THE QUESTION", "New AI is increasingly built with help from older AI. Does that make it better, or worse?");
  const loops = [
    { x: 0.5, color: C.accent1, head: "Loop 1: improve", sub: "Checked against real data every round", steps: ["Build models", "Test on real plots", "Keep the best", "Repeat"] },
    { x: 5.1, color: C.accent2, head: "Loop 2: copy a copy", sub: "Never looks at real data again", steps: ["Learn the data", "Make up new data", "Learn from that", "Repeat"] },
  ];
  loops.forEach((L, k) => {
    s.addShape(pres.shapes.ROUNDED_RECTANGLE, { x: L.x, y: 1.65, w: 4.4, h: 3.25, rectRadius: 0.1, fill: { color: C.background2 }, line: { color: C.background2 }, objectName: `Loop ${k + 1} card` });
    s.addText(L.head, { x: L.x + 0.25, y: 1.8, w: 3.9, h: 0.4, fontFace: THEME.headFontFace, fontSize: 18, bold: true, color: L.color, margin: 0, isTextBox: true });
    s.addText(L.sub, { x: L.x + 0.25, y: 2.2, w: 3.9, h: 0.3, fontSize: 12, color: C.accent5, margin: 0, isTextBox: true });
    L.steps.forEach((t, i) => {
      const yy = 2.65 + i * 0.52;
      s.addShape(pres.shapes.OVAL, { x: L.x + 0.25, y: yy, w: 0.36, h: 0.36, fill: { color: L.color }, line: { color: L.color }, objectName: `Loop ${k + 1} step ${i + 1} badge` });
      s.addText(String(i + 1), { x: L.x + 0.25, y: yy, w: 0.36, h: 0.36, fontSize: 12, bold: true, color: C.background1, align: "center", valign: "middle", margin: 0, isTextBox: true });
      s.addText(t, { x: L.x + 0.75, y: yy, w: 3.3, h: 0.36, fontSize: 14, color: C.text1, valign: "middle", margin: 0, isTextBox: true });
    });
  });
  s.addNotes("There are two very different loops hiding in that idea. In the first, a program keeps trying new models and keeps whichever scores best on real data. In the second, a model learns from data that an earlier model made up. The first should improve things. The second sounds harmless, but it isn't. This project builds both and measures them.");
}

// ---------- 3. Words ----------
{
  const s = content("Opening", "WORDS USED", "Nine words you'll hear, in plain English");
  const rows = [
    ["Model", "Rules learned from data that turn a plot's map measurements into a guess of which trees grow there"],
    ["Decision tree", "A model that asks a chain of yes/no questions until it reaches an answer"],
    ["Accuracy", "The share of plots the model labels correctly"],
    ["Held-out plots", "5,000 plots never shown to a model while it learns; every score comes from these"],
    ["Baseline", "The score of a plain model with no tuning: the number to beat"],
    ["Overfitting", "Memorizing the training plots instead of learning patterns that carry over"],
    ["Generation", "One round of the loop: build several models, score them, keep the best"],
    ["Synthetic data", "Made-up data produced by a model, meant to look like the real thing"],
    ["Model collapse", "Models trained only on earlier models' made-up data losing touch with reality"],
  ];
  const t = rows.map(([a, b], i) => [
    { text: a, options: { bold: true, color: HEX.spruce, fill: { color: i % 2 ? "FFFFFF" : "EEF3EF" } } },
    { text: b, options: { fill: { color: i % 2 ? "FFFFFF" : "EEF3EF" } } },
  ]);
  s.addTable(t, { x: 0.5, y: 1.5, w: 9.0, colW: [1.9, 7.1], fontSize: 12, color: "18201B", rowH: 0.36, margin: [2, 6, 2, 6], border: { type: "none" }, objectName: "Word list" });
  s.addNotes("I'll use these nine words throughout. If you remember only two, make them held-out plots and overfitting. Every honest score in this talk comes from plots the model never saw, and overfitting is the problem the loop ends up attacking.");
}

// ---------- 4. The plan ----------
{
  const s = content("Opening", "HOW THE PROJECT IS ORGANIZED", "Four notebooks, each answering one question");
  const nbs = [
    ["01", "Data and baseline", "What does the data look like, and how good is a plain model?", "Finished", true],
    ["02", "The evolution loop", "Can a program find better models on its own?", "In progress", false],
    ["03", "The search race", "Is the loop better than standard tools, or than guessing?", "Planned", false],
    ["04", "Model collapse", "What happens when models learn only from other models?", "Planned", false],
  ];
  nbs.forEach(([num, name, q, status, done], i) => {
    const x = 0.5 + i * 2.3;
    s.addShape(pres.shapes.ROUNDED_RECTANGLE, { x, y: 1.6, w: 2.1, h: 3.3, rectRadius: 0.1, fill: { color: done ? C.accent1 : C.background2 }, line: { color: done ? C.accent1 : C.background2 }, objectName: `Notebook ${num} card` });
    s.addText(num, { x: x + 0.2, y: 1.75, w: 1.7, h: 0.6, fontFace: THEME.headFontFace, fontSize: 30, bold: true, color: done ? C.background1 : C.accent1, margin: 0, isTextBox: true });
    s.addText(name, { x: x + 0.2, y: 2.4, w: 1.7, h: 0.6, fontSize: 15, bold: true, color: done ? C.background1 : C.text1, valign: "top", margin: 0, isTextBox: true });
    s.addText(q, { x: x + 0.2, y: 3.05, w: 1.7, h: 1.2, fontSize: 12, color: done ? C.background2 : C.accent5, valign: "top", margin: 0, isTextBox: true });
    s.addText(status, { x: x + 0.2, y: 4.4, w: 1.7, h: 0.3, fontSize: 11, bold: true, color: done ? C.accent4 : C.accent3, margin: 0, isTextBox: true });
  });
  s.addNotes("Everything I'll show comes from four Jupyter notebooks, and every step in them shows the code, its result and a plain-language reading. Notebook 01 is finished, and it's what this version of the talk covers. The label at the top of each slide tells you which notebook and which step we're on.");
}

// ---------- 5. Notebook 01 opener ----------
pres.addSection({ title: "Notebook 01: Data and baseline" });
{
  const s = pres.addSlide({ masterName: "DARK", sectionTitle: "Notebook 01: Data and baseline" }); n += 1;
  ["01", "02", "03", "04"].forEach((num, i) => {
    const on = i === 0;
    s.addShape(pres.shapes.ROUNDED_RECTANGLE, { x: 0.5 + i * 0.75, y: 0.5, w: 0.65, h: 0.32, rectRadius: 0.05, fill: { color: on ? C.accent1 : C.text2 }, line: { color: on ? C.accent4 : C.accent3 }, objectName: `Progress ${num}` });
    s.addText(num, { x: 0.5 + i * 0.75, y: 0.5, w: 0.65, h: 0.32, fontSize: 11, bold: true, color: on ? C.background1 : C.accent3, align: "center", valign: "middle", margin: 0, isTextBox: true });
  });
  s.addText("NOTEBOOK 01 OF 4", { x: 0.5, y: 1.05, w: 4.3, h: 0.3, fontSize: 11, bold: true, color: C.accent4, charSpacing: 1, margin: 0, isTextBox: true });
  s.addText("What does the data look like, and how good is a plain model?", { x: 0.5, y: 1.4, w: 4.2, h: 2.0, fontFace: THEME.headFontFace, fontSize: 28, bold: true, color: C.background1, valign: "top", margin: 0, isTextBox: true });
  const steps = ["Setup", "Load the full dataset", "Take a 20,000-plot sample", "Split into training and held-out plots", "Score guessing and a plain tree",
    "Check that scoring is repeatable", "Record the baseline", "Results by cover type", "What gets confused with what", "Save the baseline for the website"];
  s.addText(steps.map((t, i) => ({ text: `Step ${i + 1}   ${t}`, options: { breakLine: i < steps.length - 1 } })),
    { x: 5.2, y: 1.05, w: 4.3, h: 3.9, fontSize: 14, color: C.background2, paraSpaceAfter: 6, valign: "top", margin: 0, isTextBox: true, objectName: "Notebook 01 steps" });
  s.addNotes("Notebook 01 sets up everything the later notebooks depend on: the data, a fair way to test, and the number every later model has to beat. It has ten steps, and the next seven slides walk through them.");
}

// ---------- 6. The data (Steps 1-2) ----------
{
  const s = content("Notebook 01: Data and baseline", "NOTEBOOK 01 · STEPS 1–2", "581,012 plots of Colorado forest, described by map measurements alone");
  const labels = ["Cottonwood/willow", "Aspen", "Douglas-fir", "Krummholz", "Ponderosa pine", "Spruce/fir", "Lodgepole pine"];
  const vals = [0.47, 1.63, 2.99, 3.53, 6.15, 36.46, 48.76];
  s.addChart(pres.charts.BAR, [{ name: "Share of plots", labels, values: vals }], {
    x: 0.4, y: 1.5, w: 5.9, h: 3.6, barDir: "bar", chartColors: [HEX.spruce], showValue: true, dataLabelPosition: "outEnd", dataLabelFormatCode: '0.0"%"',
    valAxisHidden: true, valGridLine: { style: "none" }, catGridLine: { style: "none" }, showLegend: false, barGapWidthPct: 45,
    showTitle: true, title: "Share of all plots, by cover type", titleFontSize: 12, titleColor: HEX.ink2, ...chartText, objectName: "Cover type shares chart",
  });
  callouts(s, [
    ["581,012", "30 × 30 m plots in the Roosevelt National Forest"],
    ["54", "map features per plot: elevation, slope, distance to water and roads, soil type and more"],
    ["85%", "of plots are just two cover types: Lodgepole pine and Spruce/fir"],
  ]);
  source(s, "Forest Covertype data, U.S. Forest Service and Colorado State University, via UCI; notebook 01, Step 2.");
  s.addNotes("The data is a classic. Every plot is a square of forest about the size of a few tennis courts, described only by what you'd find on a map: no photos, no field visits. The job is to say which of seven tree covers grows there. Notice how lopsided it is. Two cover types make up 85% of the forest, and Cottonwood/willow is under half a percent. That will matter.");
}

// ---------- 7. A fair test (Steps 3-4) ----------
{
  const s = content("Notebook 01: Data and baseline", "NOTEBOOK 01 · STEPS 3–4", "Every model is scored on the same 5,000 plots it never saw while learning");
  // 20,000-plot bar split 75 / 25
  s.addText("20,000 plots, drawn so every cover type keeps its exact share", { x: 0.5, y: 1.6, w: 5.8, h: 0.35, fontSize: 13, bold: true, color: C.text1, margin: 0, isTextBox: true });
  s.addShape(pres.shapes.RECTANGLE, { x: 0.5, y: 2.05, w: 4.35, h: 1.1, fill: { color: C.accent6 }, line: { color: C.accent6 }, objectName: "Training block" });
  s.addShape(pres.shapes.RECTANGLE, { x: 4.9, y: 2.05, w: 1.4, h: 1.1, fill: { color: C.accent1 }, line: { color: C.accent1 }, objectName: "Held-out block" });
  s.addText([{ text: "15,000", options: { fontSize: 22, bold: true, breakLine: true } }, { text: "training plots", options: { fontSize: 12 } }], { x: 0.5, y: 2.05, w: 4.35, h: 1.1, color: C.text1, align: "center", valign: "middle", margin: 0, isTextBox: true });
  s.addText([{ text: "5,000", options: { fontSize: 22, bold: true, breakLine: true } }, { text: "held out", options: { fontSize: 12 } }], { x: 4.9, y: 2.05, w: 1.4, h: 1.1, color: C.background1, align: "center", valign: "middle", margin: 0, isTextBox: true });
  s.addText("Models learn only from the gray plots. Every score in this project comes from the green ones, the same 5,000 for every model, so a better score means a better model, not a luckier split.",
    { x: 0.5, y: 3.35, w: 5.8, h: 1.2, fontSize: 13, color: C.accent5, valign: "top", margin: 0, isTextBox: true });
  callouts(s, [
    ["20,000", "plots sampled so each model trains in seconds"],
    ["0.47%", "Cottonwood/willow's share in the forest and in the sample: the rare types are kept"],
    ["0", "plots in both the training and held-out sets"],
  ]);
  source(s, "Notebook 01, Steps 3–4; src/evaluate.py.");
  s.addNotes("To run a loop that trains hundreds of models, I needed a smaller sample. I took 20,000 plots, drawn so every cover type keeps its exact share, rare ones included. Then I held back 5,000 that no model ever learns from. Every score in this talk comes from those same 5,000 plots, so the comparisons are fair.");
}

// ---------- 8. Guessing vs a plain tree (Steps 5-6) ----------
{
  const s = content("Notebook 01: Data and baseline", "NOTEBOOK 01 · STEPS 5–6", "Map measurements alone get a plain tree to 77%. Guessing gets 49%");
  s.addChart(pres.charts.BAR, [{ name: "Accuracy on held-out plots", labels: ["Always guess Lodgepole pine", "Plain decision tree"], values: [48.8, 77.2] }], {
    x: 0.4, y: 1.5, w: 5.9, h: 3.6, barDir: "col", chartColors: [HEX.gray, HEX.spruce], invertedColors: [HEX.gray, HEX.spruce], showValue: true, dataLabelPosition: "outEnd", dataLabelFormatCode: '0.0"%"',
    valAxisMinVal: 0, valAxisMaxVal: 100, valAxisLabelFormatCode: '0"%"', valGridLine: { color: HEX.rule, size: 0.5 }, catGridLine: { style: "none" }, showLegend: false, barGapWidthPct: 70,
    showTitle: true, title: "Accuracy on the 5,000 held-out plots", titleFontSize: 12, titleColor: HEX.ink2, ...chartText, objectName: "Guess versus tree chart",
  });
  callouts(s, [
    ["48.8%", "always guessing the most common type, Lodgepole pine"],
    ["77.2%", "a decision tree with every setting left at its default"],
    ["28 points", "how much the map features tell us about which trees grow where"],
  ]);
  source(s, "Notebook 01, Step 5. Step 6 confirms the same model scores identically every time.");
  s.addNotes("Here's the floor. If you always guess the most common tree, you're right about half the time. A plain decision tree, which actually reads elevation, soil and so on, gets 77%. So the data really does carry information. I also checked that scoring the same model twice gives exactly the same number, because the loop will depend on that.");
}

// ---------- 9. The baseline (Step 7) ----------
{
  const s = content("Notebook 01: Data and baseline", "NOTEBOOK 01 · STEP 7", "The plain tree scores 77.2% on new plots, but 100% on the plots it learned from");
  s.addChart(pres.charts.BAR, [{ name: "Accuracy", labels: ["Its own training plots", "Held-out plots (the baseline)"], values: [100, 77.2] }], {
    x: 0.4, y: 1.5, w: 5.9, h: 3.6, barDir: "col", chartColors: [HEX.amber, HEX.spruce], invertedColors: [HEX.amber, HEX.spruce], showValue: true, dataLabelPosition: "outEnd", dataLabelFormatCode: '0.0"%"',
    valAxisMinVal: 0, valAxisMaxVal: 110, valAxisMajorUnit: 20, valAxisLabelFormatCode: '0"%"', valGridLine: { color: HEX.rule, size: 0.5 }, catGridLine: { style: "none" }, showLegend: false, barGapWidthPct: 70,
    showTitle: true, title: "The same tree, scored two ways", titleFontSize: 12, titleColor: HEX.ink2, ...chartText, objectName: "Overfitting chart",
  });
  callouts(s, [
    ["77.2%", "the baseline: right on 3,859 of 5,000 plots it never saw"],
    ["23 points", "the gap between training and new plots: overfitting"],
    ["2,341", "final answers in a tree 33 questions deep, about one for every six training plots"],
  ]);
  source(s, "Notebook 01, Step 7.");
  s.addNotes("This is the number every later model has to beat: 77.2%. But look at the other bar. On the plots it learned from, the tree is perfect. It kept asking questions until every training plot was sorted, which took 33 levels and over two thousand final answers, many of them for a single unusual plot. That's overfitting: it memorized instead of learning. The gap between these two bars is exactly what the loop in notebook 02 can work on.");
}

// ---------- 10. Results by cover type (Step 8) ----------
{
  const s = content("Notebook 01: Data and baseline", "NOTEBOOK 01 · STEP 8", "The tree handles the common trees well and struggles with Aspen and Douglas-fir");
  const labels = ["Aspen", "Douglas-fir", "Cottonwood/willow", "Spruce/fir", "Krummholz", "Ponderosa pine", "Lodgepole pine"];
  const vals = [43.9, 52.3, 65.2, 76.6, 76.8, 77.6, 80.3];
  s.addChart(pres.charts.BAR, [{ name: "Recall", labels, values: vals }], {
    x: 0.4, y: 1.5, w: 5.9, h: 3.6, barDir: "bar", chartColors: [HEX.amber, HEX.amber, HEX.amber, HEX.spruce, HEX.spruce, HEX.spruce, HEX.spruce],
    invertedColors: [HEX.amber, HEX.amber, HEX.amber, HEX.spruce, HEX.spruce, HEX.spruce, HEX.spruce],
    showValue: true, dataLabelPosition: "outEnd", dataLabelFormatCode: '0"%"', valAxisMinVal: 0, valAxisMaxVal: 100, valAxisHidden: true,
    valGridLine: { style: "none" }, catGridLine: { style: "none" }, showLegend: false, barGapWidthPct: 45,
    showTitle: true, title: "Share of each cover type's plots the tree found (recall)", titleFontSize: 12, titleColor: HEX.ink2, ...chartText, objectName: "Recall by cover type chart",
  });
  callouts(s, [
    ["80%", "of Lodgepole pine found, the most common tree"],
    ["44%", "of Aspen found: fewer than half"],
    ["77%", "of Krummholz found, though it's rare: rarity alone isn't the problem"],
  ]);
  source(s, "Notebook 01, Step 8. Amber: more than 5 points below the overall 77.2%. Cottonwood/willow has only 23 held-out plots, so its rate is rough.");
  s.addNotes("Breaking the score down by tree type, the common ones sit near 80%. Aspen is the weak spot: the tree finds fewer than half of the real Aspen plots. But rarity isn't the whole story. Krummholz is rare too, and the tree finds it just fine. The next slide shows why.");
}

// ---------- 11. Confusion (Step 9) ----------
{
  const s = content("Notebook 01: Data and baseline", "NOTEBOOK 01 · STEP 9", "The mistakes are between neighbors: trees that grow at the same elevations");
  s.addImage({ path: path.join(ASSETS, "confusion.png"), x: 0.6, y: 1.5, w: 3.62, h: 3.5, altText: "Seven by seven grid of the share of each real cover type given each answer. The darkest squares off the diagonal are Spruce/fir and Lodgepole pine confused with each other, and Aspen called Lodgepole pine.", objectName: "Confusion chart" });
  callouts(s, [
    ["21% / 16%", "Spruce/fir called Lodgepole pine, and the reverse: the two biggest types swap places"],
    ["44%", "of Aspen called Lodgepole pine; Aspen grows mixed into lodgepole stands"],
    ["1", "look-alike for Krummholz (Spruce/fir, just below it on the mountain), so it does well"],
  ], 4.65, 1.6, 4.85);
  source(s, "Notebook 01, Step 9. Read across a row: for the plots that really are that type, the share given each answer.");
  s.addNotes("Read each row as the real tree and each column as the model's answer. The dark diagonal is right answers. The mistakes cluster in neighbor pairs. Spruce/fir and Lodgepole pine swap with each other, and because those two are 85% of the forest, that pair causes most of the errors. Aspen gets called Lodgepole pine as often as it gets called Aspen. Krummholz, the stunted trees at treeline, has only one neighbor to be confused with, so it does well. If a better model can separate Spruce/fir from Lodgepole pine even a little, the overall score jumps.");
}

// ---------- 12. What notebook 01 sets up (Step 10) ----------
{
  const s = content("Notebook 01: Data and baseline", "NOTEBOOK 01 · STEP 10", "The target for the loop: beat 77.2% by ending the memorizing and telling neighbors apart");
  const rows = [
    ["77.2%", "Number to beat", "The plain tree's accuracy on the 5,000 held-out plots."],
    ["100% vs 77.2%", "Weakness 1: it memorizes", "Settings that limit how deep a tree grows, or models that average many trees, can fix this."],
    ["21% / 44%", "Weakness 2: it confuses neighbors", "Spruce/fir with Lodgepole pine, and Aspen with Lodgepole pine."],
  ];
  rows.forEach(([big, head, text], i) => {
    const y = 1.6 + i * 1.12;
    s.addShape(pres.shapes.ROUNDED_RECTANGLE, { x: 0.5, y, w: 9.0, h: 0.98, rectRadius: 0.08, fill: { color: C.background2 }, line: { color: C.background2 }, objectName: `Brief row ${i + 1}` });
    s.addText(big, { x: 0.7, y, w: 2.6, h: 0.98, fontFace: THEME.headFontFace, fontSize: 22, bold: true, color: C.accent1, valign: "middle", margin: 0, isTextBox: true });
    s.addText([{ text: head, options: { bold: true, fontSize: 15, breakLine: true } }, { text, options: { fontSize: 12, color: HEX.ink2 } }], { x: 3.4, y, w: 5.9, h: 0.98, color: C.text1, valign: "middle", margin: 0, isTextBox: true });
  });
  source(s, "Notebook 01, Step 10 saves the baseline to results/web/baseline.json, which the website reads.");
  s.addNotes("Notebook 01 ends by saving the baseline where the website can read it, so the site and the notebook can never disagree. And it hands notebook 02 a clear brief: beat 77.2%, and the two ways to do it are to stop memorizing and to tell the neighbors apart.");
}

// ---------- 13. Still to come ----------
pres.addSection({ title: "Still to come" });
{
  const s = pres.addSlide({ masterName: "DARK", sectionTitle: "Still to come" }); n += 1;
  s.addText("WHAT'S NEXT", { x: 0.5, y: 0.55, w: 9, h: 0.3, fontSize: 11, bold: true, color: C.accent4, charSpacing: 1, margin: 0, isTextBox: true });
  s.addText("The rest of the story is added as each notebook is finished", { x: 0.5, y: 0.9, w: 9, h: 0.9, fontFace: THEME.headFontFace, fontSize: 26, bold: true, color: C.background1, valign: "top", margin: 0, isTextBox: true });
  const next = [
    ["02", "The evolution loop", "Ten models a round, keep the best three, 20 rounds. How far above 77.2% does it climb?", "In progress"],
    ["03", "The search race", "The loop against Optuna and random guessing, 200 tries each.", "Planned"],
    ["04", "Model collapse", "Each generation learns only from made-up data. What is lost?", "Planned"],
  ];
  next.forEach(([num, name, text, status], i) => {
    const x = 0.5 + i * 3.05;
    s.addShape(pres.shapes.ROUNDED_RECTANGLE, { x, y: 2.05, w: 2.85, h: 2.75, rectRadius: 0.1, fill: { color: C.text2 }, line: { color: C.accent1, width: 1.5 }, objectName: `Next notebook ${num}` });
    s.addText(num, { x: x + 0.22, y: 2.2, w: 2.4, h: 0.55, fontFace: THEME.headFontFace, fontSize: 26, bold: true, color: C.accent4, margin: 0, isTextBox: true });
    s.addText(name, { x: x + 0.22, y: 2.8, w: 2.4, h: 0.4, fontSize: 15, bold: true, color: C.background1, margin: 0, isTextBox: true });
    s.addText(text, { x: x + 0.22, y: 3.25, w: 2.4, h: 1.1, fontSize: 12, color: C.background2, valign: "top", margin: 0, isTextBox: true });
    s.addText(status, { x: x + 0.22, y: 4.4, w: 2.4, h: 0.3, fontSize: 11, bold: true, color: C.accent4, margin: 0, isTextBox: true });
  });
  s.addText("Notebooks, findings and code: schirko.com/scott/model-loop-lab", { x: 0.5, y: 5.05, w: 8, h: 0.3, fontSize: 11, color: C.accent3, margin: 0, isTextBox: true });
  s.addNotes("That's part 1: the data, a fair test, and a baseline of 77.2% with two clear weaknesses. Next, notebook 02 runs the improvement loop to see how far it can climb, notebook 03 races it against a professional tuning tool and random guessing, and notebook 04 runs the copy-of-a-copy loop to see what gets lost. Each one adds its slides to this deck when it's finished.");
}

// ---------- Write ----------
(async () => {
  const { applyTheme } = require(process.env.PPTX_SKILL + "/scripts/apply_theme.js");
  require("fs").mkdirSync(path.dirname(OUT), { recursive: true });
  await pres.writeFile({ fileName: OUT });
  await applyTheme(OUT, THEME);
  console.log(`Wrote ${OUT} (${n} slides)`);
})();
