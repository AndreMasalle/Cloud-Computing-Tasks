import { useEffect, useState } from 'react';
import api from '../api';

export default function Orders() {
  const [orders, setOrders] = useState([]);
  const [customers, setCustomers] = useState([]);
  const [products, setProducts] = useState([]);

  const [form, setForm] = useState({ customer_id: '', product_id: '', quantity: 1 });

  const fetchData = async () => {
    const [resOrders, resCust, resProd] = await Promise.all([
      api.get('/orders'), api.get('/customers'), api.get('/products')
    ]);
    setOrders(resOrders.data);
    setCustomers(resCust.data);
    setProducts(resProd.data);
  };

  useEffect(() => { fetchData(); }, []);

  const handleSubmit = async (e) => {
    e.preventDefault();
    if(!form.customer_id || !form.product_id) return alert("Pilih pelanggan dan produk");
    await api.post('/orders', { ...form, quantity: parseInt(form.quantity) });
    setForm({ ...form, quantity: 1 });
    fetchData();
  };

  const handleDelete = async (id) => {
    if (window.confirm("Hapus pesanan ini?")) {
      await api.delete(`/orders/${id}`);
      fetchData();
    }
  };

  return (
    <>
      <div className="head"><div><h1>Pesanan</h1><p>{orders.length} pesanan tercatat.</p></div></div>

      <div className="panel" style={{ marginBottom: '20px' }}>
        <form onSubmit={handleSubmit} style={{ display: 'flex', gap: '10px' }}>
          <select value={form.customer_id} onChange={e => setForm({...form, customer_id: e.target.value})} required>
            <option value="">-- Pilih Pelanggan --</option>
            {customers.map(c => <option key={c.id} value={c.id}>{c.name}</option>)}
          </select>
          <select value={form.product_id} onChange={e => setForm({...form, product_id: e.target.value})} required>
            <option value="">-- Pilih Produk --</option>
            {products.map(p => <option key={p.id} value={p.id}>{p.name} (${p.price})</option>)}
          </select>
          <input type="number" min="1" placeholder="Qty" value={form.quantity} onChange={e => setForm({...form, quantity: e.target.value})} required style={{ width: '80px' }} />
          <button type="submit" className="btn">Buat Pesanan</button>
        </form>
      </div>

      <div className="panel">
        <div className="tbl">
          <table>
            <thead><tr><th>Pelanggan</th><th>Produk</th><th className="num">Qty</th><th className="num">Total</th><th></th></tr></thead>
            <tbody>
              {orders.map(o => (
                <tr key={o.id}>
                  <td>{o.customer_name}</td><td>{o.product_name}</td>
                  <td className="num">{o.quantity}</td>
                  <td className="num">${o.total_price.toFixed(2)}</td>
                  <td className="act"><button className="btn link del" onClick={() => handleDelete(o.id)}>Hapus</button></td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </>
  );
}