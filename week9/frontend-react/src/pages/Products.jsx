import { useEffect, useState } from 'react';
import api from '../api';

export default function Products() {
  const [products, setProducts] = useState([]);
  const [form, setForm] = useState({ name: '', category: '', price: '', stock: '' });

  // Fungsi untuk mengambil data dari backend FastAPI
  const fetchProducts = async () => {
    try {
      const res = await api.get('/products');
      setProducts(res.data);
    } catch (error) {
      console.error("Gagal mengambil data produk:", error);
    }
  };

  // Jalankan fetchProducts saat komponen pertama kali dimuat
  useEffect(() => {
    fetchProducts();
  }, []);

  // Fungsi saat form disubmit (Tambah Produk)
  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      await api.post('/products', {
        ...form,
        price: parseFloat(form.price),
        stock: parseInt(form.stock)
      });
      // Kosongkan form setelah berhasil
      setForm({ name: '', category: '', price: '', stock: '' });
      // Refresh tabel
      fetchProducts();
    } catch (error) {
      alert("Gagal menambah produk");
    }
  };

  // Fungsi untuk menghapus produk
  const handleDelete = async (id) => {
    if (window.confirm("Apakah kamu yakin ingin menghapus produk ini?")) {
      try {
        await api.delete(`/products/${id}`);
        fetchProducts();
      } catch (error) {
        alert("Gagal menghapus produk");
      }
    }
  };

  return (
    <>
      <div className="head">
        <div>
          <h1>Produk</h1>
          <p>{products.length} produk di katalog.</p>
        </div>
      </div>

      {/* Form Tambah Produk */}
      <div className="panel" style={{ marginBottom: '20px' }}>
        <h2>Tambah Produk Baru</h2>
        <form onSubmit={handleSubmit} style={{ display: 'flex', gap: '10px', marginTop: '10px' }}>
          <input
            placeholder="Nama Produk"
            value={form.name}
            onChange={e => setForm({...form, name: e.target.value})}
            required
          />
          <input
            placeholder="Kategori"
            value={form.category}
            onChange={e => setForm({...form, category: e.target.value})}
            required
          />
          <input
            type="number"
            step="0.01"
            placeholder="Harga ($)"
            value={form.price}
            onChange={e => setForm({...form, price: e.target.value})}
            required
          />
          <input
            type="number"
            placeholder="Stok"
            value={form.stock}
            onChange={e => setForm({...form, stock: e.target.value})}
            required
          />
          <button type="submit" className="btn">Tambah</button>
        </form>
      </div>

      {/* Tabel Daftar Produk */}
      <div className="panel">
        <div className="tbl">
          <table>
            <thead>
              <tr>
                <th>Nama</th>
                <th>Kategori</th>
                <th className="num">Harga</th>
                <th className="num">Stok</th>
                <th></th>
              </tr>
            </thead>
            <tbody>
              {products.length === 0 ? (
                <tr>
                  <td colSpan="5" style={{ textAlign: 'center', padding: '20px' }}>
                    Belum ada produk. Silakan tambah produk baru.
                  </td>
                </tr>
              ) : (
                products.map(p => (
                  <tr key={p.id}>
                    <td><b>{p.name}</b></td>
                    <td>{p.category}</td>
                    <td className="num">${p.price.toFixed(2)}</td>
                    <td className="num">
                      {p.stock <= 5 ? (
                        <span className="badge low">{p.stock}</span>
                      ) : (
                        p.stock
                      )}
                    </td>
                    <td className="act">
                      <button className="btn link del" onClick={() => handleDelete(p.id)}>
                        Hapus
                      </button>
                    </td>
                  </tr>
                ))
              )}
            </tbody>
          </table>
        </div>
      </div>
    </>
  );
}