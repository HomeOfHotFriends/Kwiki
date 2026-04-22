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
  let mediaRecorder, audioContext, analyser, dataArray, rafId, pitchBuffer = [];
  div.querySelector('#start-btn').onclick = async () => {
    perf.active = true;
    perf.startTime = performance.now();
    perf.wordData = state.tokens.map(() => ({volume:[], pitch:[], time:0}));
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
    // Volume and pitch tracking loop
    function autoCorrelate(buf, sampleRate) {
      // Basic autocorrelation pitch detection
      let SIZE = buf.length;
      let rms = 0;
      for (let i = 0; i < SIZE; i++) {
        let val = buf[i] / 128 - 1;
        rms += val * val;
      }
      rms = Math.sqrt(rms / SIZE);
      if (rms < 0.01) return 0; // too quiet
      let r1 = 0, r2 = SIZE - 1, thres = 0.2;
      for (let i = 0; i < SIZE / 2; i++) {
        if (Math.abs(buf[i] / 128 - 1) < thres) { r1 = i; break; }
      }
      for (let i = 1; i < SIZE / 2; i++) {
        if (Math.abs(buf[SIZE - i] / 128 - 1) < thres) { r2 = SIZE - i; break; }
      }
      buf = buf.slice(r1, r2);
      SIZE = buf.length;
      let c = new Array(SIZE).fill(0);
      for (let i = 0; i < SIZE; i++) {
        for (let j = 0; j < SIZE - i; j++) {
          c[i] = c[i] + ((buf[j] / 128 - 1) * (buf[j + i] / 128 - 1));
        }
      }
      let d = 0; while (c[d] > c[d + 1]) d++;
      let maxval = -1, maxpos = -1;
      for (let i = d; i < SIZE; i++) {
        if (c[i] > maxval) { maxval = c[i]; maxpos = i; }
      }
      let T0 = maxpos;
      if (T0 === -1) return 0;
      return sampleRate / T0;
    }
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
      // Pitch detection
      let pitch = autoCorrelate(dataArray, audioContext.sampleRate);
      if (pitch > 50 && pitch < 1000) {
        perf.wordData[perf.current].pitch.push(pitch);
      }
      perf.wordData[perf.current].time = performance.now() - perf.startTime;
      // Show pitch/volume for current word
      const status = div.querySelector('#perf-status');
      if (status) {
        const v = perf.wordData[perf.current].volume;
        const p = perf.wordData[perf.current].pitch;
        const avgV = v.length ? (v.reduce((a,b)=>a+b,0)/v.length).toFixed(2) : '0';
        const avgP = p.length ? (p.reduce((a,b)=>a+b,0)/p.length).toFixed(0) : '0';
        status.innerHTML = `Current word: <b>${state.tokens[perf.current]}</b> | Volume: ${avgV} | Pitch: ${avgP} Hz`;
      }
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
