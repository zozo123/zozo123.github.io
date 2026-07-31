/* ============ data: every live page, same content as the GitHub profile ============ */
const FIGSETS = {
  1: [ // §01 AI Agents & Sandboxes
    { slug: "wasted-cycles", url: "https://zozo123.github.io/wasted-cycles/",
      image: "https://zozo123.github.io/wasted-cycles/og.png",
      title: "Wasted Cycles", tldr: "Find the machine time blocking agent work — local traces and GitHub Actions latency." },
    { slug: "t2t-vs-grch38", url: "https://zozo123.github.io/t2t-vs-grch38/",
      image: "https://zozo123.github.io/t2t-vs-grch38/og.png",
      title: "What T2T Changed", tldr: "GRCh38 → T2T-CHM13 delta, computed genome-wide by a Claude Code sandbox harness." },
    { slug: "sandboxes-why-how-when", url: "https://zozo123.github.io/sandboxes-why-how-when/",
      title: "The Sandbox Shift", tldr: "Why, when & how to sandbox AI-written code — with an interactive decider." },
    { slug: "sandbox-landscape", url: "https://zozo123.github.io/sandbox-landscape/",
      title: "AI Sandbox Landscape", tldr: "A map of the execution-sandbox ecosystem." },
    { slug: "inferoa-demo", url: "https://zozo123.github.io/inferoa-demo/",
      title: "Inferoa", tldr: "Inference-native agent mechanics: prefix caching, context compression, routing." },
    { slug: "agentic-airbyte", url: "https://zozo123.github.io/agentic-airbyte/",
      title: "Agentic Airbyte", tldr: "Agent plans, crabbox runs, Airbyte moves — agentic data movement." },
    { slug: "demo-evals-pydantic-islo-crabbox", url: "https://zozo123.github.io/demo-evals-pydantic-islo-crabbox/",
      title: "Evals or You're Blind", tldr: "Pydantic AI × Pydantic Evals on disposable boxes." },
    { slug: "repo2rlenv-crabbox-demo", url: "https://zozo123.github.io/repo2rlenv-crabbox-demo/",
      title: "Repo2RLEnv × crabbox", tldr: "Score Harbor pr_diff tasks on a remote sandbox in ~50s." },
    { slug: "odysseus-crabbox-demo", url: "https://zozo123.github.io/odysseus-crabbox-demo/",
      title: "Odysseus × crabbox", tldr: "A self-hosted AI workspace on a throwaway microVM, one command." },
    { slug: "longmem-mini-on-islo", url: "https://zozo123.github.io/longmem-mini-on-islo/",
      title: "Tiny Long-Memory Benchmark", tldr: "LongMemEval-style memory benchmark fanned across sandboxes." },
    { slug: "meta-harness-on-islo-page", url: "https://zozo123.github.io/meta-harness-on-islo-page/",
      title: "Meta-harness on Islo", tldr: "A harness that builds harnesses (POC) — 0/5→5/5 in four proposer steps." },
    { slug: "env-rosetta-page", url: "https://zozo123.github.io/env-rosetta-page/",
      title: "env-rosetta", tldr: "Same Wordle env, 4 RL frameworks, 4 sandboxes." },
    { slug: "pokeloop", url: "https://zozo123.github.io/pokeloop/",
      title: "Pokeloop", tldr: "GA over LLM policies learning Pokémon GO." },
    { slug: "unity-loop-page", url: "https://zozo123.github.io/unity-loop-page/",
      title: "unity-loop", tldr: "Vibe-coded Unity on remote sandboxes — a Claude-vision tournament." },
    { slug: "wolfram-fb0", url: "https://zozo123.github.io/wolfram-fb0/",
      title: "wolfram-fb0", tldr: "AI-written x86_64 asm + eBPF fractals straight to /dev/fb0." },
    { slug: "gha-cache-field-guide", url: "https://zozo123.github.io/gha-cache-field-guide/",
      title: "CI Caching Is Not One Cache", tldr: "A field guide to GitHub Actions cache strategy." },
  ],
  2: [ // §02 Deep Dives & Essays
    { slug: "how-stackoverflow-taught-ai", url: "https://zozo123.github.io/how-stackoverflow-taught-ai/",
      title: "The Data That Taught the Machines", tldr: "How Stack Overflow trained its own replacement." },
    { slug: "loop-coming-apart", url: "https://zozo123.github.io/loop-coming-apart/",
      title: "The Loop Is Coming Apart", tldr: "jj, crabbox & the unbundled dev cycle — the diff is the unit of work." },
    { slug: "intel-story", url: "https://zozo123.github.io/intel-story/",
      title: "Intel: Vision Without Execution", tldr: "A comic-style dive into Intel's 2000–2026 journey." },
    { slug: "has-steipete-hit-1m-github-ytd", url: "https://zozo123.github.io/has-steipete-hit-1m-github-ytd/",
      title: "Has steipete hit 1M GitHub YTD?", tldr: "A live contribution tracker." },
  ],
  3: [ // §03 Quant Finance
    { slug: "market-making-sandbox", url: "https://zozo123.github.io/market-making-sandbox/",
      title: "How Market Makers Print Money", tldr: "Order books → Avellaneda–Stoikov, Glosten–Milgrom, Kyle's λ — interactive." },
    { slug: "microprice-sandbox", url: "https://zozo123.github.io/microprice-sandbox/",
      title: "Avellaneda–Stoikov, in a Sandbox", tldr: "Reproducing the HFT paper in ~90s, no local Python." },
  ],
};

/* ============ render figure cards ============ */
let figNo = 0;

function thumbHTML(p) {
  const src = p.image || `assets/thumbs/${p.slug}.jpg`;
  return `
    <span class="figure-thumb">
      <img src="${src}" alt="${p.title} — live page screenshot" width="760" height="475" loading="lazy">
    </span>`;
}
function captionHTML(n) {
  return `
    <span class="fig-caption">
      <span class="fc-no">Fig. ${n}</span>
      <span class="fc-live">● live page</span>
    </span>`;
}
function bodyHTML(p) {
  return `
    <span class="figure-body">
      <span class="figure-title">${p.title}</span>
      <span class="figure-tldr">${p.tldr}</span>
      <span class="mono figure-link">View live →</span>
    </span>`;
}

document.querySelectorAll(".figure-grid").forEach((grid) => {
  const set = FIGSETS[grid.dataset.figset] || [];
  const usePlate = grid.dataset.plate === "1";
  grid.innerHTML = set.map((p, i) => {
    figNo += 1;
    const n = String(figNo).padStart(2, "0");
    const closingPlate = i === set.length - 1 && (set.length - 2) % 3 === 0;
    if (usePlate && (i === 0 || closingPlate)) {
      return `
        <a class="figure-card plate${closingPlate ? " plate-flip" : ""} reveal" href="${p.url}" target="_blank" rel="noopener">
          ${thumbHTML(p)}
          <span class="fig-side">${captionHTML(n)}${bodyHTML(p)}</span>
        </a>`;
    }
    return `
      <a class="figure-card reveal" href="${p.url}" target="_blank" rel="noopener">
        ${thumbHTML(p)}${captionHTML(n)}${bodyHTML(p)}
      </a>`;
  }).join("");
  grid.querySelectorAll(".figure-thumb img").forEach((image) => {
    image.addEventListener("error", () => image.parentNode.classList.add("thumb-missing"));
  });
});

/* ============ masthead date ============ */
const d = new Date();
document.getElementById("today-date").textContent =
  d.toLocaleDateString("en-US", { year: "numeric", month: "short", day: "numeric" }).toUpperCase();

const reduceMotion = window.matchMedia("(prefers-reduced-motion: reduce)").matches;

/* ============ hero load-in ============ */
if (reduceMotion) {
  document.querySelectorAll(".reveal").forEach((el) => el.classList.add("in"));
} else {
  requestAnimationFrame(() => {
    document.querySelectorAll(".in-load").forEach((el) => el.classList.add("in"));
  });
}

/* ============ scroll reveal ============ */
const io = new IntersectionObserver((entries) => {
  entries.forEach((e) => {
    if (e.isIntersecting) { e.target.classList.add("in"); io.unobserve(e.target); }
  });
}, { threshold: 0.08, rootMargin: "0px 0px -4% 0px" });
if (!reduceMotion) {
  document.querySelectorAll(".reveal:not(.in-load)").forEach((el) => io.observe(el));
}

/* ============ hero counters ============ */
const counterIO = new IntersectionObserver((entries) => {
  entries.forEach((e) => {
    if (!e.isIntersecting) return;
    counterIO.unobserve(e.target);
    const target = +e.target.dataset.count;
    const t0 = performance.now(), dur = 1100;
    const tick = (t) => {
      const k = Math.min((t - t0) / dur, 1);
      e.target.textContent = Math.round(target * (1 - Math.pow(1 - k, 3)));
      if (k < 1) requestAnimationFrame(tick);
    };
    requestAnimationFrame(tick);
  });
}, { threshold: 0.5 });
document.querySelectorAll(".stat-n").forEach((el) => {
  if (reduceMotion) {
    el.textContent = el.dataset.count;
  } else {
    counterIO.observe(el);
  }
});
