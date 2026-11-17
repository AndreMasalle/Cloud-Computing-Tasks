import { NavLink } from 'react-router-dom';
import { LayoutDashboard, Package, Users, ShoppingBag, BarChart2 } from 'lucide-react';

export default function Sidebar() {
  // Fungsi untuk memberikan style khusus pada menu yang sedang aktif
  const linkStyle = ({ isActive }) => ({
    display: 'flex',
    alignItems: 'center',
    gap: '12px',
    padding: '10px 12px',
    borderRadius: '8px',
    color: isActive ? '#2A2000' : 'inherit',
    textDecoration: 'none',
    fontWeight: 500,
    background: isActive ? 'var(--sun)' : 'transparent'
  });

  return (
    <aside>
      <div className="brand">OpenLapak<small>Analitik toko online</small></div>
      <nav>
        {/* NavLink akan otomatis memberikan style aktif jika URL cocok */}
        <NavLink to="/dashboard" style={linkStyle}>
          <LayoutDashboard size={18} />Dashboard
        </NavLink>

        <NavLink to="/products" style={linkStyle}>
          <Package size={18} />Produk
        </NavLink>

        <NavLink to="/customers" style={linkStyle}>
          <Users size={18} />Pelanggan
        </NavLink>

        <NavLink to="/orders" style={linkStyle}>
          <ShoppingBag size={18} />Pesanan
        </NavLink>

        <NavLink to="/analytics" style={linkStyle}>
          <BarChart2 size={18} />Analitik
        </NavLink>
      </nav>

      {/* Indikator status server */}
      <div className="side-foot">
        <span className="dot on"></span>Server terhubung
      </div>
    </aside>
  );
}