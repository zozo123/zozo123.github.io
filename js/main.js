/* Writing archive. Selected work and reading remain available without JavaScript. */
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
      title: "Meta-harness on Islo", tldr: "A deterministic simulation of harness optimization: scripted agent, pattern-matching proposer, five toy tasks." },
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
  2: [ // Essays and architecture ideas
    { slug: "databases-in-the-ai-era", url: "https://zozo123.github.io/databases-in-the-ai-era/",
      title: "Databases in the AI Era", tldr: "An essay on database systems built for agent workloads." },
    { slug: "the-living-layer", url: "https://zozo123.github.io/the-living-layer/",
      title: "The Living Layer", tldr: "A speculative architecture thesis, with prototypes and upstream tools identified separately.", noImage: true },
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

/* Render the archive from trusted, checked-in data. */
document.querySelectorAll(".figure-grid").forEach((grid) => {
  const projects = FIGSETS[grid.dataset.figset] || [];
  grid.innerHTML = projects.map((project) => `
    <a class="figure-card" href="${project.url}">
      ${project.noImage ? "" : `<span class="figure-thumb"><img src="${project.image || `assets/thumbs/${project.slug}.jpg`}" alt="" width="760" height="475" loading="lazy"></span>`}
      <span class="figure-body">
        <span class="figure-title">${project.title}</span>
        <span class="figure-tldr">${project.tldr}</span>
        <span class="figure-link">Read experiment</span>
      </span>
    </a>`).join("");
  grid.querySelectorAll("img").forEach((image) => {
    const hideMissingThumbnail = () => image.parentElement.classList.add("thumb-missing");
    image.addEventListener("error", hideMissingThumbnail);
    if (image.complete && !image.naturalWidth) hideMissingThumbnail();
  });
});

/* Preserve direct links into collapsed archive sections. */
function openLinkedArchive() {
  const target = document.getElementById(location.hash.slice(1));
  if (target instanceof HTMLDetailsElement) target.open = true;
}
openLinkedArchive();
window.addEventListener("hashchange", openLinkedArchive);
