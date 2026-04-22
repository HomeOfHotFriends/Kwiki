// Minimal karaoke-style performance screen with volume tracking
export function showPerformance(state, onNext) {
  let div = document.getElementById('performance');
  if (!div) {
    div = document.createElement('div');
    div.id = 'performance';
    div.className = 'screen';
    div.innerHTML = `
      <h2>3. Performance</h2>
      <div id="karaoke"></div>
      <button id="start-btn">Start Recording</button>
      <button id="region-btn" disabled>New Font Region</button>
      <button id="stop-btn" disabled>Stop & Export</button>
      <div id="perf-status"></div>
    `;
    document.getElementById('app').appendChild(div);
  }
  const karaoke = div.querySelector('#karaoke');
  function renderKaraoke(current) {
    karaoke.innerHTML = state.tokens.map((w, i) => `<span class="word${i===current?' current':''}" data-idx="${i}">${w}</span>`).join(' ');
    karaoke.querySelectorAll('.word').forEach(span => {
      span.onclick = () => {
        if (state.performance && state.performance.active) {
          state.performance.current = parseInt(span.dataset.idx);
          renderKaraoke(state.performance.current);
        }
      };
    });
  }
  let perf = {
    active: false,
    current: 0,
    wordData: [],
    regions: [{start:0, end:null}],
    audioChunks: [],
    startTime: null
  };
  state.performance = perf;
  renderKaraoke(0);
  let mediaRecorder, audioContext, analyser, dataArray, rafId;
  div.querySelector('#start-btn').onclick = async () => {
    perf.active = true;
    perf.startTime = performance.now();
    perf.wordData = state.tokens.map(() => ({volume:[], time:0}));
    renderKaraoke(0);
    div.querySelector('#start-btn').disabled = true;
    div.querySelector('#region-btn').disabled = false;
    div.querySelector('#stop-btn').disabled = false;
    // Audio setup
    const stream = await navigator.mediaDevices.getUserMedia({audio:true});
    audioContext = new (window.AudioContext || window.webkitAudioContext)();
    const source = audioContext.createMediaStreamSource(stream);
    analyser = audioContext.createAnalyser();
    analyser.fftSize = 2048;
    dataArray = new Uint8Array(analyser.fftSize);
    source.connect(analyser);
    // Recording
    mediaRecorder = new MediaRecorder(stream);
    mediaRecorder.ondataavailable = e => perf.audioChunks.push(e.data);
    mediaRecorder.start();
    // Volume tracking loop
    function track() {
      if (!perf.active) return;
      analyser.getByteTimeDomainData(dataArray);
      // Simple RMS amplitude
      let sum = 0;
      for (let i=0; i<dataArray.length; ++i) {
        let v = (dataArray[i]-128)/128;
        sum += v*v;
      }
      let rms = Math.sqrt(sum/dataArray.length);
      perf.wordData[perf.current].volume.push(rms);
      perf.wordData[perf.current].time = performance.now() - perf.startTime;
      rafId = requestAnimationFrame(track);
    }
    track();
  };
  div.querySelector('#region-btn').onclick = () => {
    const last = perf.regions[perf.regions.length-1];
    last.end = perf.current;
    perf.regions.push({start:perf.current, end:null});
  };
  div.querySelector('#stop-btn').onclick = () => {
    perf.active = false;
    if (rafId) cancelAnimationFrame(rafId);
    if (mediaRecorder && mediaRecorder.state !== 'inactive') mediaRecorder.stop();
    if (audioContext) audioContext.close();
    div.querySelector('#start-btn').disabled = false;
    div.querySelector('#region-btn').disabled = true;
    div.querySelector('#stop-btn').disabled = true;
    onNext();
  };
}
