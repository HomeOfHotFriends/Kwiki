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
  // HTML export: words with inline style for volume (font-size) and pitch deviation (color)
  let html = `<div style=\"line-height:2\">`;
  const perf = state.performance;
  // Compute global pitch baseline (mean of all word means)
  let allPitches = [];
  for (let i=0; i<state.tokens.length; ++i) {
    const p = perf.wordData[i]?.pitch || [];
    if (p.length) allPitches.push(p.reduce((a,b)=>a+b,0)/p.length);
  }
  const baseline = allPitches.length ? allPitches.reduce((a,b)=>a+b,0)/allPitches.length : 150;
  // Compute stddev for normalization
  const std = allPitches.length ? Math.sqrt(allPitches.map(x => (x-baseline)**2).reduce((a,b)=>a+b,0)/allPitches.length) : 1;
  for (let i=0; i<state.tokens.length; ++i) {
    const v = perf.wordData[i]?.volume || [];
    const p = perf.wordData[i]?.pitch || [];
    const avg = v.length ? v.reduce((a,b)=>a+b,0)/v.length : 0.1;
    const avgP = p.length ? p.reduce((a,b)=>a+b,0)/p.length : 0;
    const size = 1 + avg*2;
    // Map pitch deviation to color (blue=below, red=above, gray=neutral)
    let color = '#333';
    if (avgP > 0 && std > 0) {
      let z = (avgP - baseline) / std;
      z = Math.max(-2, Math.min(2, z)); // clamp
      // z < 0: blue, z > 0: red, z ~ 0: gray
      if (z < 0) {
        const t = Math.abs(z)/2;
        const r = Math.round(80*(1-t));
        const g = Math.round(80*(1-t)+120*t);
        const b = Math.round(255 - 100*t);
        color = `rgb(${r},${g},${b})`;
      } else if (z > 0) {
        const t = z/2;
        const r = Math.round(255 - 100*t);
        const g = Math.round(80*(1-t)+120*t);
        const b = Math.round(80*(1-t));
        color = `rgb(${r},${g},${b})`;
      } else {
        color = '#333';
      }
    }
    html += `<span style=\"font-size:${size}em;color:${color}\">${state.tokens[i]}</span> `;
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
