import { useState, useEffect } from 'react'
import Header from './components/Header'
import SummaryCards from './components/SummaryCards'
import AlertTable from './components/AlertTable'

const API_URL = 'http://localhost:8000'

function App() {
  const [alerts, setAlerts] = useState([])
  const [summary, setSummary] = useState({ total: 0, high: 0, medium: 0, low: 0 })
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)

  async function fetchAlerts() {
    try {
      const res = await fetch(`${API_URL}/alerts`)
      if (!res.ok) throw new Error('Failed to fetch alerts')
      const data = await res.json()
      setAlerts(data)
    } catch (err) {
      setError('Could not connect to the ThreatVision API.')
    }
  }

  async function fetchSummary() {
    try {
      const res = await fetch(`${API_URL}/alerts/summary`)
      if (!res.ok) throw new Error('Failed to fetch summary')
      const data = await res.json()
      setSummary(data)
    } catch (err) {
      console.error('Summary fetch failed:', err)
    }
  }

  async function handleDelete(id) {
    try {
      await fetch(`${API_URL}/alerts/${id}`, { method: 'DELETE' })
      await fetchAlerts()
      await fetchSummary()
    } catch (err) {
      console.error('Delete failed:', err)
    }
  }

  useEffect(() => {
    async function loadData() {
      setLoading(true)
      await fetchAlerts()
      await fetchSummary()
      setLoading(false)
    }
    loadData()

    const interval = setInterval(() => {
      fetchAlerts()
      fetchSummary()
    }, 5000)

    return () => clearInterval(interval)
  }, [])

  return (
    <div style={{ minHeight: '100vh' }}>
      <Header />
      <main style={{ padding: '32px' }}>
        {loading && (
          <p style={{ color: '#64748b', textAlign: 'center' }}>Loading...</p>
        )}
        {error && (
          <p style={{ color: '#ef4444', textAlign: 'center' }}>{error}</p>
        )}
        {!loading && !error && (
          <>
            <SummaryCards summary={summary} />
            <AlertTable alerts={alerts} onDelete={handleDelete} />
          </>
        )}
      </main>
    </div>
  )
}

export default App
