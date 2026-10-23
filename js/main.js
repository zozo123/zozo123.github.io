/* Collected works: motion and the live years-on-GitHub count. All content is static HTML. */
document.body.classList.remove("no-js");

const dateEl = document.getElementById("today-date");
if (dateEl) {
  dateEl.textContent = new Date()
    .toLocaleDateString("en-US", { year: "numeric", month: "short", day: "numeric" })
    .toUpperCase();
}

document.querySelectorAll(".figure-thumb img, .latest-plate img").forEach((image) => {
  const hide = () => image.parentNode.classList.add("thumb-missing");
  image.addEventListener("error", hide);
  if (image.complete && !image.naturalWidth) hide();
});

const reduceMotion = window.matchMedia("(prefers-reduced-motion: reduce)").matches;

if (reduceMotion) {
  document.querySelectorAll(".reveal").forEach((el) => el.classList.add("in"));
} else {
  requestAnimationFrame(() => document.querySelectorAll(".in-load").forEach((el) => el.classList.add("in")));
  const io = new IntersectionObserver((entries) => {
    entries.forEach((e) => {
      if (e.isIntersecting) { e.target.classList.add("in"); io.unobserve(e.target); }
    });
  }, { threshold: 0.08, rootMargin: "0px 0px -4% 0px" });
  document.querySelectorAll(".reveal:not(.in-load)").forEach((el) => io.observe(el));
}

/* Count up to each stat; years on GitHub comes from the public GitHub API when it answers. */
function countUp(el) {
  const target = +el.dataset.count;
  if (reduceMotion) { el.textContent = target; return; }
  const t0 = performance.now(), dur = 1100;
  const tick = (t) => {
    const k = Math.min((t - t0) / dur, 1);
    el.textContent = Math.round(target * (1 - Math.pow(1 - k, 3)));
    if (k < 1) requestAnimationFrame(tick);
  };
  requestAnimationFrame(tick);
}

const stats = document.querySelectorAll(".stat-n");
const live = fetch("https://api.github.com/users/zozo123", { headers: { Accept: "application/vnd.github+json" } })
  .then((r) => (r.ok ? r.json() : null))
  .then((user) => {
    if (!user) return;
    const values = {
      years: new Date().getFullYear() - new Date(user.created_at).getFullYear(),
    };
    stats.forEach((el) => {
      const key = el.dataset.live;
      if (key && Number.isFinite(values[key])) el.dataset.count = values[key];
    });
  })
  .catch(() => {});

const counterIO = new IntersectionObserver((entries) => {
  entries.forEach((e) => {
    if (!e.isIntersecting) return;
    counterIO.unobserve(e.target);
    Promise.race([live, new Promise((r) => setTimeout(r, 900))]).then(() => countUp(e.target));
  });
}, { threshold: 0.5 });
stats.forEach((el) => counterIO.observe(el));
