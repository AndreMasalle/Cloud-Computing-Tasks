import { useEffect, useState } from 'react';
import api from '../api';

export default function Customers() {
  const [customers, setCustomers] = useState([]);
  const [form, setForm] = useState({ name: '', email: '', tier: 'Bronze' });

  const fetchCustomers = async () => {
    const res = await api.get('/customers');
    setCustomers(res.data);
  };

  useEffect(() => { fetchCustomers(); }, []);

  const handleSubmit = async (e) => {
    e.preventDefault();
    await api.post('/customers', form);
    setForm({ name: '', email: '', tier: 'Bronze' });
    fetchCustomers();
  };

  const handleDelete = async (id) => {
    if (window.confirm("Hapus pelanggan ini?")) {
      await api.delete(`/customers/${id}`);
      fetchCustomers();
    }
  };

  return (
    <>
      <div className="head"><div><h1>Pelanggan</h1><p>{customers.length} pelanggan terdaftar.</p></div></div>

      <div className="panel" style={{ marginBottom: '20px' }}>
        <form onSubmit={handleSubmit} style={{ display: 'flex', gap: '10px' }}>
          <input placeholder="Nama" value={form.name} onChange={e => setForm({...form, name: e.target.value})} required />
          <input type="email" placeholder="Email" value={form.email} onChange={e => setForm({...form, email: e.target.value})} required />
          <select value={form.tier} onChange={e => setForm({...form, tier: e.target.value})}>
            <option value="Bronze">Bronze</option>
            <option value="Silver">Silver</option>
            <option value="Gold">Gold</option>
            <option value="Platinum">Platinum</option>
          </select>
          <button type="submit" className="btn">Tambah</button>
        </form>
      </div>

      <div className="panel">
        <div className="tbl">
          <table>
            <thead><tr><th>Nama</th><th>Email</th><th>Membership</th><th></th></tr></thead>
            <tbody>
              {customers.map(c => (
                <tr key={c.id}>
                  <td><b>{c.name}</b></td><td>{c.email}</td>
                  <td><span className={`badge ${c.tier}`}>{c.tier}</span></td>
                  <td className="act"><button className="btn link del" onClick={() => handleDelete(c.id)}>Hapus</button></td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </>
  );
}