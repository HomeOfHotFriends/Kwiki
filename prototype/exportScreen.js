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
  };t
  div.querySelector('#export-preview').innerHTML = exportHTML(state);
}

function exportHTML(state) {
  // HTML export: font size = word volume deviation, color = pitch deviation, bold/italic = region volume deviation
  let html = `<div style=\"line-height:2\">`;
  const perf = state.performance;
  // Compute global pitch and volume baselines
  let allPitches = [], allVolumes = [];
  for (let i=0; i<state.tokens.length; ++i) {
    const p = perf.wordData[i]?.pitch || [];
    const v = perf.wordData[i]?.volume || [];
    if (p.length) allPitches.push(p.reduce((a,b)=>a+b,0)/p.length);
    if (v.length) allVolumes.push(v.reduce((a,b)=>a+b,0)/v.length);
  }
  const pitchBaseline = allPitches.length ? allPitches.reduce((a,b)=>a+b,0)/allPitches.length : 150;
  const pitchStd = allPitches.length ? Math.sqrt(allPitches.map(x => (x-pitchBaseline)**2).reduce((a,b)=>a+b,0)/allPitches.length) : 1;
  const volBaseline = allVolumes.length ? allVolumes.reduce((a,b)=>a+b,0)/allVolumes.length : 0.1;
  const volStd = allVolumes.length ? Math.sqrt(allVolumes.map(x => (x-volBaseline)**2).reduce((a,b)=>a+b,0)/allVolumes.length) : 1;
  // Compute region volume deviations
  let regionStyles = [];
  for (let r=0; r<perf.regions.length; ++r) {
    const reg = perf.regions[r];
    const start = reg.start;
    const end = reg.end !== null ? reg.end : state.tokens.length;
    let regVols = [];
    for (let i=start; i<end; ++i) {
      const v = perf.wordData[i]?.volume || [];
      if (v.length) regVols.push(v.reduce((a,b)=>a+b,0)/v.length);
    }
    const regAvg = regVols.length ? regVols.reduce((a,b)=>a+b,0)/regVols.length : volBaseline;
    const regDev = regAvg - volBaseline;
    // Style: bold if above baseline, italic if below, both if much above
    let style = '';
    if (regDev > volStd*0.5) style = 'font-weight:bold;';
    if (regDev < -volStd*0.5) style = 'font-style:italic;';
    if (regDev > volStd*1.2) style = 'font-weight:bold;font-style:italic;';
    regionStyles.push({start,end,style});
  }
  // Render words
  for (let i=0; i<state.tokens.length; ++i) {
    const v = perf.wordData[i]?.volume || [];
    const p = perf.wordData[i]?.pitch || [];
    const avgV = v.length ? v.reduce((a,b)=>a+b,0)/v.length : volBaseline;
    const avgP = p.length ? p.reduce((a,b)=>a+b,0)/p.length : pitchBaseline;
    // Font size: deviation from baseline
    let zV = volStd > 0 ? (avgV - volBaseline) / volStd : 0;
    zV = Math.max(-2, Math.min(2, zV));
    const size = 1 + zV*0.7; // moderate scaling
    // Pitch color
    let color = '#333';
    if (avgP > 0 && pitchStd > 0) {
      let z = (avgP - pitchBaseline) / pitchStd;
      z = Math.max(-2, Math.min(2, z));
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
    // Region style
    let regStyle = '';
    for (let r=0; r<regionStyles.length; ++r) {
      if (i >= regionStyles[r].start && i < regionStyles[r].end) {
        regStyle = regionStyles[r].style;
        break;
      }
    }
    html += `<span style=\"font-size:${size}em;color:${color};${regStyle}\">${state.tokens[i]}</span> `;
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
