'use client'

import { useState } from 'react'
import AssignmentModal from './AssignmentModal'
import MessageModal from './MessageModal'
import ReportModal from './ReportModal'

export default function TeacherDashboard() {
  const [selectedStudent, setSelectedStudent] = useState('all')
  const [showAssignmentModal, setShowAssignmentModal] = useState(false)
  const [showMessageModal, setShowMessageModal] = useState(false)
  const [showReportModal, setShowReportModal] = useState(false)

  const students = [
    {
      id: 'abeeha',
      name: 'Abeeha',
      avatar: 'A',
      level: 'Level 3',
      progress: 85,
      color: 'from-pink-400 to-pink-600',
      storiesCompleted: 15,
      avgScore: 87,
      lastActive: '2 hours ago',
    },
    {
      id: 'zunair',
      name: 'Zunair',
      avatar: 'Z',
      level: 'Level 4',
      progress: 92,
      color: 'from-blue-400 to-blue-600',
      storiesCompleted: 22,
      avgScore: 94,
      lastActive: '1 hour ago',
    },
    {
      id: 'affan',
      name: 'Affan',
      avatar: 'A',
      level: 'Level 2',
      progress: 68,
      color: 'from-green-400 to-green-600',
      storiesCompleted: 12,
      avgScore: 78,
      lastActive: '5 hours ago',
    },
  ]

  const classStats = {
    totalStudents: 3,
    assigned: 12,
    completed: 28,
    pending: 8,
    avgScore: 86,
  }

  const assignments = [
    {
      title: 'Read "The Enchanted Garden"',
      type: 'Story',
      dueDate: 'Jan 15, 2026',
      assigned: 3,
      completed: 2,
      pending: 1,
      avgScore: 88,
    },
    {
      title: 'Vocabulary Quiz - Animals',
      type: 'Quiz',
      dueDate: 'Jan 16, 2026',
      assigned: 3,
      completed: 3,
      pending: 0,
      avgScore: 92,
    },
    {
      title: 'Comprehension Questions Set 4',
      type: 'Questions',
      dueDate: 'Jan 18, 2026',
      assigned: 3,
      completed: 1,
      pending: 2,
      avgScore: 85,
    },
    {
      title: 'Creative Writing - My Adventure',
      type: 'Writing',
      dueDate: 'Jan 20, 2026',
      assigned: 3,
      completed: 0,
      pending: 3,
      avgScore: 0,
    },
  ]

  const recentActivity = [
    {
      student: 'Zunair',
      action: 'Completed vocabulary quiz',
      score: 5,
      time: '1 hour ago',
      icon: '✅',
    },
    {
      student: 'Abeeha',
      action: 'Started reading "The Magic Forest"',
      time: '2 hours ago',
      icon: '📖',
    },
    {
      student: 'Affan',
      action: 'Struggled with comprehension quiz',
      time: '5 hours ago',
      icon: '⚠️',
      needsHelp: true,
    },
    {
      student: 'Zunair',
      action: 'Achieved 7-day streak!',
      time: '1 day ago',
      icon: '🔥',
    },
  ]

  const selectedStudentData =
    selectedStudent === 'all'
      ? null
      : students.find((s) => s.id === selectedStudent)

  // Functions to handle actions
  const handleCreateAssignment = (assignment: {
    title: string
    type: string
    dueDate: string
    description: string
    assignedTo: string[]
  }) => {
    console.log('Creating assignment:', assignment)
    // In a real app, this would call an API to create the assignment
    alert(`Assignment "${assignment.title}" created successfully!`)
    setShowAssignmentModal(false)
  }

  const handleSendMessage = (message: {
    title: string
    content: string
    recipients: string[]
    priority: 'normal' | 'urgent'
  }) => {
    console.log('Sending message:', message)
    // In a real app, this would call an API to send the message
    alert(`Message "${message.title}" sent successfully!`)
    setShowMessageModal(false)
  }

  const handleExportReport = (report: {
    type: string
    format: string
    dateRange: { start: string; end: string }
    include: string[]
  }) => {
    console.log('Exporting report:', report)
    // In a real app, this would call an API to generate and download the report
    alert(`Report exported successfully as ${report.format.toUpperCase()}!`)
    setShowReportModal(false)
  }


  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      <div className="flex gap-6">
        {/* Left Sidebar - Students */}
        <aside className="w-64 flex-shrink-0">
          <div className="bg-white rounded-lg shadow-sm p-4">
            <h2 className="text-lg font-semibold text-gray-800 mb-4 flex items-center">
              <span className="text-xl mr-2">👥</span>
              All Students
            </h2>

            <button
              onClick={() => setSelectedStudent('all')}
              className={`w-full text-left px-3 py-2 rounded-lg mb-2 transition-colors ${
                selectedStudent === 'all'
                  ? 'bg-gradient-to-r from-purple-500 to-blue-500 text-white'
                  : 'hover:bg-gray-100 text-gray-700'
              }`}
            >
              <div className="font-medium">All Students</div>
              <div className="text-xs opacity-80">{students.length} students</div>
            </button>

            <div className="space-y-2 mt-4">
              {students.map((student) => (
                <button
                  key={student.id}
                  onClick={() => setSelectedStudent(student.id)}
                  className={`w-full text-left px-3 py-3 rounded-lg transition-colors ${
                    selectedStudent === student.id
                      ? 'bg-gradient-to-r ' + student.color + ' text-white shadow-md'
                      : 'hover:bg-gray-100 bg-gray-50'
                  }`}
                >
                  <div className="flex items-center space-x-3">
                    <div
                      className={`w-10 h-10 rounded-full flex items-center justify-center text-white font-bold ${
                        selectedStudent === student.id
                          ? 'bg-white/20'
                          : 'bg-gradient-to-br ' + student.color
                      }`}
                    >
                      {student.avatar}
                    </div>
                    <div className="flex-1">
                      <div className="font-medium">{student.name}</div>
                      <div className="text-xs opacity-75">{student.level}</div>
                    </div>
                  </div>
                  <div className="mt-2 bg-white/20 rounded-full h-1.5">
                    <div
                      className="bg-white rounded-full h-1.5 transition-all"
                      style={{ width: `${student.progress}%` }}
                    />
                  </div>
                </button>
              ))}
            </div>
          </div>

          <div className="bg-gradient-to-br from-yellow-50 to-yellow-100 rounded-lg shadow-sm p-4 mt-4 border border-yellow-200">
            <h3 className="text-sm font-semibold text-yellow-800 mb-2 flex items-center">
              <span className="mr-2">💡</span>
              Teaching Tip
            </h3>
            <p className="text-xs text-yellow-700">
              Encourage students to read daily. Affan needs extra support on comprehension skills.
            </p>
          </div>
        </aside>

        {/* Middle Section - Class Progress */}
        <main className="flex-1">
          {selectedStudent === 'all' ? (
            <>
              <div className="mb-6">
                <h2 className="text-2xl font-bold text-gray-800 mb-2">Class Progress Overview</h2>
                <p className="text-gray-600">Monitor your students reading journey</p>
              </div>

              {/* Stats Cards */}
              <div className="grid grid-cols-2 md:grid-cols-5 gap-4 mb-6">
                <div className="bg-white rounded-lg shadow-sm p-4 border-l-4 border-blue-500">
                  <div className="text-2xl font-bold text-blue-600">
                    {classStats.totalStudents}
                  </div>
                  <div className="text-xs text-gray-600 mt-1">Total Students</div>
                </div>

                <div className="bg-white rounded-lg shadow-sm p-4 border-l-4 border-purple-500">
                  <div className="text-2xl font-bold text-purple-600">{classStats.assigned}</div>
                  <div className="text-xs text-gray-600 mt-1">Assigned</div>
                </div>

                <div className="bg-white rounded-lg shadow-sm p-4 border-l-4 border-green-500">
                  <div className="text-2xl font-bold text-green-600">{classStats.completed}</div>
                  <div className="text-xs text-gray-600 mt-1">Completed</div>
                </div>

                <div className="bg-white rounded-lg shadow-sm p-4 border-l-4 border-orange-500">
                  <div className="text-2xl font-bold text-orange-600">{classStats.pending}</div>
                  <div className="text-xs text-gray-600 mt-1">Pending</div>
                </div>

                <div className="bg-white rounded-lg shadow-sm p-4 border-l-4 border-indigo-500">
                  <div className="text-2xl font-bold text-indigo-600">{classStats.avgScore}%</div>
                  <div className="text-xs text-gray-600 mt-1">Avg Score</div>
                </div>
              </div>

              {/* Student Performance Table */}
              <div className="bg-white rounded-lg shadow-sm overflow-hidden mb-6">
                <div className="p-4 bg-gradient-to-r from-purple-500 to-blue-500">
                  <h3 className="text-white font-semibold text-lg">Student Performance</h3>
                </div>
                <div className="overflow-x-auto">
                  <table className="w-full">
                    <thead className="bg-gray-50 border-b">
                      <tr>
                        <th className="px-4 py-3 text-left text-xs font-medium text-gray-600">
                          Student
                        </th>
                        <th className="px-4 py-3 text-left text-xs font-medium text-gray-600">
                          Level
                        </th>
                        <th className="px-4 py-3 text-left text-xs font-medium text-gray-600">
                          Stories Completed
                        </th>
                        <th className="px-4 py-3 text-left text-xs font-medium text-gray-600">
                          Avg Score
                        </th>
                        <th className="px-4 py-3 text-left text-xs font-medium text-gray-600">
                          Last Active
                        </th>
                        <th className="px-4 py-3 text-left text-xs font-medium text-gray-600">
                          Progress
                        </th>
                      </tr>
                    </thead>
                    <tbody className="divide-y divide-gray-200">
                      {students.map((student) => (
                        <tr key={student.id} className="hover:bg-gray-50">
                          <td className="px-4 py-3">
                            <div className="flex items-center space-x-3">
                              <div
                                className={`w-8 h-8 rounded-full bg-gradient-to-br ${student.color} flex items-center justify-center text-white text-sm font-bold`}
                              >
                                {student.avatar}
                              </div>
                              <span className="font-medium text-gray-800">{student.name}</span>
                            </div>
                          </td>
                          <td className="px-4 py-3 text-sm text-gray-600">{student.level}</td>
                          <td className="px-4 py-3 text-sm text-gray-600">
                            {student.storiesCompleted}
                          </td>
                          <td className="px-4 py-3">
                            <span className="font-semibold text-green-600">
                              {student.avgScore}%
                            </span>
                          </td>
                          <td className="px-4 py-3 text-sm text-gray-500">
                            {student.lastActive}
                          </td>
                          <td className="px-4 py-3">
                            <div className="w-24 bg-gray-200 rounded-full h-2">
                              <div
                                className={`bg-gradient-to-r ${student.color} h-2 rounded-full`}
                                style={{ width: `${student.progress}%` }}
                              />
                            </div>
                          </td>
                        </tr>
                      ))}
                    </tbody>
                  </table>
                </div>
              </div>

              {/* Assignments Overview */}
              <div className="bg-white rounded-lg shadow-sm overflow-hidden">
                <div className="p-4 bg-gradient-to-r from-indigo-500 to-purple-500">
                  <h3 className="text-white font-semibold text-lg">Assignments Overview</h3>
                </div>
                <div className="p-4">
                  <div className="space-y-3">
                    {assignments.map((assignment, index) => (
                      <div
                        key={index}
                        className="border border-gray-200 rounded-lg p-4 hover:shadow-md transition-shadow"
                      >
                        <div className="flex items-center justify-between mb-2">
                          <div>
                            <h4 className="font-semibold text-gray-800">{assignment.title}</h4>
                            <div className="flex items-center space-x-3 mt-1">
                              <span className="text-xs bg-purple-100 text-purple-700 px-2 py-1 rounded">
                                {assignment.type}
                              </span>
                              <span className="text-xs text-gray-500">
                                Due: {assignment.dueDate}
                              </span>
                            </div>
                          </div>
                          {assignment.avgScore > 0 && (
                            <div className="text-right">
                              <div className="text-2xl font-bold text-green-600">
                                {assignment.avgScore}%
                              </div>
                              <div className="text-xs text-gray-500">Avg Score</div>
                            </div>
                          )}
                        </div>
                        <div className="grid grid-cols-3 gap-2 mt-3">
                          <div className="bg-blue-50 rounded p-2 text-center">
                            <div className="font-bold text-blue-600">{assignment.assigned}</div>
                            <div className="text-xs text-blue-700">Assigned</div>
                          </div>
                          <div className="bg-green-50 rounded p-2 text-center">
                            <div className="font-bold text-green-600">{assignment.completed}</div>
                            <div className="text-xs text-green-700">Completed</div>
                          </div>
                          <div className="bg-orange-50 rounded p-2 text-center">
                            <div className="font-bold text-orange-600">{assignment.pending}</div>
                            <div className="text-xs text-orange-700">Pending</div>
                          </div>
                        </div>
                      </div>
                    ))}
                  </div>
                </div>
              </div>
            </>
          ) : (
            <>
              {/* Individual Student View */}
              {selectedStudentData && (
                <>
                  <div className="mb-6">
                    <div className="flex items-center space-x-4">
                      <div
                        className={`w-16 h-16 rounded-full bg-gradient-to-br ${selectedStudentData.color} flex items-center justify-center text-white text-2xl font-bold`}
                      >
                        {selectedStudentData.avatar}
                      </div>
                      <div>
                        <h2 className="text-2xl font-bold text-gray-800">
                          {selectedStudentData.name}&apos;s Progress
                        </h2>
                        <p className="text-gray-600">
                          {selectedStudentData.level} • {selectedStudentData.progress}% Complete
                        </p>
                      </div>
                    </div>
                  </div>

                  <div className="grid grid-cols-3 gap-4 mb-6">
                    <div className="bg-white rounded-lg shadow-sm p-4">
                      <div className="text-3xl font-bold text-purple-600">
                        {selectedStudentData.storiesCompleted}
                      </div>
                      <div className="text-sm text-gray-600">Stories Completed</div>
                    </div>
                    <div className="bg-white rounded-lg shadow-sm p-4">
                      <div className="text-3xl font-bold text-green-600">
                        {selectedStudentData.avgScore}%
                      </div>
                      <div className="text-sm text-gray-600">Average Score</div>
                    </div>
                    <div className="bg-white rounded-lg shadow-sm p-4">
                      <div className="text-3xl font-bold text-blue-600">
                        {selectedStudentData.progress}%
                      </div>
                      <div className="text-sm text-gray-600">Overall Progress</div>
                    </div>
                  </div>

                  <div className="bg-white rounded-lg shadow-sm p-6">
                    <h3 className="font-semibold text-gray-800 mb-4">Recent Activity</h3>
                    <div className="space-y-3">
                      {recentActivity
                        .filter((a) => a.student === selectedStudentData.name)
                        .map((activity, index) => (
                          <div
                            key={index}
                            className={`p-3 rounded-lg ${
                              activity.needsHelp ? 'bg-red-50 border border-red-200' : 'bg-gray-50'
                            }`}
                          >
                            <div className="flex items-center justify-between">
                              <div className="flex items-center space-x-3">
                                <span className="text-2xl">{activity.icon}</span>
                                <div>
                                  <div className="font-medium text-gray-800">
                                    {activity.action}
                                  </div>
                                  <div className="text-xs text-gray-500">{activity.time}</div>
                                </div>
                              </div>
                              {activity.score && (
                                <span className="font-bold text-green-600">{activity.score}/5</span>
                              )}
                            </div>
                          </div>
                        ))}
                    </div>
                  </div>
                </>
              )}
            </>
          )}
        </main>

        {/* Right Sidebar - Details */}
        <aside className="w-80 flex-shrink-0">
          <div className="bg-white rounded-lg shadow-sm p-4 mb-4">
            <h3 className="font-semibold text-gray-800 mb-4 flex items-center">
              <span className="mr-2">📊</span>
              Quick Stats
            </h3>
            <div className="space-y-3">
              <div className="flex items-center justify-between p-2 bg-green-50 rounded">
                <span className="text-sm text-gray-700">This Week</span>
                <span className="font-bold text-green-600">18 completions</span>
              </div>
              <div className="flex items-center justify-between p-2 bg-blue-50 rounded">
                <span className="text-sm text-gray-700">Active Now</span>
                <span className="font-bold text-blue-600">2 students</span>
              </div>
              <div className="flex items-center justify-between p-2 bg-purple-50 rounded">
                <span className="text-sm text-gray-700">Needs Help</span>
                <span className="font-bold text-purple-600">1 student</span>
              </div>
            </div>
          </div>

          <div className="bg-white rounded-lg shadow-sm p-4 mb-4">
            <h3 className="font-semibold text-gray-800 mb-4 flex items-center">
              <span className="mr-2">🎯</span>
              Upcoming Deadlines
            </h3>
            <div className="space-y-3">
              <div className="border-l-4 border-red-500 pl-3 py-1">
                <div className="font-medium text-sm text-gray-800">Vocabulary Quiz</div>
                <div className="text-xs text-red-600">Tomorrow</div>
              </div>
              <div className="border-l-4 border-orange-500 pl-3 py-1">
                <div className="font-medium text-sm text-gray-800">Comprehension Questions</div>
                <div className="text-xs text-orange-600">Jan 18</div>
              </div>
              <div className="border-l-4 border-yellow-500 pl-3 py-1">
                <div className="font-medium text-sm text-gray-800">Creative Writing</div>
                <div className="text-xs text-yellow-600">Jan 20</div>
              </div>
            </div>
          </div>

          <div className="bg-white rounded-lg shadow-sm p-4 mb-4">
            <h3 className="font-semibold text-gray-800 mb-4 flex items-center">
              <span className="mr-2">🔔</span>
              Recent Activity
            </h3>
            <div className="space-y-3">
              {recentActivity.map((activity, index) => (
                <div
                  key={index}
                  className={`p-2 rounded text-xs ${
                    activity.needsHelp ? 'bg-red-50 text-red-700' : 'bg-gray-50 text-gray-700'
                  }`}
                >
                  <div className="font-medium">
                    {activity.icon} {activity.student}
                  </div>
                  <div className="opacity-75 mt-1">{activity.action}</div>
                  <div className="opacity-50 mt-1">{activity.time}</div>
                </div>
              ))}
            </div>
          </div>

          <div className="bg-gradient-to-br from-purple-500 to-blue-500 rounded-lg shadow-lg p-4 text-white">
            <h3 className="font-semibold mb-2">Actions</h3>
            <div className="space-y-2">
              <button
                onClick={() => setShowAssignmentModal(true)}
                className="w-full bg-white/20 hover:bg-white/30 px-4 py-2 rounded text-sm font-medium transition-colors"
              >
                Create Assignment
              </button>
              <button
                onClick={() => setShowMessageModal(true)}
                className="w-full bg-white/20 hover:bg-white/30 px-4 py-2 rounded text-sm font-medium transition-colors"
              >
                Send Message
              </button>
              <button
                onClick={() => setShowReportModal(true)}
                className="w-full bg-white/20 hover:bg-white/30 px-4 py-2 rounded text-sm font-medium transition-colors"
              >
                Export Report
              </button>
            </div>
          </div>
        </aside>
      </div>

      {/* Modal Components */}
      {showAssignmentModal && (
        <AssignmentModal
          onClose={() => setShowAssignmentModal(false)}
          onCreateAssignment={handleCreateAssignment}
        />
      )}

      {showMessageModal && (
        <MessageModal
          onClose={() => setShowMessageModal(false)}
          onSendMessage={handleSendMessage}
        />
      )}

      {showReportModal && (
        <ReportModal
          onClose={() => setShowReportModal(false)}
          onExportReport={handleExportReport}
        />
      )}
    </div>
  )
}
