/* Shared helpers for the homepage data strip and the /data/ page.
   Data comes from /data/euro.json and /data/usd.json, cached at build time. */
(function(){
  const T={
    zh:{dfr:'欧央行存款利率',fed:'联邦基金区间',hicp:'欧元区 HICP',cpi:'美国 CPI',nfp:'美国非农新增',bund:'德国 10 年期',ust:'美国 10 年期',eur:'欧元兑美元',dxy:'广义美元指数',un:'美国失业率',
      c_rates:'政策利率（%）',c_infl:'通胀，同比（%）',c_core:'核心通胀，同比（%）',c_y:'10 年期国债收益率（%）',c_fx:'欧元兑美元',c_dxy:'广义美元指数',c_un:'美国失业率（%）',c_curve:'美债 10 年减 2 年（百分点）',
      ecb:'欧央行',fedl:'美联储',ea:'欧元区',us:'美国',de:'德国',fr:'法国',it:'意大利',es:'西班牙',
      asof:'数据截至',src:'来源：ECB、FRED，每 6 小时更新',fail:'数据暂时取不到。',k:' 千',next:'下次议息',days:'天后'},
    en:{dfr:'ECB deposit rate',fed:'Fed funds range',hicp:'Euro area HICP',cpi:'US CPI',nfp:'US payrolls',bund:'German 10y',ust:'US 10y',eur:'EUR/USD',dxy:'Broad dollar index',un:'US unemployment',
      c_rates:'Policy rates (%)',c_infl:'Inflation, y/y (%)',c_core:'Core inflation, y/y (%)',c_y:'10-year bond yields (%)',c_fx:'EUR/USD',c_dxy:'Broad dollar index',c_un:'US unemployment rate (%)',c_curve:'US 10y minus 2y (pp)',
      ecb:'ECB',fedl:'Fed',ea:'Euro area',us:'US',de:'Germany',fr:'France',it:'Italy',es:'Spain',
      asof:'Data as of',src:'Sources: ECB, FRED; refreshed every 6 hours',fail:'Data unavailable right now.',k:'k',next:'Next meeting',days:' days'}};
  const C={eu:'#22d3ee',us:'#f59e0b',a:'#22d3ee',b:'#a78bfa',c:'#f472b6',d:'#34d399',e:'#f59e0b'};
  const card='border:1px solid rgba(161,161,170,.25);border-radius:.6rem;padding:.55rem .7rem;background:rgba(161,161,170,.07)';
  const last=s=>s&&s.length?s[s.length-1]:null;
  const kpi=(l,v,d)=>`<div style="${card}"><div style="font-size:.72rem;opacity:.75">${l}</div><div style="font-size:1.2rem;font-weight:700;line-height:1.3;white-space:nowrap">${v}</div><div style="font-size:.68rem;opacity:.6">${d||''}</div></div>`;
  function chart(title,sets,opt){
    opt=opt||{};sets=sets.filter(s=>s.data&&s.data.length>1);if(!sets.length)return '';
    const W=320,H=opt.h||110,P=4;const all=sets.flatMap(s=>s.data.map(p=>p[1]));
    const lo=Math.min(...all),hi=Math.max(...all),n=Math.max(...sets.map(s=>s.data.length));
    const path=s=>s.data.map((p,i)=>`${i?'L':'M'}${(P+(W-2*P)*(i+n-s.data.length)/(n-1)).toFixed(1)},${(H-P-(H-2*P)*(p[1]-lo)/((hi-lo)||1)).toFixed(1)}`).join('');
    const dec=opt.dec==null?2:opt.dec;
    const leg=sets.map(s=>{const l=last(s.data);return `<span style="color:${s.c};white-space:nowrap">● ${s.l} ${l?l[1].toFixed(dec):''}</span>`}).join(' &nbsp;');
    const first=sets[0].data[0][0],end=last(sets[0].data)[0];
    const zero=(lo<0&&hi>0)?`<line x1="0" x2="${W}" y1="${(H-P-(H-2*P)*(0-lo)/(hi-lo)).toFixed(1)}" y2="${(H-P-(H-2*P)*(0-lo)/(hi-lo)).toFixed(1)}" stroke="rgba(161,161,170,.4)" stroke-dasharray="3 3" vector-effect="non-scaling-stroke"/>`:'';
    return `<div style="${card}"><div style="font-size:.8rem;font-weight:600">${title}</div><div style="font-size:.72rem;margin:.15rem 0">${leg}</div>
      <div style="display:flex;justify-content:space-between;font-size:.62rem;opacity:.55"><span>${hi.toFixed(dec)}</span></div>
      <svg viewBox="0 0 ${W} ${H}" style="width:100%;height:auto;display:block" preserveAspectRatio="none">${zero}${sets.map(s=>`<path d="${path(s)}" fill="none" stroke="${s.c}" stroke-width="2" vector-effect="non-scaling-stroke"/>`).join('')}</svg>
      <div style="display:flex;justify-content:space-between;font-size:.62rem;opacity:.55"><span>${lo.toFixed(dec)}</span><span></span></div>
      <div style="display:flex;justify-content:space-between;font-size:.65rem;opacity:.6"><span>${first}</span><span>${end}</span></div></div>`;
  }
  function asof(d){
    if(!d||!d.updated)return '';
    const m=d.updated.match(/(\d{4})-(\d\d)-(\d\d) (\d\d):(\d\d)/);if(!m)return d.updated;
    const t=new Date(Date.UTC(+m[1],m[2]-1,+m[3],+m[4],+m[5]));
    return t.toLocaleString(document.documentElement.lang&&document.documentElement.lang.startsWith('zh')?'zh-CN':'en-GB',{timeZone:'Asia/Shanghai',year:'numeric',month:'2-digit',day:'2-digit',hour:'2-digit',minute:'2-digit'})+(m?' (UTC+8)':'');
  }
  function kpis(E,U,L){
    let k='';const f=(s,n,u='%')=>{const p=last(s);return p?[p[1].toFixed(n)+u,p[0]]:null};
    const add=(l,r)=>{if(r)k+=kpi(l,r[0],r[1])};
    if(E)add(L.dfr,f(E.dfr,2));
    if(U){const h=last(U.fed_hi),o=last(U.fed_lo);if(h&&o)k+=kpi(L.fed,o[1].toFixed(2)+'–'+h[1].toFixed(2)+'%',h[0])}
    if(E)add(L.hicp,f(E.hicp,1));
    if(U){add(L.cpi,f(U.cpi,1));const nf=last(U.nfp);if(nf)k+=kpi(L.nfp,(nf[1]>0?'+':'')+Math.round(nf[1])+L.k,nf[0])}
    if(E)add(L.bund,f(E.y_de,2));
    if(U)add(L.ust,f(U.t10_d,2));
    if(E)add(L.eur,f(E.eurusd_d,4,''));
    return k;
  }
  function load(base){
    const get=u=>fetch(u,{cache:'no-cache'}).then(r=>{if(!r.ok)throw r.status;return r.json()});
    return Promise.allSettled([get(base+'data/euro.json'),get(base+'data/usd.json')]).then(([e,u])=>[
      e.status==='fulfilled'?e.value:null,u.status==='fulfilled'?u.value:null]);
  }
  window.DataKit={T,C,card,last,kpi,chart,asof,kpis,load};
})();
