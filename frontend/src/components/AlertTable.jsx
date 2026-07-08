import { Trash2 } from 'lucide-react'

function SeverityBadge({ severity }) {
  const colors = {
    HIGH: { bg: '#ef444422', color: '#ef4444', border: '#ef444444' },
    MEDIUM: { bg: '#f59e0b22', color: '#f59e0b', border: '#f59e0b44' },
    LOW: { bg: '#22c55e22', color: '#22c55e', border: '#22c55e44' }
  }

  const style = colors[severity] || colors.LOW

  return (
    <span style={{
      backgroundColor: style.bg,
      color: style.color,
      border: `1px solid ${style.border}`,
      borderRadius: '6px',
      padding: '3px 10px',
      fontSize: '12px',
      fontWeight: '600'
    }}>
      {severity}
    </span>
  )
}

function AlertTable({ alerts, onDelete }) {
  if (alerts.length === 0) {
    return (
      <div style={{
        backgroundColor: '#1a1d27',
        borderRadius: '12px',
        padding: '48px',
        textAlign: 'center',
        color: '#64748b'
      }}>
        No alerts detected yet.
      </div>
    )
  }

  return (
    <div style={{
      backgroundColor: '#1a1d27',
      borderRadius: '12px',
      border: '1px solid #2d3148',
      overflow: 'hidden'
    }}>
      <table style={{ width: '100%', borderCollapse: 'collapse' }}>
        <thead>
          <tr style={{ borderBottom: '1px solid #2d3148' }}>
            {['ID', 'Type', 'IP Address', 'Severity', 'Message', ''].map(header => (
              <th key={header} style={{
                padding: '14px 20px',
                textAlign: 'left',
                fontSize: '12px',
                fontWeight: '600',
                color: '#64748b',
                textTransform: 'uppercase',
                letterSpacing: '0.05em'
              }}>
                {header}
              </th>
            ))}
          </tr>
        </thead>
        <tbody>
          {alerts.map((alert, index) => (
            <tr key={alert.id} style={{
              borderBottom: index < alerts.length - 1 ? '1px solid #2d3148' : 'none',
              transition: 'background-color 0.15s'
            }}
              onMouseEnter={e => e.currentTarget.style.backgroundColor = '#ffffff08'}
              onMouseLeave={e => e.currentTarget.style.backgroundColor = 'transparent'}
            >
              <td style={{ padding: '14px 20px', fontSize: '14px', color: '#64748b' }}>#{alert.id}</td>
              <td style={{ padding: '14px 20px', fontSize: '14px', color: '#e2e8f0', fontWeight: '500' }}>{alert.type}</td>
              <td style={{ padding: '14px 20px', fontSize: '14px', fontFamily: 'monospace', color: '#6366f1' }}>{alert.ip}</td>
              <td style={{ padding: '14px 20px' }}><SeverityBadge severity={alert.severity} /></td>
              <td style={{ padding: '14px 20px', fontSize: '14px', color: '#94a3b8' }}>{alert.message}</td>
              <td style={{ padding: '14px 20px' }}>
                <button
                  onClick={() => onDelete(alert.id)}
                  style={{
                    background: 'none',
                    border: 'none',
                    cursor: 'pointer',
                    color: '#64748b',
                    padding: '6px',
                    borderRadius: '6px',
                    display: 'flex',
                    alignItems: 'center',
                    transition: 'color 0.15s'
                  }}
                  onMouseEnter={e => e.currentTarget.style.color = '#ef4444'}
                  onMouseLeave={e => e.currentTarget.style.color = '#64748b'}
                >
                  <Trash2 size={16} />
                </button>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  )
}

export default AlertTable