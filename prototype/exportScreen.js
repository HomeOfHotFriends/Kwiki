export function showExport(state) {
  let div = document.getElementById('export');
  if (!div) {
    div = document.createElement('div');
    div.id = 'export';
    div.className = 'screen';
    div.innerHTML = `
      <h2>4. Export</h2>
      <button id="download-html">Download HTML</button>
      <button id="download-json">Download JSON</button>
      <div id="export-preview"></div>
    `;
    document.getElementById('app').appendChild(div);
  }
  div.querySelector('#download-html').onclick = () => {
    const html = exportHTML(state);
    downloadFile('performance.html', html, 'text/html');
  };
  div.querySelector('#download-json').onclick = () => {
    const json = JSON.stringify({
      mapping: state.mapping,
      tokens: state.tokens,
      performance: state.performance
    }, null, 2);
    downloadFile('performance.json', json, 'application/json');
  };
  div.querySelector('#export-preview').innerHTML = exportHTML(state);
}

function exportHTML(state) {
  // HTML export: words with inline style for volume (font-size) and pitch (color)
  let html = `<div style="line-height:2">`;
  const perf = state.performance;
  for (let i=0; i<state.tokens.length; ++i) {
    const v = perf.wordData[i]?.volume || [];
    const p = perf.wordData[i]?.pitch || [];
    const avg = v.length ? v.reduce((a,b)=>a+b,0)/v.length : 0.1;
    const avgP = p.length ? p.reduce((a,b)=>a+b,0)/p.length : 0;
    const size = 1 + avg*2;
    // Map pitch to color (blue=low, red=high)
    let color = '#333';
    if (avgP > 0) {
      const minP = 80, maxP = 400;
      const t = Math.max(0, Math.min(1, (avgP-minP)/(maxP-minP)));
      const r = Math.round(50 + 205*t);
      const b = Math.round(255 - 205*t);
      color = `rgb(${r},60,${b})`;
    }
    html += `<span style="font-size:${size}em;color:${color}">${state.tokens[i]}</span> `;
  }
  html += `</div>`;
  return html;
}

function downloadFile(filename, content, mime) {
  const a = document.createElement('a');
  a.href = URL.createObjectURL(new Blob([content], {type: mime}));
  a.download = filename;
  a.click();
}
