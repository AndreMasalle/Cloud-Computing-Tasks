import { useEffect, useState } from 'react';
import api from '../api';

const CAT_COLORS = ["#2a78d6", "#eb6834", "#1baf7a", "#eda100"];
const OTHER_COLOR = "#98A6A2";
const TIERS = ["Bronze", "Silver", "Gold", "Platinum"];
const TIER_COLORS = { Bronze: "#A8643A", Silver: "#6F7F86", Gold: "#B7791F", Platinum: "#2D4E52" };
const CUST_COLOR = "#7b61c9";

const money = n => "$" + Number(n || 0).toLocaleString("en-US", { minimumFractionDigits: 2, maximumFractionDigits: 2 });
const niceStep = x => { const p = Math.pow(10, Math.floor(Math.log10(x))), f = x / p; return (f <= 1 ? 1 : f <= 2 ? 2 : f <= 5 ? 5 : 10) * p; };
const yTicks = (max, n = 4) => { if (!(max > 0)) return [0, 1]; const st = niceStep(max / n), out = []; for (let v = 0; ; v += st) { out.push(+v.toFixed(6)); if (v >= max) break; } return out; };
const axisMoney = v => "$" + (Math.abs(v) >= 1000 ? +(v / 1000).toFixed(1) + "k" : +v.toFixed(2));
const trunc = (s, n) => (String(s).length > n ? String(s).slice(0, n - 1) + "…" : String(s));
const rrRight = (x, y, w, h, r) => (r = Math.min(r, w, h / 2), `M${x} ${y}h${w - r}a${r} ${r} 0 0 1 ${r} ${r}v${h - 2 * r}a${r} ${r} 0 0 1 ${-r} ${r}h${-(w - r)}z`);
const rrTop = (x, y, w, h, r) => (r = Math.min(r, h, w / 2), `M${x} ${y + h}v${-(h - r)}a${r} ${r} 0 0 1 ${r} ${-r}h${w - 2 * r}a${r} ${r} 0 0 1 ${r} ${r}v${h - r}z`);

export default function Analytics() {
  const [data, setData] = useState({ products: [], customers: [], orders: [], tc: [], tp: [] });
  const [loading, setLoading] = useState(true);
  const [tooltip, setTooltip] = useState({ show: false, text: "", x: 0, y: 0 });

  useEffect(() => {
    const fetchData = async () => {
      try {
        const [p, c, o, tc, tp] = await Promise.all([
          api.get('/products'), api.get('/customers'), api.get('/orders'),
          api.get('/analytics/top-customers'), api.get('/analytics/top-products')
        ]);
        setData({ products: p.data, customers: c.data, orders: o.data, tc: tc.data, tp: tp.data });
        setLoading(false);
      } catch (err) { console.error(err); }
    };
    fetchData();
  }, []);

  const handleMouseMove = (e, text) => setTooltip({ show: true, text, x: e.clientX + 14, y: e.clientY + 14 });
  const handleMouseLeave = () => setTooltip({ ...tooltip, show: false });

  if (loading) return <div className="skel"></div>;
  if (!data.orders.length) return (
    <div className="head"><div><h1>Analitik</h1><p>Grafik penjualan dari data pesanan, produk, dan pelanggan.</p></div></div>
    && <div className="panel empty"><h3>Belum ada pesanan untuk dianalisis</h3><p>Grafik muncul setelah pesanan pertama dibuat.</p></div>
  );

  // Persiapan Data
  const total = data.orders.reduce((s, o) => s + o.total_price, 0);
  const pm = Object.fromEntries(data.products.map(p => [p.id, p]));
  const cm = Object.fromEntries(data.customers.map(c => [c.id, c]));

  const byCat = {}, byTier = Object.fromEntries(TIERS.map(t => [t, 0]));
  data.orders.forEach(o => {
    const cat = pm[o.product_id]?.category || "Produk terhapus";
    byCat[cat] = (byCat[cat] || 0) + o.total_price;
    const t = cm[o.customer_id]?.tier; if (t in byTier) byTier[t] += o.total_price;
  });

  let cats = Object.entries(byCat).sort((a, b) => b[1] - a[1]);
  const keep = cats.slice(0, 4), rest = cats.slice(4).reduce((s, c) => s + c[1], 0);
  const catItems = keep.map(([label, value], i) => ({ label, value, color: CAT_COLORS[i] }));
  if (rest > 0) catItems.push({ label: "Lainnya", value: rest, color: OTHER_COLOR });
  const colorOf = cat => catItems.find(c => c.label === cat)?.color || OTHER_COLOR;

  const cs = data.tc.slice(0, 5).map(c => ({ label: c.customer_name, value: c.total_spent, color: CUST_COLOR }));
  const ps = data.tp.slice(0, 5).map(p => { const cat = pm[p.product_id]?.category; return { label: p.product_name, value: p.total_revenue, color: colorOf(cat) }; });
  const tierItems = TIERS.map(t => ({ label: t, value: byTier[t], color: TIER_COLORS[t] }));

  const agg = {}; data.orders.forEach(o => { const a = agg[o.product_id] ||= { rev: 0, sold: 0 }; a.rev += o.total_price; a.sold += o.quantity; });
  const bub = data.products.map(p => ({ name: p.name, cat: p.category, price: p.price, sold: agg[p.id]?.sold || 0, rev: agg[p.id]?.rev || 0 }));

  // --- SVG RENDERERS ---
  const LineChart = ({ W = 600 }) => {
    const o = [...data.orders].sort((a, b) => a.order_date.localeCompare(b.order_date));
    let cum = 0; const pts = o.map((x, i) => ({ i, v: (cum += x.total_price), o: x }));
    const H = 260, L = 50, R = 14, T = 14, B = 34, iw = W - L - R, ih = H - T - B;
    const ticks = yTicks(cum), ymax = ticks[ticks.length - 1];
    const X = i => (pts.length === 1 ? L + iw / 2 : L + (i / (pts.length - 1)) * iw);
    const Y = v => +(T + ih - (v / ymax) * ih).toFixed(1);
    const line = pts.map((p, k) => (k ? "L" : "M") + X(p.i).toFixed(1) + " " + Y(p.v)).join(" ");
    const last = pts[pts.length - 1];

    return (
      <svg className="chart" viewBox={`0 0 ${W} ${H}`}>
        <g className="grid">{ticks.map(t => <g key={t}><line x1={L} x2={W - R} y1={Y(t)} y2={Y(t)}/><text x={L - 8} y={Y(t) + 4} textAnchor="end">{axisMoney(t)}</text></g>)}</g>
        <path d={`${line} L${X(last.i)} ${T + ih} L${X(0)} ${T + ih}Z`} fill="rgba(13,92,85,.10)"/>
        <path d={line} fill="none" stroke="var(--teal)" strokeWidth="2" strokeLinejoin="round" strokeLinecap="round"/>
        <circle cx={X(last.i)} cy={Y(last.v)} r="4" fill="var(--teal)" stroke="#fff" strokeWidth="2"/>
      </svg>
    );
  };

  const HBar = ({ items, W = 300 }) => {
    const rowH = 46, T = 2, B = 24, H = T + items.length * rowH + B;
    const ticks = yTicks(Math.max(...items.map(i => i.value), 0)), xm = ticks[ticks.length - 1];
    const X = v => +((v / xm) * W).toFixed(1), maxCh = Math.floor((W - 80) / 7.5);
    return (
      <svg className="chart" viewBox={`0 0 ${W} ${H}`}>
        <g className="grid">{ticks.map(t => <g key={t}><line x1={X(t)} x2={X(t)} y1={T} y2={H - B}/><text x={X(t)} y={H - 8} textAnchor={t === 0 ? "start" : t === xm ? "end" : "middle"}>{axisMoney(t)}</text></g>)}</g>
        {items.map((it, i) => { const y = T + i * rowH;
          return (
            <g key={i} className="bar">
              <text x="0" y={y + 14} className="cat">{trunc(it.label, maxCh)}</text>
              <text className="val" x={W} y={y + 14} textAnchor="end">{money(it.value)}</text>
              <path className="fill" style={{ fill: it.color || 'var(--teal)' }} d={rrRight(0, y + 22, Math.max(X(it.value), 2), 12, 4)}/>
            </g>
          );
        })}
      </svg>
    );
  };

  const VBar = ({ items, W = 300 }) => {
    const H = 250, L = 50, R = 8, T = 24, B = 34, iw = W - L - R, ih = H - T - B;
    const ticks = yTicks(Math.max(...items.map(i => i.value), 0)), ym = ticks[ticks.length - 1];
    const Y = v => +(T + ih - (v / ym) * ih).toFixed(1);
    const slot = iw / items.length, bw = Math.min(64, slot * 0.55);
    return (
      <svg className="chart" viewBox={`0 0 ${W} ${H}`}>
        <g className="grid">{ticks.map(t => <g key={t}><line x1={L} x2={W - R} y1={Y(t)} y2={Y(t)}/><text x={L - 8} y={Y(t) + 4} textAnchor="end">{axisMoney(t)}</text></g>)}</g>
        {items.map((it, i) => { const cx = L + slot * i + slot / 2, h = ih - (Y(it.value) - T);
          return (
            <g key={i} className="bar">
              {h > 0 && <path className="fill" style={{ fill: it.color || 'var(--teal)' }} d={rrTop(cx - bw / 2, Y(it.value), bw, h, 4)}/>}
              <text className="val" x={cx} y={Y(it.value) - 7} textAnchor="middle">{money(it.value)}</text>
              <text x={cx} y={H - 10} textAnchor="middle" className="cat">{it.label}</text>
            </g>
          );
        })}
      </svg>
    );
  };

  const Donut = ({ items }) => {
    const total = items.reduce((s, i) => s + i.value, 0), R = 62, C = 2 * Math.PI * R;
    let acc = 0;
    return (
      <div className="donut">
        <svg viewBox="0 0 180 180">
          {items.map((it, i) => {
            const len = (it.value / total) * C, gap = items.length > 1 ? 2 : 0;
            const el = <circle key={i} className="seg" cx="90" cy="90" r={R} fill="none" stroke={it.color} strokeWidth="26" strokeDasharray={`${Math.max(len - gap, 0.1)} ${C}`} strokeDashoffset={-(acc + gap / 2)} transform="rotate(-90 90 90)" />;
            acc += len; return el;
          })}
          <text x="90" y="88" textAnchor="middle" className="dv">{money(total)}</text>
          <text x="90" y="106" textAnchor="middle" className="dl">total</text>
        </svg>
        <ul className="legend">
          {items.map((it, i) => <li key={i}><i style={{ background: it.color }}></i><span>{it.label}</span><b>{money(it.value)}</b><em>{Math.round((it.value / total) * 100)}%</em></li>)}
        </ul>
      </div>
    );
  };

  const BubbleChart = ({ items, W = 600 }) => {
    const H = 380, L = 56, R = 16, T = 16, B = 46, iw = W - L - R, ih = H - T - B, padX = 52, padY = 52;
    const xt = yTicks(Math.max(...items.map(i => i.price), 1)), yt = yTicks(Math.max(...items.map(i => i.sold), 1));
    const xm = xt[xt.length - 1], ym = yt[yt.length - 1], maxRev = Math.max(...items.map(i => i.rev), 1);
    const X = v => +(L + padX + (v / xm) * (iw - 2 * padX)).toFixed(1), Y = v => +(T + ih - padY - (v / ym) * (ih - 2 * padY)).toFixed(1);
    const rad = i => (i.rev > 0 ? 26 + 22 * Math.sqrt(i.rev / maxRev) : 5);
    return (
      <svg className="chart" viewBox={`0 0 ${W} ${H}`}>
        <g className="grid">
          {yt.map(t => <g key={t}><line x1={L} x2={W - R} y1={Y(t)} y2={Y(t)}/><text x={L - 8} y={Y(t) + 4} textAnchor="end">{t}</text></g>)}
          {xt.map(t => <g key={t}><line className="v" x1={X(t)} x2={X(t)} y1={T} y2={T + ih}/><text x={X(t)} y={T + ih + 16} textAnchor="middle">{axisMoney(t)}</text></g>)}
        </g>
        <text x={L + iw / 2} y={H - 6} textAnchor="middle">Harga satuan</text>
        <text transform={`translate(12 ${T + ih / 2}) rotate(-90)`} textAnchor="middle">Item terjual</text>
        {[...items].sort((a, b) => b.rev - a.rev).map((it, idx) => {
          const x = X(it.price), y = Y(it.sold), r = rad(it);
          const words = String(it.name).trim().split(/\s+/).slice(0, 2).map(w => trunc(w, 11));
          const fs = Math.max(9, Math.min(13, Math.round(r * 0.3)));
          return (
            <g key={idx} className="bub">
              <circle className="b" cx={x} cy={y} r={r} fill={colorOf(it.cat)} fillOpacity={it.rev > 0 ? .85 : .35} stroke="#fff" strokeWidth="2"/>
              {it.rev > 0 && (
                <text className="bl" textAnchor="middle" style={{ fontSize: `${fs}px` }}>
                  {words.map((w, k) => <tspan key={k} x={x} y={(y + (k - (words.length - 1) / 2) * (fs + 2) + fs * 0.35).toFixed(1)}>{w}</tspan>)}
                </text>
              )}
            </g>
          );
        })}
      </svg>
    );
  };

  return (
    <>
      <div className="head"><div><h1>Analitik</h1><p>Grafik penjualan dari data pesanan, produk, dan pelanggan.</p></div></div>
      <div className="charts">
        <div className="panel">
          <h2>Tren pendapatan</h2>
          <p className="sub">Pendapatan kumulatif, pesanan demi pesanan.</p>
          <LineChart />
        </div>

        {data.products.length > 0 && (
          <div className="panel">
            <h2>Harga vs penjualan produk</h2>
            <p className="sub">Ukuran gelembung menunjukkan pendapatan, warna menunjukkan kategori. Titik kecil di dasar berarti produk belum terjual.</p>
            <BubbleChart items={bub} />
          </div>
        )}

        <div className="cols2">
          <div className="panel"><h2>5 pelanggan teratas</h2><p className="sub">Berdasarkan total belanja.</p><HBar items={cs} /></div>
          <div className="panel"><h2>5 produk terlaris</h2><p className="sub">Berdasarkan pendapatan, warna mengikuti kategori.</p><HBar items={ps} /></div>
        </div>

        <div className="cols2">
          <div className="panel"><h2>Pendapatan per kategori</h2><p className="sub">Gabungan data pesanan dan produk.</p><Donut items={catItems} /></div>
          <div className="panel"><h2>Pendapatan per membership</h2><p className="sub">Gabungan data pesanan dan pelanggan.</p><VBar items={tierItems} /></div>
        </div>
      </div>
    </>
  );
}