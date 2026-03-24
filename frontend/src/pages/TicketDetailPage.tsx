import { useState, useEffect } from 'react'
import { useParams, Link } from 'react-router-dom'
import { ArrowLeft, Paperclip, Download, Send, UserPlus, Clock } from 'lucide-react'
import {
  getTicket,
  listComments,
  createComment,
  updateTicket,
  assignTicket,
  listUsers,
  getAttachmentDownloadUrl,
} from '../services/api'
import clsx from 'clsx'

interface User {
  id: number
  name: string
  email: string
  role: string
}

interface Attachment {
  id: number
  ticket_id: number
  original_filename: string
  content_type: string
  size_bytes: number
  uploaded_at: string
}

interface Comment {
  id: number
  ticket_id: number
  author_id: number | null
  author_email: string | null
  body: string
  source: string
  created_at: string
  attachments: Attachment[]
}

interface TicketData {
  id: number
  subject: string
  category: string
  project: string
  priority: string
  status: string
  description: string
  reporter_email: string
  sla_deadline: string | null
  created_at: string
  updated_at: string
  attachments: Attachment[]
}

const statusOptions = ['open', 'in_progress', 'resolved', 'closed']
const statusColors: Record<string, string> = {
  open: 'bg-blue-100 text-blue-800',
  in_progress: 'bg-yellow-100 text-yellow-800',
  resolved: 'bg-green-100 text-green-800',
  closed: 'bg-gray-100 text-gray-600',
}

function formatBytes(bytes: number): string {
  if (bytes < 1024) return bytes + ' B'
  if (bytes < 1024 * 1024) return (bytes / 1024).toFixed(1) + ' KB'
  return (bytes / (1024 * 1024)).toFixed(1) + ' MB'
}

function isPreviewable(contentType: string): boolean {
  return contentType.startsWith('image/') || contentType === 'application/pdf'
}

export default function TicketDetailPage({ user }: { user: User }) {
  const { id } = useParams<{ id: string }>()
  const [ticket, setTicket] = useState<TicketData | null>(null)
  const [comments, setComments] = useState<Comment[]>([])
  const [agents, setAgents] = useState<User[]>([])
  const [newComment, setNewComment] = useState('')
  const [selectedAgent, setSelectedAgent] = useState('')
  const [loading, setLoading] = useState(true)
  const [submitting, setSubmitting] = useState(false)

  const isStaff = user.role === 'admin' || user.role === 'manager' || user.role === 'agent'

  const fetchData = async () => {
    try {
      const [ticketRes, commentsRes] = await Promise.all([
        getTicket(Number(id)),
        listComments(Number(id)),
      ])
      setTicket(ticketRes.data)
      setComments(commentsRes.data)

      if (isStaff) {
        const agentsRes = await listUsers('agent')
        setAgents(agentsRes.data)
      }
    } catch (err) {
      console.error('Failed to load ticket', err)
    } finally {
      setLoading(false)
    }
  }

  useEffect(() => {
    fetchData()
  }, [id])

  const handleStatusChange = async (newStatus: string) => {
    if (!ticket) return
    try {
      const res = await updateTicket(ticket.id, { status: newStatus })
      setTicket(res.data)
    } catch (err) {
      console.error('Failed to update status', err)
    }
  }

  const handleAssign = async () => {
    if (!ticket || !selectedAgent) return
    try {
      await assignTicket(ticket.id, Number(selectedAgent))
      await fetchData()
    } catch (err) {
      console.error('Failed to assign', err)
    }
  }

  const handleComment = async (e: React.FormEvent) => {
    e.preventDefault()
    if (!newComment.trim() || !ticket) return
    setSubmitting(true)
    try {
      await createComment(ticket.id, newComment)
      setNewComment('')
      const res = await listComments(ticket.id)
      setComments(res.data)
    } catch (err) {
      console.error('Failed to add comment', err)
    } finally {
      setSubmitting(false)
    }
  }

  if (loading) {
    return <div className="p-12 text-center text-gray-400">Loading...</div>
  }

  if (!ticket) {
    return <div className="p-12 text-center text-red-500">Ticket not found</div>
  }

  return (
    <div>
      <Link to="/tickets" className="inline-flex items-center gap-1.5 text-sm text-gray-500 hover:text-gray-700 mb-4">
        <ArrowLeft className="w-4 h-4" /> Back to tickets
      </Link>

      <div className="grid grid-cols-3 gap-6">
        {/* Main content */}
        <div className="col-span-2 space-y-6">
          {/* Ticket header */}
          <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
            <div className="flex items-start justify-between mb-3">
              <div>
                <span className="text-xs font-mono text-gray-400">#{ticket.id}</span>
                <h1 className="text-xl font-bold text-gray-900 mt-1">{ticket.subject}</h1>
              </div>
              <span className={clsx('text-xs px-3 py-1 rounded-full font-medium', statusColors[ticket.status])}>
                {ticket.status.replace('_', ' ')}
              </span>
            </div>
            <div className="prose prose-sm max-w-none text-gray-700 whitespace-pre-wrap">
              {ticket.description}
            </div>
          </div>

          {/* Attachments */}
          {ticket.attachments.length > 0 && (
            <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
              <h3 className="text-sm font-semibold text-gray-700 mb-3 flex items-center gap-2">
                <Paperclip className="w-4 h-4" /> Attachments ({ticket.attachments.length})
              </h3>
              <div className="space-y-2">
                {ticket.attachments.map((att) => (
                  <div key={att.id} className="flex items-center justify-between bg-gray-50 rounded-lg px-4 py-2.5">
                    <div className="flex items-center gap-3 min-w-0">
                      <Paperclip className="w-4 h-4 text-gray-400 shrink-0" />
                      <div className="min-w-0">
                        <p className="text-sm font-medium text-gray-800 truncate">{att.original_filename}</p>
                        <p className="text-xs text-gray-400">{formatBytes(att.size_bytes)} · {att.content_type}</p>
                      </div>
                    </div>
                    <div className="flex items-center gap-2 shrink-0">
                      {isPreviewable(att.content_type) && (
                        <a
                          href={getAttachmentDownloadUrl(att.id)}
                          target="_blank"
                          rel="noopener noreferrer"
                          className="text-xs text-primary-600 hover:underline"
                        >
                          Preview
                        </a>
                      )}
                      <a
                        href={getAttachmentDownloadUrl(att.id)}
                        download
                        className="inline-flex items-center gap-1 text-xs text-primary-600 hover:underline"
                      >
                        <Download className="w-3.5 h-3.5" /> Download
                      </a>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          )}

          {/* Comments */}
          <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
            <h3 className="text-sm font-semibold text-gray-700 mb-4">Comments ({comments.length})</h3>
            <div className="space-y-4 mb-6">
              {comments.length === 0 && (
                <p className="text-sm text-gray-400">No comments yet</p>
              )}
              {comments.map((c) => (
                <div key={c.id} className="border-l-2 border-gray-200 pl-4">
                  <div className="flex items-center gap-2 mb-1">
                    <span className="text-sm font-medium text-gray-800">
                      {c.author_email || 'Unknown'}
                    </span>
                    <span className="text-xs text-gray-400">
                      {new Date(c.created_at).toLocaleString()}
                    </span>
                    <span className={clsx(
                      'text-xs px-1.5 py-0.5 rounded',
                      c.source === 'email' ? 'bg-purple-50 text-purple-600' : 'bg-gray-100 text-gray-500'
                    )}>
                      {c.source}
                    </span>
                  </div>
                  <p className="text-sm text-gray-700 whitespace-pre-wrap">{c.body}</p>
                  {c.attachments.length > 0 && (
                    <div className="mt-2 flex flex-wrap gap-2">
                      {c.attachments.map((att) => (
                        <a
                          key={att.id}
                          href={getAttachmentDownloadUrl(att.id)}
                          className="inline-flex items-center gap-1 text-xs bg-gray-100 px-2 py-1 rounded hover:bg-gray-200"
                        >
                          <Paperclip className="w-3 h-3" /> {att.original_filename}
                        </a>
                      ))}
                    </div>
                  )}
                </div>
              ))}
            </div>

            {/* Add comment */}
            <form onSubmit={handleComment} className="border-t pt-4">
              <textarea
                value={newComment}
                onChange={(e) => setNewComment(e.target.value)}
                placeholder="Add a comment..."
                rows={3}
                className="w-full border border-gray-300 rounded-lg px-4 py-2.5 text-sm focus:ring-2 focus:ring-primary-500 focus:border-primary-500 outline-none resize-none"
              />
              <div className="flex justify-end mt-2">
                <button
                  type="submit"
                  disabled={submitting || !newComment.trim()}
                  className="inline-flex items-center gap-1.5 bg-primary-600 text-white px-4 py-2 rounded-lg text-sm font-medium hover:bg-primary-700 transition disabled:opacity-50"
                >
                  <Send className="w-4 h-4" />
                  {submitting ? 'Sending...' : 'Send'}
                </button>
              </div>
            </form>
          </div>
        </div>

        {/* Sidebar */}
        <div className="space-y-4">
          {/* Details card */}
          <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-5">
            <h3 className="text-sm font-semibold text-gray-700 mb-3">Details</h3>
            <dl className="space-y-3 text-sm">
              <div>
                <dt className="text-gray-400">Category</dt>
                <dd className="font-medium text-gray-800">{ticket.category}</dd>
              </div>
              <div>
                <dt className="text-gray-400">Project</dt>
                <dd className="font-medium text-gray-800">{ticket.project}</dd>
              </div>
              <div>
                <dt className="text-gray-400">Priority</dt>
                <dd className="font-medium text-gray-800">{ticket.priority}</dd>
              </div>
              <div>
                <dt className="text-gray-400">Reporter</dt>
                <dd className="font-medium text-gray-800">{ticket.reporter_email}</dd>
              </div>
              <div>
                <dt className="text-gray-400">Created</dt>
                <dd className="font-medium text-gray-800">{new Date(ticket.created_at).toLocaleString()}</dd>
              </div>
              {ticket.sla_deadline && (
                <div>
                  <dt className="text-gray-400 flex items-center gap-1"><Clock className="w-3.5 h-3.5" /> SLA Deadline</dt>
                  <dd className="font-medium text-gray-800">{new Date(ticket.sla_deadline).toLocaleString()}</dd>
                </div>
              )}
            </dl>
          </div>

          {/* Actions (staff only) */}
          {isStaff && (
            <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-5 space-y-4">
              <h3 className="text-sm font-semibold text-gray-700">Actions</h3>

              {/* Status change */}
              <div>
                <label className="text-xs text-gray-400 block mb-1">Status</label>
                <select
                  value={ticket.status}
                  onChange={(e) => handleStatusChange(e.target.value)}
                  className="w-full text-sm border border-gray-300 rounded-lg px-3 py-2 focus:ring-2 focus:ring-primary-500 outline-none"
                >
                  {statusOptions.map((s) => (
                    <option key={s} value={s}>{s.replace('_', ' ')}</option>
                  ))}
                </select>
              </div>

              {/* Assignment */}
              <div>
                <label className="text-xs text-gray-400 block mb-1">Assign to Agent</label>
                <div className="flex gap-2">
                  <select
                    value={selectedAgent}
                    onChange={(e) => setSelectedAgent(e.target.value)}
                    className="flex-1 text-sm border border-gray-300 rounded-lg px-3 py-2 focus:ring-2 focus:ring-primary-500 outline-none"
                  >
                    <option value="">Select agent...</option>
                    {agents.map((a) => (
                      <option key={a.id} value={a.id}>{a.name}</option>
                    ))}
                  </select>
                  <button
                    onClick={handleAssign}
                    disabled={!selectedAgent}
                    className="inline-flex items-center gap-1 bg-gray-800 text-white px-3 py-2 rounded-lg text-sm hover:bg-gray-900 transition disabled:opacity-50"
                  >
                    <UserPlus className="w-4 h-4" />
                  </button>
                </div>
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  )
}
