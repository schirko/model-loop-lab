/* Model Loop Lab: shared chart helpers.
   Charts read JSON from /scott/model-loop-lab/data/. Each file carries
   "sample": true until the notebooks write real results, and every chart
   that draws from a sample file shows the "Sample data" notice. */

(function () {
  const DATA = "/scott/model-loop-lab/data/";

  function css(name) {
    return getComputedStyle(document.documentElement).getPropertyValue(name).trim();
  }

  async function load(name) {
    const res = await fetch(DATA + name + ".json", { cache: "no-cache" });
    if (!res.ok) throw new Error("Could not load " + name + ".json (" + res.status + ")");
    return res.json();
  }

  // Show or hide every sample notice tied to a data file.
  function markSample(name, isSample) {
    document.querySelectorAll('[data-sample-for="' + name + '"]').forEach((el) => {
      el.hidden = !isSample;
    });
  }

  function showError(el, err) {
    el.innerHTML = '<p class="mll-small" style="padding:24px">This chart could not load its data. ' +
      String(err.message || err) + "</p>";
  }

  // Plotly layout that follows the page's light or dark tokens.
  function layout(extra) {
    const ink2 = css("--ink-2"), ink3 = css("--ink-3"), rule = css("--rule");
    const base = {
      paper_bgcolor: "rgba(0,0,0,0)",
      plot_bgcolor: "rgba(0,0,0,0)",
      font: { family: css("--sans") || "system-ui", size: 13, color: ink2 },
      margin: { l: 64, r: 20, t: 16, b: 60 },
      hovermode: "x unified",
      hoverlabel: { bgcolor: css("--surface-raised"), bordercolor: rule, font: { color: css("--ink") } },
      legend: { orientation: "h", x: 0, y: 1.12, font: { color: ink2 } },
      xaxis: { gridcolor: "rgba(0,0,0,0)", linecolor: rule, tickcolor: rule, zeroline: false, title: { font: { color: ink3 } } },
      yaxis: { gridcolor: rule, gridwidth: 1, linecolor: "rgba(0,0,0,0)", zeroline: false, title: { font: { color: ink3 } } },
    };
    return deepMerge(base, extra || {});
  }

  function deepMerge(a, b) {
    const out = Array.isArray(a) ? a.slice() : Object.assign({}, a);
    Object.keys(b).forEach((k) => {
      const bv = b[k];
      out[k] = bv && typeof bv === "object" && !Array.isArray(bv) && a[k] && typeof a[k] === "object"
        ? deepMerge(a[k], bv) : bv;
    });
    return out;
  }

  const config = { displayModeBar: false, responsive: true };

  // Redraw every chart when the color scheme flips so axes stay legible.
  const redraws = [];
  function onTheme(fn) { redraws.push(fn); }
  if (window.matchMedia) {
    window.matchMedia("(prefers-color-scheme: dark)").addEventListener("change", () => redraws.forEach((f) => f()));
  }

  // Draw a chart sized to its box. Passing the width explicitly avoids
  // Plotly guessing too wide on narrow phone screens.
  function draw(id, traces, lay) {
    const el = document.getElementById(id);
    lay.width = el.clientWidth;
    // End-of-line labels need room; on phones the legend carries the names.
    if (lay.width < 520 && lay.annotations) lay.annotations = [];
    lay.height = el.clientHeight;
    return Plotly.react(el, traces, lay, config);
  }
  window.addEventListener("resize", () => redraws.forEach((f) => f()));

  // The baseline lives in its own file (written by notebook 01). Pages that
  // also draw the evolution chart use it in place of evolution.json's copy.
  async function baseline(evo) {
    try {
      const b = await load("baseline");
      markSample("baseline", b.sample);
      if (evo && !b.sample) evo.baseline = { label: b.label, score: b.score };
      return b;
    } catch (e) {
      console.error(e);
      return evo ? Object.assign({ sample: true }, evo.baseline) : null;
    }
  }

  function pct(v, digits) { return (v * 100).toFixed(digits == null ? 1 : digits) + "%"; }

  window.MLL = { css, load, markSample, showError, layout, config, onTheme, draw, baseline, pct };
})();
