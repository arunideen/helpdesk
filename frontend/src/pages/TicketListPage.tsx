import { useState, useEffect } from 'react'
import { Link } from 'react-router-dom'
import { Search, Filter, ChevronRight, Paperclip } from 'lucide-react'
import { listTickets } from '../services/api'
import clsx from 'clsx'

const statusColors: Record<string, string> = {
  open: 'bg-blue-100 text-blue-800',
  in_progress: 'bg-yellow-100 text-yellow-800',
  resolved: 'bg-green-100 text-green-800',
  closed: 'bg-gray-100 text-gray-600',
}

const priorityColors: Record<string, string> = {
  Low: 'text-gray-500',
  Medium: 'text-blue-600',
  High: 'text-orange-600',
  Critical: 'text-red-600 font-semibold',
}

interface Ticket {
  id: number
  subject: string
  category: string
  project: string
  priority: string
  status: string
  reporter_email: string
  created_at: string
  attachment_count: number
}

export default function TicketListPage() {
  const [tickets, setTickets] = useState<Ticket[]>([])
  const [total, setTotal] = useState(0)
  const [loading, setLoading] = useState(true)
  const [filters, setFilters] = useState({
    status: '',
    priority: '',
    category: '',
    project: '',
  })

  const fetchTickets = async () => {
    setLoading(true)
    try {
      const params: Record<string, string> = {}
      if (filters.status) params.status = filters.status
      if (filters.priority) params.priority = filters.priority
      if (filters.category) params.category = filters.category
      if (filters.project) params.project = filters.project

      const res = await listTickets(params)
      setTickets(res.data.items)
      setTotal(res.data.total)
    } catch (err) {
      console.error('Failed to load tickets', err)
    } finally {
      setLoading(false)
    }
  }

  useEffect(() => {
    fetchTickets()
  }, [filters])

  return (
    <div>
      <div className="flex items-center justify-between mb-6">
        <div>
          <h1 className="text-2xl font-bold text-gray-900">Tickets</h1>
          <p className="text-sm text-gray-500 mt-1">{total} total tickets</p>
        </div>
        <Link
          to="/tickets/new"
          className="bg-primary-600 text-white px-4 py-2 rounded-lg text-sm font-medium hover:bg-primary-700 transition"
        >
          + New Ticket
        </Link>
      </div>

      {/* Filters */}
      <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-4 mb-6">
        <div className="flex items-center gap-2 mb-3">
          <Filter className="w-4 h-4 text-gray-400" />
          <span className="text-sm font-medium text-gray-600">Filters</span>
        </div>
        <div className="grid grid-cols-4 gap-3">
          <select
            value={filters.status}
            onChange={(e) => setFilters({ ...filters, status: e.target.value })}
            className="text-sm border border-gray-300 rounded-lg px-3 py-2 focus:ring-2 focus:ring-primary-500 outline-none"
          >
            <option value="">All Statuses</option>
            <option value="open">Open</option>
            <option value="in_progress">In Progress</option>
            <option value="resolved">Resolved</option>
            <option value="closed">Closed</option>
          </select>
          <select
            value={filters.priority}
            onChange={(e) => setFilters({ ...filters, priority: e.target.value })}
            className="text-sm border border-gray-300 rounded-lg px-3 py-2 focus:ring-2 focus:ring-primary-500 outline-none"
          >
            <option value="">All Priorities</option>
            <option value="Low">Low</option>
            <option value="Medium">Medium</option>
            <option value="High">High</option>
            <option value="Critical">Critical</option>
          </select>
          <select
            value={filters.category}
            onChange={(e) => setFilters({ ...filters, category: e.target.value })}
            className="text-sm border border-gray-300 rounded-lg px-3 py-2 focus:ring-2 focus:ring-primary-500 outline-none"
          >
            <option value="">All Categories</option>
            <option value="Bug">Bug</option>
            <option value="Feature">Feature</option>
            <option value="Access">Access</option>
            <option value="Infra">Infra</option>
            <option value="General">General</option>
            <option value="Urgent">Urgent</option>
          </select>
          <input
            type="text"
            placeholder="Search project..."
            value={filters.project}
            onChange={(e) => setFilters({ ...filters, project: e.target.value })}
            className="text-sm border border-gray-300 rounded-lg px-3 py-2 focus:ring-2 focus:ring-primary-500 outline-none"
          />
        </div>
      </div>

      {/* Ticket list */}
      <div className="bg-white rounded-xl shadow-sm border border-gray-200 divide-y divide-gray-100">
        {loading ? (
          <div className="p-12 text-center text-gray-400">Loading...</div>
        ) : tickets.length === 0 ? (
          <div className="p-12 text-center text-gray-400">No tickets found</div>
        ) : (
          tickets.map((ticket) => (
            <Link
              key={ticket.id}
              to={`/tickets/${ticket.id}`}
              className="flex items-center gap-4 px-5 py-4 hover:bg-gray-50 transition group"
            >
              <div className="flex-1 min-w-0">
                <div className="flex items-center gap-2 mb-1">
                  <span className="text-xs font-mono text-gray-400">#{ticket.id}</span>
                  <span className={clsx('text-xs px-2 py-0.5 rounded-full font-medium', statusColors[ticket.status] || 'bg-gray-100')}>
                    {ticket.status.replace('_', ' ')}
                  </span>
                  <span className="text-xs bg-gray-100 text-gray-600 px-2 py-0.5 rounded-full">
                    {ticket.category}
                  </span>
                  {ticket.attachment_count > 0 && (
                    <span className="flex items-center gap-1 text-xs text-gray-400">
                      <Paperclip className="w-3 h-3" />
                      {ticket.attachment_count}
                    </span>
                  )}
                </div>
                <p className="text-sm font-medium text-gray-900 truncate">{ticket.subject}</p>
                <p className="text-xs text-gray-400 mt-0.5">
                  {ticket.reporter_email} · {ticket.project} · {new Date(ticket.created_at).toLocaleDateString()}
                </p>
              </div>
              <div className="text-right shrink-0">
                <span className={clsx('text-xs font-medium', priorityColors[ticket.priority])}>
                  {ticket.priority}
                </span>
              </div>
              <ChevronRight className="w-4 h-4 text-gray-300 group-hover:text-gray-500 transition" />
            </Link>
          ))
        )}
      </div>
    </div>
  )
}
