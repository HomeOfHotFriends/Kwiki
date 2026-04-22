export function showScriptInput(state, onNext) {
  let div = document.getElementById('script-input');
  if (!div) {
    div = document.createElement('div');
    div.id = 'script-input';
    div.className = 'screen';
    div.innerHTML = `
      <h2>2. Script Input</h2>
      <textarea id="script-area" rows="6" style="width:100%"></textarea><br>
      <button id="tokenize-btn">Tokenize & Next</button>
    `;
    document.getElementById('app').appendChild(div);
  }
  div.querySelector('#tokenize-btn').onclick = () => {
    const text = div.querySelector('#script-area').value;
    state.script = text;
    state.tokens = text.match(/\S+/g) || [];
    onNext();
  };
}
