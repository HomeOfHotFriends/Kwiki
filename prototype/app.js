// Minimal vertical slice for performance-to-typography prototype
import { showMappingBrief } from './mappingBrief.js';
import { showScriptInput } from './scriptInput.js';
import { showPerformance } from './performance.js';
import { showExport } from './exportScreen.js';

const screens = ['mapping-brief', 'script-input', 'performance', 'export'];
let state = {
  mapping: null,
  script: null,
  tokens: [],
  performance: null,
  regions: [],
  exportData: null
};

function showScreen(name) {
  document.querySelectorAll('.screen').forEach(div => div.classList.remove('active'));
  document.getElementById(name).classList.add('active');
}

function nextScreen(current) {
  const idx = screens.indexOf(current);
  if (idx < screens.length - 1) showScreen(screens[idx + 1]);
}

window.appState = state;
window.showScreen = showScreen;
window.nextScreen = nextScreen;

// Initial render
showMappingBrief(state, () => showScreen('script-input'));
showScriptInput(state, () => showScreen('performance'));
showPerformance(state, () => showScreen('export'));
showExport(state);

showScreen('mapping-brief');
