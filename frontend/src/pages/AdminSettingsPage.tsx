import { useState, useEffect } from 'react'
import { Settings, Save, Eye, EyeOff, Mail, Paperclip, Shield, Globe } from 'lucide-react'
import { listSettings, updateSettings } from '../services/api'

interface SettingItem {
  id: number
  key: string
  value: string
  category: string
  label: string
  description: string | null
  value_type: string
  updated_at: string | null
}

const categoryMeta: Record<string, { label: string; icon: typeof Mail; color: string }> = {
  email: { label: 'Email Configuration', icon: Mail, color: 'text-blue-600 bg-blue-50' },
  attachments: { label: 'Attachment Limits', icon: Paperclip, color: 'text-amber-600 bg-amber-50' },
  auto_reply: { label: 'Auto-Reply', icon: Shield, color: 'text-purple-600 bg-purple-50' },
  general: { label: 'General', icon: Globe, color: 'text-green-600 bg-green-50' },
}

export default function AdminSettingsPage() {
  const [settings, setSettings] = useState<SettingItem[]>([])
  const [edited, setEdited] = useState<Record<string, string>>({})
  const [loading, setLoading] = useState(true)
  const [saving, setSaving] = useState(false)
  const [success, setSuccess] = useState('')
  const [error, setError] = useState('')
  const [showPasswords, setShowPasswords] = useState<Record<string, boolean>>({})

  const fetchSettings = async () => {
    setLoading(true)
    try {
      const res = await listSettings()
      setSettings(res.data)
      setEdited({})
    } catch {
      setError('Failed to load settings')
    } finally {
      setLoading(false)
    }
  }

  useEffect(() => {
    fetchSettings()
  }, [])

  const handleChange = (key: string, value: string) => {
    setEdited((prev) => ({ ...prev, [key]: value }))
    setSuccess('')
  }

  const getValue = (s: SettingItem) =>
    edited[s.key] !== undefined ? edited[s.key] : s.value

  const hasChanges = Object.keys(edited).length > 0

  const handleSave = async () => {
    if (!hasChanges) return
    setSaving(true)
    setError('')
    setSuccess('')
    try {
      const res = await updateSettings(edited)
      setSettings(res.data)
      setEdited({})
      setSuccess('Settings saved successfully')
      setTimeout(() => setSuccess(''), 3000)
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Failed to save settings')
    } finally {
      setSaving(false)
    }
  }

  const handleDiscard = () => {
    setEdited({})
    setSuccess('')
    setError('')
  }

  const grouped = settings.reduce<Record<string, SettingItem[]>>((acc, s) => {
    if (!acc[s.category]) acc[s.category] = []
    acc[s.category].push(s)
    return acc
  }, {})

  const categoryOrder = ['general', 'email', 'attachments', 'auto_reply']

  if (loading) {
    return (
      <div className="flex items-center justify-center h-64 text-gray-400">
        Loading settings...
      </div>
    )
  }

  return (
    <div className="max-w-3xl">
      <div className="flex items-center justify-between mb-6">
        <div className="flex items-center gap-3">
          <Settings className="w-6 h-6 text-gray-400" />
          <h1 className="text-2xl font-bold text-gray-900">System Settings</h1>
        </div>
        <div className="flex items-center gap-2">
          {hasChanges && (
            <button
              onClick={handleDiscard}
              className="px-4 py-2 text-sm font-medium text-gray-600 bg-white border border-gray-300 rounded-lg hover:bg-gray-50 transition"
            >
              Discard
            </button>
          )}
          <button
            onClick={handleSave}
            disabled={!hasChanges || saving}
            className="inline-flex items-center gap-2 px-4 py-2 text-sm font-medium text-white bg-primary-600 rounded-lg hover:bg-primary-700 transition disabled:opacity-50 disabled:cursor-not-allowed"
          >
            <Save className="w-4 h-4" />
            {saving ? 'Saving...' : 'Save Changes'}
          </button>
        </div>
      </div>

      {success && (
        <div className="mb-4 px-4 py-3 bg-green-50 text-green-700 rounded-lg text-sm font-medium">
          {success}
        </div>
      )}
      {error && (
        <div className="mb-4 px-4 py-3 bg-red-50 text-red-700 rounded-lg text-sm font-medium">
          {error}
        </div>
      )}

      <div className="space-y-6">
        {categoryOrder.map((cat) => {
          const items = grouped[cat]
          if (!items) return null
          const meta = categoryMeta[cat] || { label: cat, icon: Globe, color: 'text-gray-600 bg-gray-50' }
          const Icon = meta.icon

          return (
            <div key={cat} className="bg-white rounded-xl shadow-sm border border-gray-200 overflow-hidden">
              <div className="px-6 py-4 border-b border-gray-100 flex items-center gap-3">
                <div className={`p-2 rounded-lg ${meta.color}`}>
                  <Icon className="w-5 h-5" />
                </div>
                <h2 className="text-lg font-semibold text-gray-900">{meta.label}</h2>
              </div>

              <div className="divide-y divide-gray-50">
                {items.map((s) => (
                  <div key={s.key} className="px-6 py-4 grid grid-cols-[1fr_1.2fr] gap-4 items-start">
                    <div>
                      <div className="text-sm font-medium text-gray-900">{s.label}</div>
                      {s.description && (
                        <div className="text-xs text-gray-400 mt-0.5">{s.description}</div>
                      )}
                    </div>
                    <div>
                      {s.value_type === 'bool' ? (
                        <label className="relative inline-flex items-center cursor-pointer">
                          <input
                            type="checkbox"
                            checked={getValue(s) === 'True' || getValue(s) === 'true'}
                            onChange={(e) =>
                              handleChange(s.key, e.target.checked ? 'True' : 'False')
                            }
                            className="sr-only peer"
                          />
                          <div className="w-11 h-6 bg-gray-200 peer-focus:outline-none peer-focus:ring-2 peer-focus:ring-primary-300 rounded-full peer peer-checked:after:translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-[2px] after:left-[2px] after:bg-white after:border-gray-300 after:border after:rounded-full after:h-5 after:w-5 after:transition-all peer-checked:bg-primary-600"></div>
                          <span className="ml-3 text-sm text-gray-500">
                            {getValue(s) === 'True' || getValue(s) === 'true' ? 'Enabled' : 'Disabled'}
                          </span>
                        </label>
                      ) : s.value_type === 'password' ? (
                        <div className="relative">
                          <input
                            type={showPasswords[s.key] ? 'text' : 'password'}
                            value={getValue(s)}
                            onChange={(e) => handleChange(s.key, e.target.value)}
                            className="w-full px-3 py-2 pr-10 text-sm border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-primary-500 outline-none"
                          />
                          <button
                            type="button"
                            onClick={() =>
                              setShowPasswords((p) => ({ ...p, [s.key]: !p[s.key] }))
                            }
                            className="absolute right-2 top-1/2 -translate-y-1/2 text-gray-400 hover:text-gray-600"
                          >
                            {showPasswords[s.key] ? (
                              <EyeOff className="w-4 h-4" />
                            ) : (
                              <Eye className="w-4 h-4" />
                            )}
                          </button>
                        </div>
                      ) : s.value_type === 'int' ? (
                        <input
                          type="number"
                          value={getValue(s)}
                          onChange={(e) => handleChange(s.key, e.target.value)}
                          className="w-full px-3 py-2 text-sm border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-primary-500 outline-none"
                        />
                      ) : s.key === 'ALLOWED_EXTENSIONS' ? (
                        <textarea
                          value={getValue(s)}
                          onChange={(e) => handleChange(s.key, e.target.value)}
                          rows={2}
                          className="w-full px-3 py-2 text-sm border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-primary-500 outline-none resize-none font-mono"
                        />
                      ) : (
                        <input
                          type="text"
                          value={getValue(s)}
                          onChange={(e) => handleChange(s.key, e.target.value)}
                          className="w-full px-3 py-2 text-sm border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-primary-500 outline-none"
                        />
                      )}
                      {edited[s.key] !== undefined && edited[s.key] !== s.value && (
                        <div className="text-xs text-amber-500 mt-1">Modified</div>
                      )}
                    </div>
                  </div>
                ))}
              </div>
            </div>
          )
        })}
      </div>
    </div>
  )
}
