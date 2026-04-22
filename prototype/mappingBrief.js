export function showMappingBrief(state, onNext) {
  let div = document.getElementById('mapping-brief');
  if (!div) {
    div = document.createElement('div');
    div.id = 'mapping-brief';
    div.className = 'screen';
    div.innerHTML = `
      <h2>1. Mapping Brief</h2>
      <form id="mapping-form">
        <label>Font for Low Sibilance:<br><input name="fontLow" value="serif"></label><br>
        <label>Font for Medium Sibilance:<br><input name="fontMed" value="sans-serif"></label><br>
        <label>Font for High Sibilance:<br><input name="fontHigh" value="monospace"></label><br>
        <button type="submit">Next: Script Input</button>
      </form>
    `;
    document.getElementById('app').appendChild(div);
  }
  div.querySelector('form').onsubmit = e => {
    e.preventDefault();
    const f = Object.fromEntries(new FormData(e.target));
    state.mapping = {
      fonts: [f.fontLow, f.fontMed, f.fontHigh]
    };
    onNext();
  };
}
