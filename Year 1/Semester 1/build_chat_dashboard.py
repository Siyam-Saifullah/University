#!/usr/bin/env python3
from pathlib import Path

out = Path("D:/Academic/Year 1/Semester 1/MSE_1st_Semester_Dashboard.html")

html = r'''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>MSE 1st Semester | RU 2025-26</title>
<style>
:root {
  --bg: #0b0f1a;
  --card: #111827;
  --border: #1f2937;
  --text: #f3f4f6;
  --muted: #9ca3af;
  --accent: #22d3ee;
  --accent2: #34d399;
  --warn: #fbbf24;
  --danger: #f87171;
}
* { box-sizing: border-box; }
body { margin: 0; font-family: ui-sans-serif, system-ui, -apple-system, Segoe UI, Roboto, Helvetica, Arial, sans-serif; background: var(--bg); color: var(--text); }
.container { max-width: 1200px; margin: 0 auto; padding: 16px; }
.header { display: flex; justify-content: space-between; align-items: flex-end; padding-bottom: 14px; border-bottom: 1px solid var(--border); margin-bottom: 16px; gap: 12px; flex-wrap: wrap; }
.title h1 { font-size: 1.4rem; font-weight: 700; }
.title p { color: var(--muted); font-size: 0.85rem; margin-top: 4px; }
.badge-row { display: flex; gap: 8px; margin-top: 6px; flex-wrap: wrap; }
.badge { background: var(--card); color: var(--accent); padding: 4px 10px; border-radius: 999px; font-size: 0.75rem; font-weight: 600; border: 1px solid var(--border); }
.stat { background: var(--card); border: 1px solid var(--border); padding: 10px 14px; border-radius: 10px; text-align: center; min-width: 72px; }
.stat .value { font-family: ui-monospace, monospace; font-size: 1.2rem; font-weight: 700; color: var(--accent); }
.stat .label { font-size: 0.65rem; color: var(--muted); text-transform: uppercase; }

.stats { display: flex; gap: 10px; flex-wrap: wrap; }
.layout { display: grid; grid-template-columns: 1fr 300px; gap: 16px; }
@media (max-width: 980px) { .layout { grid-template-columns: 1fr; } }
.card + .card { margin-top: 14px; }
.card { background: var(--card); border: 1px solid var(--border); border-radius: 12px; overflow: hidden; }
.card-header { display: flex; justify-content: space-between; align-items: center; padding: 12px 14px; border-bottom: 1px solid var(--bg); background: #111827; gap: 10px; flex-wrap: wrap; }
.card-header h2 { font-size: 0.95rem; font-weight: 600; display: flex; align-items: center; gap: 8px; }
.card-body { padding: 14px; }

/* Chat */
.chat-block { padding: 0; }
.chat-log { max-height: 320px; overflow-y: auto; padding: 12px; display: flex; flex-direction: column; gap: 10px; }
.chat-log .empty-state { margin-top: 20px; }
.chat-msg { max-width: 85%; display: flex; flex-direction: column; gap: 4px; }
.chat-msg.user { align-self: flex-end; }
.chat-msg.assistant { align-self: flex-start; }
.chat-bubble { padding: 10px 12px; border-radius: 12px; font-size: 0.85rem; line-height: 1.45; white-space: pre-wrap; }
.user .chat-bubble { background: rgba(34,211,238,0.18); color: var(--text); border: 1px solid rgba(34,211,238,0.25); }
.assistant .chat-bubble { background: var(--bg); color: var(--text); border: 1px solid var(--border); }
.chat-meta { font-size: 0.7rem; color: var(--muted); padding: 0 4px; }
.chat-bar { display: flex; gap: 8px; padding: 12px; border-top: 1px solid var(--bg); background: var(--card); }
.chat-input { flex: 1; background: var(--bg); border: 1px solid var(--border); color: var(--text); padding: 10px 12px; border-radius: 10px; font-size: 0.85rem; min-width: 0; }
.chat-send { background: var(--accent); color: var(--bg); border: none; padding: 10px 14px; border-radius: 10px; font-weight: 700; cursor: pointer; }
.chat-clear { background: var(--bg); color: var(--muted); border: 1px solid var(--border); padding: 10px 12px; border-radius: 10px; font-size: 0.8rem; cursor: pointer; }

/* Courses */
.courses { display: grid; grid-template-columns: repeat(auto-fill, minmax(220px, 1fr)); gap: 12px; }
.course {
  background: #111827;
  border: 1px solid var(--bg);
  border-radius: 10px;
  padding: 14px;
  transition: all 0.2s;
  position: relative;
}
.course:hover { border-color: var(--border); transform: translateY(-2px); }
.course::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 3px;
  background: var(--accent);
  border-radius: 10px 10px 0 0;
}
.course-head { display: flex; justify-content: space-between; align-items: center; margin-bottom: 6px; }
.course-code { font-family: ui-monospace, monospace; font-size: 0.75rem; font-weight: 700; color: var(--accent); background: rgba(34,211,238,0.1); padding: 3px 8px; border-radius: 4px; }
.course-credits { font-size: 0.7rem; color: var(--muted); }
.course-title { font-size: 0.9rem; font-weight: 600; margin: 6px 0; }
.course-teacher { font-size: 0.8rem; color: var(--muted); margin-bottom: 10px; }
.course-meta { display: flex; gap: 6px; flex-wrap: wrap; }
.course-meta span { background: var(--bg); padding: 3px 8px; border-radius: 6px; font-size: 0.75rem; color: var(--muted); border: 1px solid var(--border); }

/* Sidebar */
.sidebar { display: flex; flex-direction: column; gap: 14px; }
.quick-stats { display: grid; grid-template-columns: repeat(3, 1fr); gap: 8px; }
.quick-stat { background: #111827; padding: 10px; border-radius: 10px; text-align: center; border: 1px solid var(--bg); }
.quick-stat .value { font-family: ui-monospace, monospace; font-size: 1.1rem; font-weight: 700; color: var(--accent); }
.quick-stat .label { font-size: 0.7rem; color: var(--muted); text-transform: uppercase; margin-top: 2px; }

/* Modal */
.modal { display: none; position: fixed; inset: 0; background: rgba(0,0,0,0.82); z-index: 1000; padding: 20px; align-items: center; justify-content: center; backdrop-filter: blur(4px); }
.modal.active { display: flex; }
.modal-content { background: var(--card); border-radius: 14px; max-width: 520px; width: 100%; max-height: 85vh; overflow-y: auto; border: 1px solid var(--border); }
.modal-header { display: flex; justify-content: space-between; align-items: center; padding: 12px 16px; border-bottom: 1px solid var(--bg); background: #111827; }
.modal-header h3 { font-size: 0.95rem; }
.modal-close { background: none; border: none; color: var(--muted); font-size: 1.5rem; cursor: pointer; }
.modal-body { padding: 14px; }
.form-group { margin-bottom: 14px; }
.form-group label { display: block; font-size: 0.8rem; color: var(--muted); margin-bottom: 4px; }
.form-group input, .form-group select, .form-group textarea {
  width: 100%;
  background: var(--bg);
  border: 1px solid var(--border);
  color: var(--text);
  padding: 8px;
  border-radius: 8px;
  font-size: 0.85rem;
}
.form-group textarea { resize: vertical; min-height: 140px; font-family: ui-monospace, monospace; }
.form-actions { display: flex; gap: 8px; justify-content: flex-end; }
.btn { padding: 8px 14px; border-radius: 8px; font-size: 0.8rem; font-weight: 600; cursor: pointer; border: 1px solid var(--border); background: var(--bg); color: var(--text); transition: all 0.2s; }
.btn.primary { background: var(--accent); color: var(--bg); border-color: var(--accent); font-weight: 700; }
.btn.danger { background: var(--danger); color: white; border-color: var(--danger); }
.btn:hover { background: var(--border); }
</style>
</head>
<body>
<div class="container">
  <header class="header">
    <div class="title">
      <h1>MSE 1st Semester</h1>
      <p>RU • Materials Science & Engineering • 2025-26</p>
      <div class="badge-row">
        <span class="badge">10 Courses</span>
        <span class="badge">18 Credits</span>
        <span class="badge">450 Marks</span>
      </div>
    </div>
    <div class="stats">
      <div class="stat"><div class="value">10</div><div class="label">Courses</div></div>
      <div class="stat"><div class="value">18</div><div class="label">Credits</div></div>
      <div class="stat"><div class="value">450</div><div class="label">Total</div></div>
    </div>
  </header>

  <div class="layout">
    <main>
      <section class="card">
        <div class="card-header"><h2>Courses</h2></div>
        <div class="card-body">
          <div class="courses" id="coursesList"></div>
        </div>
      </section>
    </main>
    <aside class="sidebar">
      <section class="card chat-block">
        <div class="card-header"><h2>Chat</h2></div>
        <div class="chat-log" id="chatLog">
          <div class="empty-state" style="color:var(--muted);font-size:0.85rem;">No messages yet. Ask something or say <strong>help</strong>.</div>
        </div>
        <div class="chat-bar">
          <input id="chatInput" class="chat-input" placeholder="Type a message..." autocomplete="off">
          <button id="chatSend" class="chat-send">Send</button>
          <button id="chatClear" class="chat-clear">Clear</button>
        </div>
      </section>
      <section class="card">
        <div class="card-header"><h2>Stats</h2></div>
        <div class="card-body">
          <div class="quick-stats" id="quickStats"></div>
        </div>
      </section>
    </aside>
  </div>
</div>

<!-- Modal: Edit Routine -->
<div class="modal" id="rawModal">
  <div class="modal-content" style="max-width:720px">
    <div class="modal-header">
      <h3>Edit Routine (Raw Text)</h3>
      <button class="modal-close" id="closeRaw">×</button>
    </div>
    <div class="modal-body">
      <div class="form-group">
        <label>Paste your routine in this format:</label>
        <textarea id="rawEditor" placeholder="Sunday\n10.15-11.15\nIntroduction to MSE\nA.A.Mamun Sir\n\nMonday\n09.00-10.00\nMathematics\nProf. Rahman"></textarea>
      </div>
      <div class="form-actions">
        <button class="btn danger" id="clearRoutine">Clear All</button>
        <button class="btn" id="cancelRaw">Cancel</button>
        <button class="btn primary" id="updateRoutine">Update Routine</button>
      </div>
    </div>
  </div>
</div>

<script>
const STORAGE_KEY = 'mse_routines';
const courses = [
  { code: 'MSE1111', title: 'Introduction to MSE', teacher: 'A.A. Mamun Sir', credits: 3, marks: 100 },
  { code: 'MSE1121', title: 'Crystallography I', teacher: 'Jesmin Sultana Mam', credits: 3, marks: 100 },
  { code: 'MSE1122', title: 'Crystallography I Sessional', teacher: '', credits: 1, marks: 50 },
  { code: 'MATH1111', title: 'Matrices, Vector Analysis and Geometry', teacher: '', credits: 3, marks: 100 },
  { code: 'PHY1111', title: 'Electricity and Magnetism', teacher: 'Mijanur Rahman Sir', credits: 3, marks: 100 },
  { code: 'PHY1112', title: 'Electricity and Magnetism Sessional', teacher: '', credits: 1, marks: 50 },
  { code: 'CHEM1111', title: 'Organic Chemistry', teacher: '', credits: 3, marks: 100 },
  { code: 'CHEM1112', title: 'Organic Chemistry Sessional', teacher: '', credits: 1, marks: 50 },
  { code: 'ENG1111', title: 'Technical English', teacher: '', credits: 2, marks: 75 },
  { code: 'MSE1112', title: 'Engineering Drawing', teacher: '', credits: 2, marks: 75 }
];

function renderCourses() {
  const container = document.getElementById('coursesList');
  container.innerHTML = courses.map(c => `
    <div class="course">
      <div class="course-head">
        <span class="course-code">${c.code}</span>
        <span class="course-credits">${c.credits} cr</span>
      </div>
      <div class="course-title">${c.title}</div>
      <div class="course-teacher">${c.teacher || 'Not assigned'}</div>
      <div class="course-meta">
        <span>${c.marks} marks</span>
      </div>
    </div>
  `).join('');
}

function updateStats() {
  const el = document.getElementById('quickStats')
  const credits = courses.reduce((s,c)=>s + Number(c.credits), 0)
  const marks = courses.reduce((s,c)=>s + Number(c.marks), 0)
  el.innerHTML = `
    <div class="quick-stat"><div class="value">${courses.length}</div><div class="label">Courses</div></div>
    <div class="quick-stat"><div class="value">${credits}</div><div class="label">Credits</div></div>
    <div class="quick-stat"><div class="value">${marks}</div><div class="label">Marks</div></div>
  `;
}

/* Chat */
function loadChat() {
  try {
    return JSON.parse(localStorage.getItem('mse_chat') || '[]')
  } catch (e) { return [] }
}
function saveChat(msgs) {
  localStorage.setItem('mse_chat', JSON.stringify(msgs.slice(-200)));
}
function renderChat() {
  const msgs = loadChat();
  const log = document.getElementById('chatLog');
  if (!msgs.length) {
    log.innerHTML = '<div class="empty-state" style="color:var(--muted);font-size:0.85rem;">No messages yet. Ask something or say <strong>help</strong>.</div>';
    return;
  }
  log.innerHTML = msgs.map((m, idx) => `
    <div class="chat-msg ${m.role}">
      <div class="chat-bubble">${escapeHtml(m.text)}</div>
      <div class="chat-meta">${m.role} • ${new Date(m.ts).toLocaleTimeString([], {hour: '2-digit', minute:'2-digit'})}</div>
    </div>
  `).join('');
  log.scrollTop = log.scrollHeight;
}
function escapeHtml(str) {
  return String(str).replace(/[&<>"']/g, function (m) {
    return ({ '&':'&amp;', '<':'&lt;', '>':'&gt;', '"':'&quot;', "'":'&#39;' })[m];
  });
}

/* Simple local demo reply */
function demoReply(text) {
  const t = text.toLowerCase();
  if (/\b(hi|hello|hey)\b/.test(t)) return 'Hi! I’m your study assistant. Ask about CT, mid, final, or any course.';
  if (/\bhelp\b/.test(t)) return 'Try: "How to prepare for CT", "Plan for Crystallography", or "Help me with final strategy".';
  if (/\bct\b/.test(t) || /class test/.test(t)) return 'CT = 30%. Solve at least 10 problems per topic and revise within 24 hours.';
  if (/\bmid\b/.test(t) || /sessional exam/.test(t)) return 'Mid = 20%. Start with previous-year questions and make a 1-page formula sheet per subject.';
  if (/\bfinal\b/.test(t)) return 'Final = 50%. Start 4 weeks early, solve full past papers, and make model answers.';
  if (/\bcrystallography\b/.test(t)) return 'Crystallography is visual. Practice Miller indices, symmetry, and stereographic projections daily.';
  if (/\bmathematics\b/.test(t) || /\bmath\b/.test(t)) return 'Math supports MSE. Prioritize matrices and vector algebra now.';
  return 'This is a demo reply. For full AI chat, connect the backend later. Until then, ask about CT, mid, final, or a course.';
}

function sendMessage() {
  const input = document.getElementById('chatInput');
  const text = input.value.trim();
  if (!text) return;
  const msgs = loadChat();
  msgs.push({ role: 'user', text, ts: Date.now() });
  saveChat(msgs);
  renderChat();
  input.value = '';
  setTimeout(() => {
    const reply = demoReply(text);
    const chat2 = loadChat();
    chat2.push({ role: 'assistant', text: reply, ts: Date.now() });
    saveChat(chat2);
    renderChat();
  }, 300);
}

/* Init */
renderCourses();
updateStats();

document.getElementById('chatSend').addEventListener('click', sendMessage);
document.getElementById('chatInput').addEventListener('keydown', function (e) {
  if (e.key === 'Enter') sendMessage();
});
document.getElementById('chatClear').addEventListener('click', function () {
  localStorage.removeItem('mse_chat');
  renderChat();
});
</script>
</body>
</html>
'''

out.write_text(html, encoding='utf-8')
print(f"Wrote {out}")
