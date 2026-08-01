// Client-side rendering and interaction for the Flask-backed Sudoku
const SIZE = 9;
const STORAGE_KEY = 'sudoku-leaderboard';
const THEME_KEY = 'sudoku-theme';
let puzzle = [];
let startTime = null;
let hintsUsed = 0;
let currentSolution = [];
let timerInterval = null;

function applyTheme(theme) {
  document.body.setAttribute('data-theme', theme);
  document.documentElement.style.colorScheme = theme;
  const toggle = document.getElementById('theme-toggle');
  if (toggle) {
    toggle.setAttribute('aria-pressed', String(theme === 'dark'));
    toggle.textContent = theme === 'dark' ? '☀️ Light Mode' : '🌙 Dark Mode';
  }
}

function initializeTheme() {
  const storedTheme = localStorage.getItem(THEME_KEY);
  const preferredTheme = storedTheme || (window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light');
  applyTheme(preferredTheme);
}

function toggleTheme() {
  const nextTheme = document.body.getAttribute('data-theme') === 'dark' ? 'light' : 'dark';
  localStorage.setItem(THEME_KEY, nextTheme);
  applyTheme(nextTheme);
}

function updateTimer() {
  if (!startTime) {
    return;
  }
  const elapsedSeconds = Math.floor((Date.now() - startTime) / 1000);
  const minutes = String(Math.floor(elapsedSeconds / 60)).padStart(2, '0');
  const seconds = String(elapsedSeconds % 60).padStart(2, '0');
  const timer = document.getElementById('timer');
  if (timer) {
    timer.textContent = `Time: ${minutes}:${seconds}`;
  }
}

function startTimer() {
  stopTimer();
  startTime = Date.now();
  updateTimer();
  timerInterval = window.setInterval(updateTimer, 1000);
}

function stopTimer() {
  if (timerInterval) {
    window.clearInterval(timerInterval);
    timerInterval = null;
  }
}

function createBoardElement() {
  const boardDiv = document.getElementById('sudoku-board');
  boardDiv.innerHTML = '';
  for (let i = 0; i < SIZE; i++) {
    const rowDiv = document.createElement('div');
    rowDiv.className = 'sudoku-row';
    for (let j = 0; j < SIZE; j++) {
      const input = document.createElement('input');
      input.type = 'text';
      input.maxLength = 1;
      const subgridClass = (Math.floor(i / 3) + Math.floor(j / 3)) % 2 === 0 ? 'subgrid-a' : 'subgrid-b';
      input.className = `sudoku-cell ${subgridClass}`;
      input.dataset.row = i;
      input.dataset.col = j;
      input.addEventListener('input', (e) => {
        const val = e.target.value.replace(/[^1-9]/g, '');
        e.target.value = val;
      });
      rowDiv.appendChild(input);
    }
    boardDiv.appendChild(rowDiv);
  }
}

function renderPuzzle(puz, solution = null) {
  puzzle = puz;
  currentSolution = solution || [];
  hintsUsed = 0;
  createBoardElement();
  startTimer();
  const boardDiv = document.getElementById('sudoku-board');
  const inputs = boardDiv.getElementsByTagName('input');
  for (let i = 0; i < SIZE; i++) {
    for (let j = 0; j < SIZE; j++) {
      const idx = i * SIZE + j;
      const val = puzzle[i][j];
      const inp = inputs[idx];
      if (val !== 0) {
        inp.value = val;
        inp.disabled = true;
        inp.classList.add('prefilled');
        inp.classList.remove('incorrect');
      } else {
        inp.value = '';
        inp.disabled = false;
        inp.classList.remove('prefilled', 'incorrect');
      }
    }
  }
}

async function newGame() {
  const res = await fetch('/new');
  const data = await res.json();
  renderPuzzle(data.puzzle, data.solution);
  document.getElementById('message').innerText = '';
}

function useHint() {
  if (currentSolution.length === 0) {
    const msg = document.getElementById('message');
    msg.style.color = '#d32f2f';
    msg.innerText = 'No hint available yet.';
    return;
  }

  const boardDiv = document.getElementById('sudoku-board');
  const inputs = boardDiv.getElementsByTagName('input');
  for (let idx = 0; idx < inputs.length; idx++) {
    const input = inputs[idx];
    if (input.disabled || input.value) {
      continue;
    }

    const row = Math.floor(idx / SIZE);
    const col = idx % SIZE;
    input.value = currentSolution[row][col];
    input.disabled = true;
    input.classList.add('prefilled');
    input.classList.remove('incorrect');
    hintsUsed += 1;
    const msg = document.getElementById('message');
    msg.style.color = '#1565c0';
    msg.innerText = 'Hint used.';
    return;
  }

  const msg = document.getElementById('message');
  msg.style.color = '#1565c0';
  msg.innerText = 'No empty cells left to hint.';
}

function getLeaderboard() {
  const raw = localStorage.getItem(STORAGE_KEY);
  return raw ? JSON.parse(raw) : [];
}

function saveLeaderboard(entries) {
  localStorage.setItem(STORAGE_KEY, JSON.stringify(entries));
}

function renderLeaderboard() {
  const entries = getLeaderboard()
    .sort((a, b) => a.time - b.time)
    .slice(0, 10);
  const body = document.getElementById('leaderboard-body');
  body.innerHTML = '';
  if (entries.length === 0) {
    const row = document.createElement('tr');
    const cell = document.createElement('td');
    cell.colSpan = 5;
    cell.textContent = 'No completed games yet.';
    cell.className = 'empty-state';
    row.appendChild(cell);
    body.appendChild(row);
    return;
  }
  entries.forEach((entry, index) => {
    const row = document.createElement('tr');
    row.innerHTML = `
      <td>${index + 1}</td>
      <td>${entry.playerName}</td>
      <td>${entry.time}s</td>
      <td>${entry.difficulty}</td>
      <td>${entry.hintsUsed}</td>
    `;
    body.appendChild(row);
  });
}

function submitScore(event) {
  event.preventDefault();
  const playerName = document.getElementById('player-name').value.trim() || 'Anonymous';
  const difficulty = document.getElementById('difficulty-select').value;
  if (!startTime) {
    return;
  }
  const timeTaken = Math.round((Date.now() - startTime) / 1000);
  const entries = getLeaderboard();
  entries.push({
    playerName,
    time: timeTaken,
    difficulty,
    hintsUsed,
  });
  const sortedEntries = entries.sort((a, b) => a.time - b.time).slice(0, 10);
  saveLeaderboard(sortedEntries);
  renderLeaderboard();
  document.getElementById('player-name').value = '';
}

async function checkSolution() {
  const boardDiv = document.getElementById('sudoku-board');
  const inputs = boardDiv.getElementsByTagName('input');
  const board = [];
  for (let i = 0; i < SIZE; i++) {
    board[i] = [];
    for (let j = 0; j < SIZE; j++) {
      const idx = i * SIZE + j;
      const val = inputs[idx].value;
      board[i][j] = val ? parseInt(val, 10) : 0;
    }
  }
  const res = await fetch('/check', {
    method: 'POST',
    headers: {'Content-Type': 'application/json'},
    body: JSON.stringify({board})
  });
  const data = await res.json();
  const msg = document.getElementById('message');
  if (data.error) {
    msg.style.color = '#d32f2f';
    msg.innerText = data.error;
    return;
  }
  const incorrect = new Set(data.incorrect.map(x => x[0] * SIZE + x[1]));
  for (let idx = 0; idx < inputs.length; idx++) {
    const inp = inputs[idx];
    if (inp.disabled) {
      continue;
    }
    inp.classList.remove('incorrect');
    if (incorrect.has(idx)) {
      inp.classList.add('incorrect');
    }
  }
  if (incorrect.size === 0) {
    stopTimer();
    msg.style.color = '#388e3c';
    msg.innerText = 'Congratulations! You solved it!';
    document.getElementById('leaderboard-form').dispatchEvent(new Event('submit'));
  } else {
    msg.style.color = '#d32f2f';
    msg.innerText = 'Some cells are incorrect.';
  }
}

// Wire buttons
window.addEventListener('load', () => {
  initializeTheme();
  document.getElementById('new-game').addEventListener('click', newGame);
  document.getElementById('check-solution').addEventListener('click', checkSolution);
  document.getElementById('use-hint').addEventListener('click', useHint);
  document.getElementById('theme-toggle').addEventListener('click', toggleTheme);
  document.getElementById('leaderboard-form').addEventListener('submit', submitScore);
  renderLeaderboard();
  // initialize
  newGame();
});