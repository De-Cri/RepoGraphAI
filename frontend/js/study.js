const navItems = document.querySelectorAll(".nav-item");
const tabPanels = document.querySelectorAll(".tab-panel");

const levelSelect = document.getElementById("levelSelect");
const subjectSelect = document.getElementById("subjectSelect");
const topicInput = document.getElementById("topicInput");
const responseInput = document.getElementById("responseInput");

const startSimulationBtn = document.getElementById("startSimulationBtn");
const submitAnswerBtn = document.getElementById("submitAnswerBtn");
const setupHint = document.getElementById("setupHint");

const charCount = document.getElementById("charCount");
const timerValue = document.getElementById("timerValue");
const evaluationContent = document.getElementById("evaluationContent");
const historyList = document.getElementById("historyList");

const examsTaken = document.getElementById("examsTaken");
const avgScore = document.getElementById("avgScore");
const bestSubject = document.getElementById("bestSubject");

const inlineExams = document.getElementById("inlineExams");
const inlineAvg = document.getElementById("inlineAvg");
const inlineBest = document.getElementById("inlineBest");

const appState = {
  attempts: [],
  timerSeconds: 0,
  timerId: null,
};

function switchTab(tabName) {
  navItems.forEach((item) => {
    item.classList.toggle("active", item.dataset.tab === tabName);
  });

  tabPanels.forEach((panel) => {
    panel.classList.toggle("active", panel.id === `panel-${tabName}`);
  });
}

navItems.forEach((item) => {
  item.addEventListener("click", () => {
    switchTab(item.dataset.tab);
  });
});

function formatSeconds(totalSeconds) {
  const minutes = Math.floor(totalSeconds / 60)
    .toString()
    .padStart(2, "0");
  const seconds = (totalSeconds % 60).toString().padStart(2, "0");
  return `${minutes}:${seconds}`;
}

function resetTimer() {
  if (appState.timerId) {
    clearInterval(appState.timerId);
    appState.timerId = null;
  }
  appState.timerSeconds = 0;
  timerValue.textContent = "00:00";
}

function startTimerIfNeeded() {
  if (appState.timerId || responseInput.value.length === 0) {
    return;
  }

  appState.timerId = setInterval(() => {
    appState.timerSeconds += 1;
    timerValue.textContent = formatSeconds(appState.timerSeconds);
  }, 1000);
}

responseInput.addEventListener("input", () => {
  charCount.textContent = responseInput.value.length;
  startTimerIfNeeded();
});

function updateStats() {
  const attempts = appState.attempts;
  const total = attempts.length;

  const avg = total
    ? Math.round(attempts.reduce((sum, item) => sum + item.score, 0) / total)
    : 0;

  const subjectScores = {};
  attempts.forEach((item) => {
    if (!subjectScores[item.subject]) {
      subjectScores[item.subject] = [];
    }
    subjectScores[item.subject].push(item.score);
  });

  let best = "-";
  let bestAvg = -1;
  Object.keys(subjectScores).forEach((subject) => {
    const values = subjectScores[subject];
    const subjectAvg = values.reduce((sum, score) => sum + score, 0) / values.length;
    if (subjectAvg > bestAvg) {
      bestAvg = subjectAvg;
      best = subject;
    }
  });

  examsTaken.textContent = String(total);
  avgScore.textContent = `${avg} / 30`;
  bestSubject.textContent = best;

  inlineExams.textContent = String(total);
  inlineAvg.textContent = `${avg} / 30`;
  inlineBest.textContent = best;
}

function addHistoryEntry(entry) {
  if (appState.attempts.length === 1) {
    historyList.innerHTML = "";
  }

  const listItem = document.createElement("li");
  listItem.textContent = `${entry.date} - ${entry.subject} (${entry.level}) - Score ${entry.score}/30`;
  historyList.prepend(listItem);
}

startSimulationBtn.addEventListener("click", () => {
  const level = levelSelect.value;
  const subject = subjectSelect.value;
  const topic = topicInput.value.trim();

  if (!level || !subject || !topic) {
    setupHint.textContent = "Complete level, subject, and topic to start the simulation.";
    return;
  }

  switchTab("simulation");
  setupHint.textContent = `Simulation ready for ${subject} (${level}) on \"${topic}\".`;
  responseInput.value = "";
  charCount.textContent = "0";
  evaluationContent.className = "placeholder-box";
  evaluationContent.textContent = "Write your response, then submit to receive AI evaluation.";
  resetTimer();
  responseInput.focus();
});

submitAnswerBtn.addEventListener("click", () => {
  const level = levelSelect.value;
  const subject = subjectSelect.value;
  const topic = topicInput.value.trim();
  const response = responseInput.value.trim();

  if (!level || !subject || !topic) {
    setupHint.textContent = "Set level, subject, and topic before submitting.";
    return;
  }

  if (response.length < 40) {
    evaluationContent.className = "placeholder-box";
    evaluationContent.textContent = "Response too short. Provide at least 40 characters for a realistic evaluation.";
    return;
  }

  evaluationContent.className = "placeholder-box";
  evaluationContent.innerHTML = `
    <div class="loader" aria-label="Loading"></div>
    <p>Evaluating your response...</p>
  `;

  setTimeout(() => {
    const entry = {
      level,
      subject,
      topic,
      score: 24,
      date: new Date().toLocaleDateString(),
    };

    appState.attempts.push(entry);
    addHistoryEntry(entry);
    updateStats();

    evaluationContent.className = "";
    evaluationContent.innerHTML = `
      <p class="score-pill">Score: 24/30</p>
      <h4>Breakdown</h4>
      <ul class="breakdown-list">
        <li>Clarity: 8/10</li>
        <li>Completeness: 7/10</li>
        <li>Accuracy: 9/10</li>
      </ul>
      <h4>Strengths</h4>
      <ul class="bullet-list">
        <li>Strong structure and sequencing.</li>
        <li>Good use of subject vocabulary in ${subject}.</li>
      </ul>
      <h4>Weaknesses</h4>
      <ul class="bullet-list">
        <li>Some key claims need clearer evidence.</li>
        <li>Closing summary can be sharper.</li>
      </ul>
      <h4>Follow-up Questions</h4>
      <ul class="bullet-list">
        <li>How would you connect this to a real-world scenario?</li>
        <li>What misconception about ${topic} should be avoided?</li>
      </ul>
    `;
  }, 2000);
});

updateStats();
switchTab("dashboard");
