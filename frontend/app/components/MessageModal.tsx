'use client'

import { useState } from 'react'

interface MessageModalProps {
  onClose: () => void
  onSendMessage: (message: {
    title: string
    content: string
    recipients: string[]
    priority: 'normal' | 'urgent'
  }) => void
}

const MessageModal = ({ onClose, onSendMessage }: MessageModalProps) => {
  const [title, setTitle] = useState('')
  const [content, setContent] = useState('')
  const [recipients, setRecipients] = useState<string[]>(['all'])
  const [priority, setPriority] = useState<'normal' | 'urgent'>('normal')

  // Sample students data
  const students = [
    { id: 'all', name: 'All Students' },
    { id: 'abeeha', name: 'Abeeha' },
    { id: 'zunair', name: 'Zunair' },
    { id: 'affan', name: 'Affan' }
  ]

  const handleRecipientToggle = (studentId: string) => {
    if (studentId === 'all') {
      // If selecting "All Students", clear individual selections
      setRecipients(['all'])
    } else {
      // Remove "all" if it's selected, then toggle the specific student
      if (recipients.includes('all')) {
        setRecipients([studentId])
      } else {
        if (recipients.includes(studentId)) {
          setRecipients(recipients.filter(id => id !== studentId))
        } else {
          setRecipients([...recipients, studentId])
        }
      }
    }
  }

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault()

    // If "All Students" is selected, use all student IDs (except 'all')
    const finalRecipients = recipients.includes('all')
      ? students.filter(s => s.id !== 'all').map(s => s.id)
      : recipients

    onSendMessage({
      title,
      content,
      recipients: finalRecipients,
      priority
    })
  }

  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4">
      <div className="bg-white rounded-xl max-w-2xl w-full max-h-[90vh] overflow-y-auto">
        <div className="sticky top-0 bg-white border-b p-4 flex justify-between items-center z-10">
          <h2 className="text-xl font-bold text-gray-800">Send Message</h2>
          <button
            onClick={onClose}
            className="text-gray-500 hover:text-gray-700 text-2xl"
          >
            &times;
          </button>
        </div>

        <form onSubmit={handleSubmit} className="p-6">
          <div className="mb-6">
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Message Title
            </label>
            <input
              type="text"
              value={title}
              onChange={(e) => setTitle(e.target.value)}
              className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
              placeholder="e.g., Reminder about Reading Assignment"
              required
            />
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-6 mb-6">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Priority
              </label>
              <div className="space-y-2">
                <div className="flex items-center">
                  <input
                    type="radio"
                    id="normal"
                    name="priority"
                    checked={priority === 'normal'}
                    onChange={() => setPriority('normal')}
                    className="h-4 w-4 text-blue-600"
                  />
                  <label htmlFor="normal" className="ml-2 text-gray-700">
                    Normal
                  </label>
                </div>
                <div className="flex items-center">
                  <input
                    type="radio"
                    id="urgent"
                    name="priority"
                    checked={priority === 'urgent'}
                    onChange={() => setPriority('urgent')}
                    className="h-4 w-4 text-red-600"
                  />
                  <label htmlFor="urgent" className="ml-2 text-gray-700 text-red-600">
                    Urgent
                  </label>
                </div>
              </div>
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Send To
              </label>
              <div className="space-y-2 max-h-40 overflow-y-auto border border-gray-200 rounded-lg p-2">
                {students.map((student) => (
                  <div key={student.id} className="flex items-center">
                    <input
                      type="checkbox"
                      id={`recipient-${student.id}`}
                      checked={recipients.includes(student.id)}
                      onChange={() => handleRecipientToggle(student.id)}
                      className="h-4 w-4 text-blue-600 rounded focus:ring-blue-500"
                    />
                    <label htmlFor={`recipient-${student.id}`} className="ml-2 text-gray-700">
                      {student.name}
                    </label>
                  </div>
                ))}
              </div>
            </div>
          </div>

          <div className="mb-6">
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Message Content
            </label>
            <textarea
              value={content}
              onChange={(e) => setContent(e.target.value)}
              rows={5}
              className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
              placeholder="Type your message here..."
              required
            ></textarea>
          </div>

          <div className="flex justify-end space-x-3 pt-4">
            <button
              type="button"
              onClick={onClose}
              className="px-4 py-2 border border-gray-300 rounded-lg text-gray-700 hover:bg-gray-50"
            >
              Cancel
            </button>
            <button
              type="submit"
              className={`px-4 py-2 text-white rounded-lg ${
                priority === 'urgent'
                  ? 'bg-red-500 hover:bg-red-600'
                  : 'bg-blue-500 hover:bg-blue-600'
              }`}
            >
              Send Message
            </button>
          </div>
        </form>
      </div>
    </div>
  )
}

export default MessageModal