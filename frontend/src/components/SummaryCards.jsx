import { AlertTriangle, ShieldAlert, ShieldCheck, Activity } from 'lucide-react'

function StatCard({ title, value, icon: Icon, color }) {
  return (
    <div style={{
      backgroundColor: '#1a1d27',
      border: `1px solid ${color}33`,
      borderRadius: '12px',
      padding: '24px',
      display: 'flex',
      alignItems: 'center',
      gap: '16px',
      flex: 1
    }}>
      <div style={{
        backgroundColor: `${color}22`,
        borderRadius: '10px',
        padding: '12px',
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'center'
      }}>
        <Icon size={24} color={color} />
      </div>
      <div>
        <p style={{ fontSize: '13px', color: '#64748b', marginBottom: '4px' }}>{title}</p>
        <p style={{ fontSize: '28px', fontWeight: '700', color: '#e2e8f0' }}>{value}</p>
      </div>
    </div>
  )
}

function SummaryCards({ summary }) {
  return (
    <div style={{ display: 'flex', gap: '16px', marginBottom: '24px' }}>
      <StatCard title="Total Alerts" value={summary.total} icon={Activity} color="#6366f1" />
      <StatCard title="High Severity" value={summary.high} icon={ShieldAlert} color="#ef4444" />
      <StatCard title="Medium Severity" value={summary.medium} icon={AlertTriangle} color="#f59e0b" />
      <StatCard title="Low Severity" value={summary.low} icon={ShieldCheck} color="#22c55e" />
    </div>
  )
}

export default SummaryCards