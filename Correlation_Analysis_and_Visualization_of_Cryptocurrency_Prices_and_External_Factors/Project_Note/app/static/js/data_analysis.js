document.addEventListener('DOMContentLoaded', function () {
    // 버튼 & 컨테이너 참조
    const btnStructure   = document.getElementById('btnStructure');
    const btnViz         = document.getElementById('btnViz');
    const toggleSection  = document.getElementById('toggleSection');
    const btnPreprocViz  = document.getElementById('btnPreprocViz');
    const preprocSection = document.getElementById('preprocVizSection');
  
    // 차트 인스턴스 보관
    let currentMode             = "";
    let chartCountsInstance     = null;
    let chartMissingInstance    = null;
    let preprocChartRawInstance = null;
    let preprocChartNormInstance= null;
  
    // ----------------------------------------------------------------
    // (A) 데이터셋 구조 보기
    // ----------------------------------------------------------------
    function loadStructureSection() {
      const html = `
        <p class="font-semibold mb-2">데이터셋 선택:</p>
        <div class="dataset-selector grid grid-cols-2 gap-2">
          <label><input type="radio" name="dataset"
                        value="비트코인_23.01.01~25.01.31.csv" checked> 비트코인</label>
          <label><input type="radio" name="dataset"
                        value="이더리움_23.01.01~25.01.31.csv"> 이더리움</label>
          <label><input type="radio" name="dataset"
                        value="도지코인_23.01.01~25.01.31.csv"> 도지코인</label>
          <label><input type="radio" name="dataset"
                        value="코스피_23.01.01~25.01.31.csv"> 코스피</label>
          <label><input type="radio" name="dataset"
                        value="나스닥_23.01.01~25.01.31.csv"> 나스닥</label>
          <label><input type="radio" name="dataset"
                        value="한국금리_23.01.01~25.01.31.csv"> 한국금리</label>
          <label><input type="radio" name="dataset"
                        value="미국금리_23.01.01~25.01.31.csv"> 미국금리</label>
          <label><input type="radio" name="dataset"
                        value="월령_23.01.01~25.01.31.csv"> 월령</label>
          <label><input type="radio" name="dataset"
                        value="날씨_23.01.01~25.01.31.csv"> 날씨</label>
        </div>
        <div id="datasetResult" class="mt-4"></div>
      `;
      toggleSection.innerHTML = html;
  
      function updateStructure() {
        const sel = document.querySelector('input[name="dataset"]:checked');
        if (!sel) return;
        fetch(`/dataset_structure?dataset=${encodeURIComponent(sel.value)}`)
          .then(r => r.json())
          .then(data => {
            if (data.error) { alert(data.error); return; }
      
            // ✅ 각 테이블에 스타일 클래스 삽입
            const styleFix = `
            <style>
              table, th, td {
                border: 1px solid #4B5563; /* Tailwind gray-600 */
                border-collapse: collapse;
              }
              th {
                text-align: center;
                background-color: #1F2937; /* Tailwind gray-800 */
              }
              td, th {
                padding: 6px 10px;
              }
            </style>
            `;
            const styledHead     = styleFix + data.head.replace('<table', '<table class="table-auto w-full text-sm text-white bg-gray-800"');
            const styledDtypes   = styleFix + data.dtypes.replace('<table', '<table class="table-auto w-full text-sm text-white bg-gray-800"');
            const styledIsna     = styleFix + data.isna.replace('<table', '<table class="table-auto w-full text-sm text-white bg-gray-800"');
            const styledNunique  = styleFix + data.nunique.replace('<table', '<table class="table-auto w-full text-sm text-white bg-gray-800"');
            const styledDescribe = styleFix + data.describe.replace('<table', '<table class="table-auto w-full text-sm text-white bg-gray-800"');
                       
      
            document.getElementById('datasetResult').innerHTML = `
              <div class="table-card p-2 bg-gray-700 rounded-lg shadow mb-2">
                <h3 class="font-semibold mb-1">구조</h3>
                <div class="overflow-auto">${styledHead}</div>
              </div>
              <div class="table-card p-2 bg-gray-700 rounded-lg shadow mb-2">
                <h3 class="font-semibold mb-1">데이터타입</h3>
                <div class="overflow-auto">${styledDtypes}</div>
              </div>
              <div class="table-card p-2 bg-gray-700 rounded-lg shadow mb-2">
                <h3 class="font-semibold mb-1">결측치</h3>
                <div class="overflow-auto">${styledIsna}</div>
              </div>
              <div class="table-card p-2 bg-gray-700 rounded-lg shadow mb-2">
                <h3 class="font-semibold mb-1">유니크값</h3>
                <div class="overflow-auto">${styledNunique}</div>
              </div>
              <div class="table-card p-2 bg-gray-700 rounded-lg shadow mb-2">
                <h3 class="font-semibold mb-1">기초통계량</h3>
                <div class="overflow-auto">${styledDescribe}</div>
              </div>
            `;
          })
          .catch(err => {
            console.error(err);
            alert('데이터 로드 실패: ' + err);
          });
      }      
  
      document.querySelectorAll('input[name="dataset"]')
        .forEach(r => r.addEventListener('change', updateStructure));
      updateStructure();
    }
  
    // ----------------------------------------------------------------
    // (B) 데이터셋 시각화 (바 차트)
    // ----------------------------------------------------------------
    function loadVizSection() {
      const html = `
        <p class="font-semibold mb-2">데이터셋 선택:</p>
        <div class="grid grid-cols-2 gap-2 mb-4">
          <label><input type="radio" name="vizDataset" value="비트코인_23.01.01~25.01.31.csv" checked> 비트코인</label>
          <label><input type="radio" name="vizDataset" value="이더리움_23.01.01~25.01.31.csv"> 이더리움</label>
          <label><input type="radio" name="vizDataset" value="도지코인_23.01.01~25.01.31.csv"> 도지코인</label>
          <label><input type="radio" name="vizDataset" value="코스피_23.01.01~25.01.31.csv"> 코스피</label>
          <label><input type="radio" name="vizDataset" value="나스닥_23.01.01~25.01.31.csv"> 나스닥</label>
          <label><input type="radio" name="vizDataset" value="한국금리_23.01.01~25.01.31.csv"> 한국금리</label>
          <label><input type="radio" name="vizDataset" value="미국금리_23.01.01~25.01.31.csv"> 미국금리</label>
          <label><input type="radio" name="vizDataset" value="월령_23.01.01~25.01.31.csv"> 월령</label>
          <label><input type="radio" name="vizDataset" value="날씨_23.01.01~25.01.31.csv"> 날씨</label>
        </div>
        <div class="mb-4"><canvas id="chartCountsCanvas"></canvas></div>
        <div><canvas id="chartMissingCanvas"></canvas></div>
      `;
      toggleSection.innerHTML = html;
    
      function updateVizCharts() {
        const sel = document.querySelector('input[name="vizDataset"]:checked');
        if (!sel) return;
    
        fetch(`/dataset_viz?dataset=${encodeURIComponent(sel.value)}`)
          .then(r => r.json())
          .then(data => {
            if (data.error) { alert(data.error); return; }
    
            const cols    = data.columns  || [];
            const counts  = data.counts   || [];
            const missing = data.missing  || [];
    
            const ctx1 = document.getElementById('chartCountsCanvas').getContext('2d');
            if (chartCountsInstance) chartCountsInstance.destroy();
            chartCountsInstance = new Chart(ctx1, {
              type: 'bar',
              data: {
                labels: cols,
                datasets: [{
                  label: '갯수',
                  data: counts,
                  backgroundColor: 'rgba(54,162,235,0.6)',
                  borderColor: 'rgba(54,162,235,1)',
                  borderWidth: 1
                }]
              },
              options: {
                responsive: true,
                maintainAspectRatio: true,
                scales: { y: { beginAtZero: true } }
              }
            });
    
            const ctx2 = document.getElementById('chartMissingCanvas').getContext('2d');
            if (chartMissingInstance) chartMissingInstance.destroy();
            chartMissingInstance = new Chart(ctx2, {
              type: 'bar',
              data: {
                labels: cols,
                datasets: [{
                  label: '결측치',
                  data: missing,
                  backgroundColor: 'rgba(255,99,132,0.6)',
                  borderColor: 'rgba(255,99,132,1)',
                  borderWidth: 1
                }]
              },
              options: {
                responsive: true,
                maintainAspectRatio: true,
                scales: { y: { beginAtZero: true } }
              }
            });
          })
          .catch(err => {
            console.error(err);
            alert('시각화 로드 실패: ' + err);
          });
      }
    
      document.querySelectorAll('input[name="vizDataset"]')
        .forEach(r => r.addEventListener('change', updateVizCharts));
    
      updateVizCharts();
    }
    
  
    // ----------------------------------------------------------------
    // (C) 전처리 차트만 갱신 (HTML은 템플릿에 고정)
    // ----------------------------------------------------------------
    function getColorForColumn(col) {
      const map = {
        btc_price: 'rgba(255,99,132,1)',
        eth_price: 'rgba(54,162,235,1)',
        doge_price:'rgba(255,206,86,1)',
        kospi:     'rgba(75,192,192,1)',
        nasdaq:    'rgba(153,102,255,1)',
        kor_rate:  'rgba(255,159,64,1)',
        usa_rate:  'rgba(199,199,199,1)',
        moon_phase:'rgba(0,0,0,1)'
      };
      return map[col]||'rgba(100,100,100,1)';
    }
  
    function parseWeather(dates, w) {
      return dates.map((_,i)=>{
        if (w.clear && w.clear[i]===1) return 'clear';
        if (w.rain  && w.rain[i]===1)  return 'rain';
        if (w.cloudy&& w.cloudy[i]===1)return 'cloudy';
        if (w.partly_cloudy&&w.partly_cloudy[i]===1) return 'partly_cloudy';
        if (w.snow&& w.snow[i]===1) return 'snow';
        return null;
      });
    }
  
    function getPointStyle(cond) {
      const m = { clear:'circle', rain:'cross', cloudy:'rect',
                  partly_cloudy:'triangle', snow:'star' };
      return m[cond]||'circle';
    }
  
    function generateFinanceLegendHTML(ds) {
      let html = `<div class="flex flex-wrap gap-2">`;
      ds.forEach(o=>{
        html+=`<div class="flex items-center gap-1">
                 <div style="width:15px;height:15px;background:${o.borderColor}"></div>
                 <span>${o.label}</span>
               </div>`;
      });
      return html+`</div>`;
    }
  
    function generateWeatherLegendHTML() {
      const items = [
        {label:'clear(맑음)',shape:'○'},
        {label:'rain(비)',shape:'+'},
        {label:'cloudy(흐림)',shape:'■'},
        {label:'partly_cloudy(구름조금)',shape:'△'},
        {label:'snow(눈)',shape:'*'},
      ];
      let html = `<div class="flex flex-wrap gap-2">`;
      items.forEach(it=>{
        html+=`<div class="flex items-center gap-1">
                 <span class="text-lg font-bold text-gray-600">${it.shape}</span>
                 <span>${it.label}</span>
               </div>`;
      });
      return html+`</div>`;
    }
  
    function showFullLegend(fin,weather){
      const c = document.getElementById('weatherMarkerGuide');
      if(!c)return;
      c.innerHTML = `<div class="flex flex-col gap-2">${fin}${weather}</div>`;
    }
  
    function updatePreprocCharts(){
      if(preprocChartRawInstance) preprocChartRawInstance.destroy();
      if(preprocChartNormInstance)preprocChartNormInstance.destroy();
  
      const cols = Array.from(
        document.querySelectorAll('input[name="preprocColumns"]:checked')
      ).map(cb=>cb.value).join(',');
      const from = document.getElementById('preprocFromDate').value;
      const to   = document.getElementById('preprocToDate').value;
  
      // RAW
      fetch(`/preproc_viz?type=raw&cols=${encodeURIComponent(cols)}&from=${from}&to=${to}`)
        .then(r=>r.json()).then(data=>{
          if(data.error){alert(data.error);return;}
          const dates = data.dates||[];
          const wCond = parseWeather(dates,data.weather||{});
          const ds = Object.keys(data.data||{}).map(col=>({
            label:col,
            data:data.data[col],
            borderColor:getColorForColumn(col),
            borderWidth:2,fill:false,tension:0.1,pointRadius:6,
            pointStyle(ctx){return getPointStyle(wCond[ctx.dataIndex]);}
          }));
          const ctx = document.getElementById('preprocChartRaw').getContext('2d');
          preprocChartRawInstance = new Chart(ctx,{
            type:'line',
            data:{labels:dates,datasets:ds},
            options:{
              responsive:true,
              maintainAspectRatio:false,  // ★ true로 고정
              plugins:{legend:{display:false}},
              scales:{y:{beginAtZero:true}}
            }
          });
          showFullLegend(generateFinanceLegendHTML(ds),generateWeatherLegendHTML());
        })
        .catch(e=>{console.error(e);alert('원본 실패:'+e);});
        document.getElementById('preprocChartRaw').parentNode.style.height = '400px'
  
      // NORM
      fetch(`/preproc_viz?type=norm&cols=${encodeURIComponent(cols)}&from=${from}&to=${to}`)
        .then(r=>r.json()).then(data=>{
          if(data.error){alert(data.error);return;}
          const dates = data.dates||[];
          const wCond = parseWeather(dates,data.weather||{});
          const ds = Object.keys(data.data||{}).map(col=>({
            label:col,
            data:data.data[col],
            borderColor:getColorForColumn(col),
            borderWidth:2,fill:false,tension:0.1,pointRadius:6,
            pointStyle(ctx){return getPointStyle(wCond[ctx.dataIndex]);}
          }));
          const ctx = document.getElementById('preprocChartNorm').getContext('2d');
          preprocChartNormInstance = new Chart(ctx,{
            type:'line',
            data:{labels:dates,datasets:ds},
            options:{
              responsive:true,
              maintainAspectRatio:false,  // ★ true로 고정
              plugins:{legend:{display:false}},
              scales:{y:{beginAtZero:true}}
            }
          });
          showFullLegend(generateFinanceLegendHTML(ds),generateWeatherLegendHTML());
        })
        .catch(e=>{console.error(e);alert('정규화 실패:'+e);});
        document.getElementById('preprocChartNorm').parentNode.style.height = '400px';
    }
  
    // 체크박스 & 날짜 이벤트 (한 번만)
    document.querySelectorAll('input[name="preprocColumns"]')
      .forEach(cb=>cb.addEventListener('change',updatePreprocCharts));
    document.getElementById('preprocFromDate')
      .addEventListener('change',updatePreprocCharts);
    document.getElementById('preprocToDate')
      .addEventListener('change',updatePreprocCharts);
  
    // (D) 버튼 토글
    btnStructure.addEventListener('click',function(){
      if(currentMode!=='structure'){
        loadStructureSection();
        currentMode='structure';
        btnStructure.textContent='데이터셋 구조 보기 ▲';
        btnViz.textContent='데이터셋 시각화 ▼';
        preprocSection.style.display='none';
        btnPreprocViz.textContent='전처리 데이터 시각화 ▼';
        toggleSection.style.display='block';
      } else {
        toggleSection.style.display='none';
        btnStructure.textContent='데이터셋 구조 보기 ▼';
        currentMode='';
      }
    });
  
    btnViz.addEventListener('click',function(){
      if(currentMode!=='viz'){
        loadVizSection();
        currentMode='viz';
        btnViz.textContent='데이터셋 시각화 ▲';
        btnStructure.textContent='데이터셋 구조 보기 ▼';
        preprocSection.style.display='none';
        btnPreprocViz.textContent='전처리 데이터 시각화 ▼';
        toggleSection.style.display='block';
      } else {
        toggleSection.style.display='none';
        btnViz.textContent='데이터셋 시각화 ▼';
        currentMode='';
      }
    });
  
    btnPreprocViz.addEventListener('click',function(){
      if(currentMode!=='preproc'){
        preprocSection.style.display='block';
        btnPreprocViz.textContent='전처리 데이터 시각화 ▲';
        toggleSection.style.display='none';
        btnStructure.textContent='데이터셋 구조 보기 ▼';
        btnViz.textContent='데이터셋 시각화 ▼';
        updatePreprocCharts();
        currentMode='preproc';
      } else {
        preprocSection.style.display='none';
        btnPreprocViz.textContent='전처리 데이터 시각화 ▼';
        currentMode='';
      }
    });
  
  });  