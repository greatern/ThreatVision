import { Shield } from 'lucide-react'

function Header() {
  return (
    <header style={{
      backgroundColor: '#1a1d27',
      borderBottom: '1px solid #2d3148',
      padding: '16px 32px',
      display: 'flex',
      alignItems: 'center',
      gap: '12px'
    }}>
      <Shield size={28} color="#6366f1" />
      <div>
        <h1 style={{ fontSize: '20px', fontWeight: '700', color: '#e2e8f0' }}>
          ThreatVision
        </h1>
        <p style={{ fontSize: '12px', color: '#64748b' }}>
          Cybersecurity Threat Detection Platform
        </p>
      </div>
    </header>
  )
}

export default Header