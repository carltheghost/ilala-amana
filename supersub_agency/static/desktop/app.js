/**
 * SuperSub 4D Command Deck — hyperspace canvas + agency API surface.
 */

const $ = (sel, root = document) => root.querySelector(sel);
const $$ = (sel, root = document) => [...root.querySelectorAll(sel)];

// ——— Hyperspace (Three.js) ———

function initHyperspace() {
  const canvas = $("#hyperspace");
  if (!window.THREE) {
    console.warn("Three.js not loaded; skipping hyperspace.");
    return null;
  }

  try {
    const scene = new THREE.Scene();
    const camera = new THREE.PerspectiveCamera(60, window.innerWidth / window.innerHeight, 0.1, 2000);
    camera.position.z = 42;

    const renderer = new THREE.WebGLRenderer({ canvas, antialias: false, alpha: true, failIfMajorPerformanceCaveat: false });
    renderer.setPixelRatio(1);
    renderer.setSize(window.innerWidth, window.innerHeight);
    renderer.setClearColor(0x03040a, 1);

  const particles = 4200;
  const positions = new Float32Array(particles * 3);
  const colors = new Float32Array(particles * 3);
  for (let i = 0; i < particles; i++) {
    const radius = 20 + Math.random() * 180;
    const theta = Math.random() * Math.PI * 2;
    const phi = Math.acos(2 * Math.random() - 1);
    positions[i * 3] = radius * Math.sin(phi) * Math.cos(theta);
    positions[i * 3 + 1] = radius * Math.sin(phi) * Math.sin(theta);
    positions[i * 3 + 2] = radius * Math.cos(phi);
    const mix = Math.random();
    colors[i * 3] = 0.2 + mix * 0.6;
    colors[i * 3 + 1] = 0.5 + (1 - mix) * 0.5;
    colors[i * 3 + 2] = 0.9;
  }

  const particleGeo = new THREE.BufferGeometry();
  particleGeo.setAttribute("position", new THREE.BufferAttribute(positions, 3));
  particleGeo.setAttribute("color", new THREE.BufferAttribute(colors, 3));
  const particleMat = new THREE.PointsMaterial({
    size: 0.55,
    vertexColors: true,
    transparent: true,
    opacity: 0.75,
    blending: THREE.AdditiveBlending,
    depthWrite: false,
  });
  const starfield = new THREE.Points(particleGeo, particleMat);
  scene.add(starfield);

  const hyperGroup = new THREE.Group();
  const edgeMat = new THREE.LineBasicMaterial({
    color: 0x3ef0ff,
    transparent: true,
    opacity: 0.35,
  });
  const hyperMat2 = new THREE.LineBasicMaterial({
    color: 0xff4fd8,
    transparent: true,
    opacity: 0.28,
  });

  const verts4d = [];
  for (let i = 0; i < 16; i++) {
    verts4d.push([
      (i & 1) ? 1 : -1,
      (i & 2) ? 1 : -1,
      (i & 4) ? 1 : -1,
      (i & 8) ? 1 : -1,
    ]);
  }
  const edges = [];
  for (let a = 0; a < 16; a++) {
    for (let b = a + 1; b < 16; b++) {
      let diff = 0;
      for (let d = 0; d < 4; d++) {
        if (verts4d[a][d] !== verts4d[b][d]) diff++;
      }
      if (diff === 1) edges.push([a, b]);
    }
  }

  function project4D(v, wAngle, vAngle) {
    const w = Math.cos(wAngle) * v[3] - Math.sin(wAngle) * v[0];
    const x = Math.sin(wAngle) * v[3] + Math.cos(wAngle) * v[0];
    const y = v[1];
    const z = v[2];
    const scale = 2.8 / (3.2 - w);
    const x3 = x * scale;
    const y3 = y * scale;
    const z3 = z * scale + Math.sin(vAngle) * w * 0.4;
    return new THREE.Vector3(x3 * 5, y3 * 5, z3 * 5);
  }

  const linePairs = edges.map(([a, b]) => {
    const geo = new THREE.BufferGeometry();
    const line = new THREE.Line(geo, Math.random() > 0.5 ? edgeMat : hyperMat2);
    hyperGroup.add(line);
    return { line, a, b };
  });
  scene.add(hyperGroup);

  const grid = new THREE.GridHelper(120, 40, 0x9b6bff, 0x1a2040);
  grid.position.y = -28;
  grid.material.opacity = 0.22;
  grid.material.transparent = true;
  scene.add(grid);

  let pointerX = 0;
  let pointerY = 0;
  let scrollW = 0;
  window.addEventListener("pointermove", (e) => {
    pointerX = (e.clientX / window.innerWidth - 0.5) * 2;
    pointerY = (e.clientY / window.innerHeight - 0.5) * 2;
  });
  window.addEventListener(
    "wheel",
    (e) => {
      scrollW = Math.max(-2, Math.min(2, scrollW + e.deltaY * 0.001));
    },
    { passive: true }
  );

  const clock = new THREE.Clock();

  function animate() {
    requestAnimationFrame(animate);
    const t = clock.getElapsedTime();
    const wAngle = t * 0.35 + scrollW;
    const vAngle = t * 0.22;

    starfield.rotation.y = t * 0.02;
    starfield.rotation.x = pointerY * 0.08;

    for (const { line, a, b } of linePairs) {
      const p1 = project4D(verts4d[a], wAngle, vAngle);
      const p2 = project4D(verts4d[b], wAngle, vAngle);
      line.geometry.setFromPoints([p1, p2]);
    }
    hyperGroup.rotation.x = pointerY * 0.25;
    hyperGroup.rotation.y = pointerX * 0.35 + t * 0.15;

    camera.position.x = pointerX * 6;
    camera.position.y = -pointerY * 4;
    camera.lookAt(0, 0, 0);

    renderer.render(scene, camera);
  }
  animate();

  window.addEventListener("resize", () => {
    camera.aspect = window.innerWidth / window.innerHeight;
    camera.updateProjectionMatrix();
    renderer.setSize(window.innerWidth, window.innerHeight);
  });

    return { setIntensity: (factor) => {
      particleMat.opacity = 0.45 + factor * 0.4;
      edgeMat.opacity = 0.2 + factor * 0.25;
    }};
  } catch (err) {
    console.warn("WebGL initialization failed:", err);
    if (canvas) canvas.style.display = 'none';
    return null;
  }
}

// ——— Deck UI ———

let hyperspace = null;
let timeSlice = 0;

function startTimeSlice() {
  setInterval(() => {
    timeSlice += 1;
    const el = $("#time-slice");
    if (el) el.textContent = `T+${timeSlice}`;
  }, 1000);
}

function updateHyperDepth() {
  const deck = $("#deck");
  const depthEl = $("#hyper-depth");
  if (!deck || !depthEl) return;
  const w = 4 + (parseFloat(getComputedStyle(deck).getPropertyValue("--parallax-w")) || 0);
  depthEl.textContent = w.toFixed(2);
}

function initParallax() {
  const deck = $("#deck");
  window.addEventListener("pointermove", (e) => {
    const x = (e.clientX / window.innerWidth - 0.5) * 2;
    const y = (e.clientY / window.innerHeight - 0.5) * 2;
    deck.style.setProperty("--parallax-x", x.toFixed(3));
    deck.style.setProperty("--parallax-y", y.toFixed(3));
    const panels = $$(".panel.active");
    panels.forEach((p, i) => {
      const z = 12 + i * 4;
      p.style.transform = `translateZ(0) rotateX(${-y * 2}deg) rotateY(${x * 2}deg) translateZ(${z}px)`;
    });
  });
  window.addEventListener("wheel", (e) => {
    const cur = parseFloat(deck.style.getPropertyValue("--parallax-w") || "0");
    deck.style.setProperty("--parallax-w", Math.max(-1, Math.min(1, cur + e.deltaY * 0.002)).toFixed(3));
    updateHyperDepth();
  });
}

function setPanel(name) {
  $$(".dock-item").forEach((btn) => {
    btn.classList.toggle("active", btn.dataset.panel === name);
  });
  $$(".panel").forEach((p) => {
    p.classList.toggle("active", p.dataset.panel === name);
  });
  $("#agency-core")?.classList.toggle("dim", name !== "mission");
}

function setStatus(text) {
  const el = $("#status-text");
  if (el) el.textContent = text;
}

function setRisk(level, running = false) {
  const pill = $("#risk-pill");
  if (!pill) return;
  pill.className = "metric risk-pill";
  if (running) pill.classList.add("running");
  if (level) pill.classList.add(level);
  pill.textContent = running ? "ROUTING" : (level || "IDLE").toUpperCase();
}

async function loadCapabilities() {
  const grid = $("#lane-grid");
  try {
    const res = await fetch("/api/capabilities");
    const data = await res.json();
    grid.innerHTML = "";
    for (const p of data.providers || []) {
      const card = document.createElement("article");
      card.className = "lane-card";
      card.innerHTML = `
        <h3>${escapeHtml(p.name)}</h3>
        <p>${escapeHtml(p.role)}</p>
        <div class="lane-tags">
          ${(p.strengths || []).map((s) => `<span>${escapeHtml(s)}</span>`).join("")}
        </div>
      `;
      grid.appendChild(card);
    }
    setStatus(`${data.providers?.length || 0} lanes online in provider mixer`);
  } catch {
    grid.innerHTML = "<p class='loading'>Could not load lanes. Is the command deck server running?</p>";
  }
}

function escapeHtml(str) {
  return String(str)
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;")
    .replace(/"/g, "&quot;");
}

function renderResponse(payload) {
  const r = payload.response;
  $("#hero-intent").textContent = r.intent;
  $("#hero-specialist").textContent = `${r.specialist} · ${r.model_route}`;
  $("#response-meta").textContent = r.summary;

  setRisk(r.risk_level);

  const stream = $("#tool-stream");
  stream.innerHTML = "";
  (r.tool_results || []).forEach((tool, i) => {
    const card = document.createElement("article");
    card.className = "tool-card" + (tool.requires_approval ? " approval" : "");
    card.style.animationDelay = `${i * 0.08}s`;
    const steps = (tool.next_steps || [])
      .map((s) => `<li>${escapeHtml(s)}</li>`)
      .join("");
    card.innerHTML = `
      <h4>${escapeHtml(tool.tool_name)}${tool.requires_approval ? " · approval required" : ""}</h4>
      <p>${escapeHtml(tool.summary)}</p>
      ${steps ? `<ul>${steps}</ul>` : ""}
    `;
    stream.appendChild(card);
  });

  const gates = $("#gates-list");
  gates.innerHTML = "";
  (r.gated_actions || []).forEach((g) => {
    const li = document.createElement("li");
    li.textContent = g;
    gates.appendChild(li);
  });
  $("#gates-fold").open = (r.gated_actions || []).length > 0;
}

async function runMission() {
  const mission = $("#mission-input").value.trim();
  if (!mission) {
    setStatus("Enter a mission before launching.");
    return;
  }

  const budgetRaw = $("#budget-input").value;
  const body = { mission };
  if (budgetRaw) body.budget_usd = parseFloat(budgetRaw);

  const btn = $("#btn-run-mission");
  const core = $("#agency-core");
  btn.disabled = true;
  core?.classList.add("processing");
  setRisk(null, true);
  hyperspace?.setIntensity?.(1);
  setStatus("Coordinator routing mission through specialist lanes…");

  try {
    const res = await fetch("/api/mission", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(body),
    });
    const data = await res.json();
    if (!res.ok) throw new Error(data.error || "Mission failed");

    renderResponse(data);
    setPanel("response");
    setStatus(`Mission complete · intent ${data.response.intent} · specialist ${data.response.specialist}`);
  } catch (err) {
    setStatus(`Error: ${err.message}`);
    setRisk("high");
  } finally {
    btn.disabled = false;
    core?.classList.remove("processing");
    hyperspace?.setIntensity?.(0.5);
  }
}

function wireUi() {
  $$(".dock-item[data-panel]").forEach((btn) => {
    btn.addEventListener("click", () => setPanel(btn.dataset.panel));
  });

  $("#btn-run-mission")?.addEventListener("click", runMission);
  $("#btn-focus-core")?.addEventListener("click", () => {
    $("#agency-core")?.classList.remove("dim");
    setPanel("mission");
  });

  $$(".chip[data-mission]").forEach((chip) => {
    chip.addEventListener("click", () => {
      $("#mission-input").value = chip.dataset.mission;
      runMission();
    });
  });

  $("#mission-input")?.addEventListener("keydown", (e) => {
    if (e.key === "Enter" && (e.metaKey || e.ctrlKey)) runMission();
  });
}

// ——— Boot ———

hyperspace = initHyperspace();
initParallax();
startTimeSlice();
updateHyperDepth();
wireUi();
loadCapabilities();
setPanel("mission");
