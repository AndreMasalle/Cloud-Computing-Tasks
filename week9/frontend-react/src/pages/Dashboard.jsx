import { useEffect, useState } from 'react';
import api from '../api';

export default function Dashboard() {
  const [data, setData] = useState(null);
  const [orders, setOrders] = useState([]);

  const fetchData = async () => {
    try {
      const [resDash, resOrders] = await Promise.all([api.get('/dashboard'), api.get('/orders')]);
      setData(resDash.data);
      setOrders(resOrders.data);
    } catch (err) {
      console.error(err);
    }
  };

  useEffect(() => { fetchData(); }, []);

  const seedData = async () => {
    try {
      // DATA DUMMY 100% SAMA DENGAN VERSI HTML ASLI
      const P = [
        ["Kopi Arabika Gayo 250g", "Minuman", 9.5, 40],
        ["Teko Keramik Handmade", "Perabot", 24, 12],
        ["Tumbler Stainless 500ml", "Perabot", 15.75, 4],
        ["Teh Melati Premium", "Minuman", 6.25, 60],
        ["Gilingan Kopi Manual", "Peralatan", 32, 3]
      ];
      const C = [
        ["Adrian Maulana", "bangmega@mail.id", "Silver"],
        ["Muhammad Rizki Anshari", "rizkivoker@mail.id", "Platinum"],
        ["Andre Fransiscus Masalle", "masxebec@mail.id", "Bronze"],
        ["Muhammad Dhafa Ramadhani", "presidenri@mail.id", "Gold"]
      ];
      const O = [
        [3, 3, 4], [2, 1, 1], [1, 4, 1], [3, 2, 2], [1, 0, 10], [3, 3, 6], [1, 1, 2], [0, 4, 1], [0, 0, 3]
      ];

      // 1. Masukkan Produk
      const ps = await Promise.all(P.map(p =>
        api.post('/products', { name: p[0], category: p[1], price: p[2], stock: p[3] })
      ));

      // 2. Masukkan Pelanggan
      const cs = await Promise.all(C.map(c =>
        api.post('/customers', { name: c[0], email: c[1], tier: c[2] })
      ));

      // 3. Masukkan Pesanan (dibalik agar urutan tanggal sesuai)
      for (const [cIdx, pIdx, qty] of [...O].reverse()) {
        await api.post('/orders', {
          customer_id: cs[cIdx].data.id,
          product_id: ps[pIdx].data.id,
          quantity: qty
        });
      }

      // 4. Refresh data
      fetchData();
    } catch (err) {
      alert("Gagal memasukkan data contoh. Pastikan backend menyala.");
    }
  };

  if (!data) return <div className="skel"></div>;

  // Render Sparkline Chart
  let spark = <div className="nospark">Grafik muncul setelah ada minimal 2 pesanan.</div>;
  if (orders.length >= 2) {
    const sorted = [...orders].sort((a, b) => a.order_date.localeCompare(b.order_date));
    let cum = 0; const pts = sorted.map(o => (cum += o.total_price));
    const W = 600, H = 110, max = pts[pts.length - 1] || 1;
    const xy = pts.map((v, i) => [i / (pts.length - 1) * W, H - 8 - (v / max) * (H - 24)]);
    const line = xy.map((p, i) => (i ? "L" : "M") + p[0].toFixed(1) + " " + p[1].toFixed(1)).join(" ");
    spark = (
      <svg className="spark" viewBox={`0 0 ${W} ${H}`} preserveAspectRatio="none">
        <path className="area" d={`${line} L${W} ${H} L0 ${H}Z`}/>
        <path className="line" d={line}/>
      </svg>
    );
  }

  const avg = data.total_orders ? data.total_revenue / data.total_orders : 0;

  return (
    <>
      <div className="head">
        <div><h1>Dashboard</h1><p>Ringkasan penjualan toko Anda.</p></div>
        <div className="tools"><button className="btn ghost" onClick={seedData}>Isi data contoh</button></div>
      </div>

      <section className="hero">
        <div className="lbl">Total pendapatan</div>
        <div className="big"><sup>$</sup>{data.total_revenue.toLocaleString('en-US', { minimumFractionDigits: 2 })}</div>
        <div className="sub">{data.total_orders ? `dari ${data.total_orders} pesanan, rata-rata $${avg.toFixed(2)} per pesanan` : "Belum ada pesanan masuk"}</div>
        {spark}
      </section>

      <div className="panel facts" style={{ marginTop: '20px' }}>
        <div className="fact"><b>{data.total_orders}</b><span>Pesanan</span></div>
        <div className="fact"><b>{data.total_customers}</b><span>Pelanggan</span></div>
        <div className="fact"><b>{data.total_products}</b><span>Produk</span></div>
        <div className="fact"><b>${avg.toFixed(2)}</b><span>Rata-rata per pesanan</span></div>
      </div>

      {data.total_orders > 0 && (
        <div className="two" style={{ marginTop: '20px' }}>
          <div className="panel">
            <h2>Pesanan terbaru</h2>
            <div className="tbl">
              <table>
                <thead><tr><th>Pelanggan</th><th>Produk</th><th className="num">Total</th><th>Tanggal</th></tr></thead>
                <tbody>
                  {data.recent_orders.map(o => (
                    <tr key={o.id}>
                      <td>{o.customer_name}</td><td>{o.product_name}</td>
                      <td className="num">${o.total_price.toFixed(2)}</td>
                      <td className="muted">{o.order_date.slice(0, 10)}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>
        </div>
      )}
    </>
  );
}