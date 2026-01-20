'use client'

import { useState } from 'react'

interface AssignmentModalProps {
  onClose: () => void
  onCreateAssignment: (assignment: {
    title: string
    type: string
    dueDate: string
    description: string
    assignedTo: string[]
  }) => void
}

const AssignmentModal = ({ onClose, onCreateAssignment }: AssignmentModalProps) => {
  const [title, setTitle] = useState('')
  const [type, setType] = useState('Story')
  const [dueDate, setDueDate] = useState('')
  const [description, setDescription] = useState('')
  const [assignedTo, setAssignedTo] = useState<string[]>(['all'])

  // Sample students data
  const students = [
    { id: 'all', name: 'All Students' },
    { id: 'abeeha', name: 'Abeeha' },
    { id: 'zunair', name: 'Zunair' },
    { id: 'affan', name: 'Affan' }
  ]

  const handleStudentToggle = (studentId: string) => {
    if (studentId === 'all') {
      // If selecting "All Students", clear individual selections
      setAssignedTo(['all'])
    } else {
      // Remove "all" if it's selected, then toggle the specific student
      if (assignedTo.includes('all')) {
        setAssignedTo([studentId])
      } else {
        if (assignedTo.includes(studentId)) {
          setAssignedTo(assignedTo.filter(id => id !== studentId))
        } else {
          setAssignedTo([...assignedTo, studentId])
        }
      }
    }
  }

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault()

    // If "All Students" is selected, use all student IDs (except 'all')
    const finalAssignedTo = assignedTo.includes('all')
      ? students.filter(s => s.id !== 'all').map(s => s.id)
      : assignedTo

    onCreateAssignment({
      title,
      type,
      dueDate,
      description,
      assignedTo: finalAssignedTo
    })
  }

  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4">
      <div className="bg-white rounded-xl max-w-2xl w-full max-h-[90vh] overflow-y-auto">
        <div className="sticky top-0 bg-white border-b p-4 flex justify-between items-center z-10">
          <h2 className="text-xl font-bold text-gray-800">Create Assignment</h2>
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
              Assignment Title
            </label>
            <input
              type="text"
              value={title}
              onChange={(e) => setTitle(e.target.value)}
              className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
              placeholder="e.g., Read 'The Magic Forest'"
              required
            />
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-6 mb-6">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Assignment Type
              </label>
              <select
                value={type}
                onChange={(e) => setType(e.target.value)}
                className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
              >
                <option value="Story">Story</option>
                <option value="Quiz">Quiz</option>
                <option value="Questions">Comprehension Questions</option>
                <option value="Writing">Creative Writing</option>
                <option value="Vocabulary">Vocabulary Exercise</option>
              </select>
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Due Date
              </label>
              <input
                type="date"
                value={dueDate}
                onChange={(e) => setDueDate(e.target.value)}
                className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                required
              />
            </div>
          </div>

          <div className="mb-6">
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Description
            </label>
            <textarea
              value={description}
              onChange={(e) => setDescription(e.target.value)}
              rows={3}
              className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
              placeholder="Describe the assignment requirements..."
            ></textarea>
          </div>

          <div className="mb-6">
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Assign To
            </label>
            <div className="space-y-2 max-h-40 overflow-y-auto border border-gray-200 rounded-lg p-2">
              {students.map((student) => (
                <div key={student.id} className="flex items-center">
                  <input
                    type="checkbox"
                    id={student.id}
                    checked={assignedTo.includes(student.id)}
                    onChange={() => handleStudentToggle(student.id)}
                    className="h-4 w-4 text-blue-600 rounded focus:ring-blue-500"
                  />
                  <label htmlFor={student.id} className="ml-2 text-gray-700">
                    {student.name}
                  </label>
                </div>
              ))}
            </div>
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
              className="px-4 py-2 bg-blue-500 text-white rounded-lg hover:bg-blue-600"
            >
              Create Assignment
            </button>
          </div>
        </form>
      </div>
    </div>
  )
}

export default AssignmentModal