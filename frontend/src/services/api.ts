import axios from 'axios'

const api = axios.create({
  baseURL: import.meta.env.VITE_API_URL || '/api',
})

api.interceptors.request.use((config) => {
  const token = localStorage.getItem('token')
  if (token) {
    config.headers.Authorization = `Bearer ${token}`
  }
  return config
})

api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      localStorage.removeItem('token')
      localStorage.removeItem('user')
      window.location.href = '/login'
    }
    return Promise.reject(error)
  }
)

export default api

// Auth
export const login = (email: string, password: string) =>
  api.post('/auth/login', { email, password })

export const register = (data: { name: string; email: string; password: string; role?: string; team?: string }) =>
  api.post('/auth/register', data)

// Users
export const getMe = () => api.get('/users/me')
export const listUsers = (role?: string) =>
  api.get('/users/', { params: role ? { role } : {} })
export const updateUser = (id: number, data: Record<string, unknown>) =>
  api.put(`/users/${id}`, data)

// Tickets
export const listTickets = (params?: Record<string, string | number>) =>
  api.get('/tickets/', { params })

export const getTicket = (id: number) => api.get(`/tickets/${id}`)

export const createTicket = (data: {
  subject: string
  category: string
  project: string
  priority: string
  description: string
}) => api.post('/tickets/', data)

export const updateTicket = (id: number, data: Record<string, unknown>) =>
  api.put(`/tickets/${id}`, data)

// Assignments
export const assignTicket = (ticketId: number, agentId: number) =>
  api.post(`/tickets/${ticketId}/assign`, { agent_id: agentId })

// Comments
export const listComments = (ticketId: number) =>
  api.get(`/tickets/${ticketId}/comments`)

export const createComment = (ticketId: number, body: string) =>
  api.post(`/tickets/${ticketId}/comments`, { body })

// Attachments
export const listAttachments = (ticketId: number) =>
  api.get(`/tickets/${ticketId}/attachments`)

export const getAttachmentDownloadUrl = (attachmentId: number) => {
  const token = localStorage.getItem('token')
  const base = import.meta.env.VITE_API_URL || '/api'
  return `${base}/attachments/${attachmentId}/download?token=${encodeURIComponent(token || '')}`
}

export const uploadAttachments = (ticketId: number, files: File[]) => {
  const formData = new FormData()
  formData.append('ticket_id', String(ticketId))
  files.forEach((f) => formData.append('files', f))
  return api.post('/attachments/upload', formData, {
    headers: { 'Content-Type': 'multipart/form-data' },
  })
}

// Notifications
export const listNotifications = (unreadOnly = false) =>
  api.get('/notifications/', { params: { unread_only: unreadOnly } })

export const markNotificationRead = (id: number) =>
  api.put(`/notifications/${id}/read`)

export const markAllNotificationsRead = () =>
  api.put('/notifications/read-all')

// Settings
export const listSettings = (category?: string) =>
  api.get('/settings/', { params: category ? { category } : {} })

export const updateSettings = (settings: Record<string, string>) =>
  api.put('/settings/', { settings })
