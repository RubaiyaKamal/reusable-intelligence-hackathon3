'use client'

import { useState } from 'react'
import StudentDashboard from './components/StudentDashboard'
import TeacherDashboard from './components/TeacherDashboard'

export default function Home() {
  const [userType, setUserType] = useState<'student' | 'teacher'>('student')

  return (
    <main className="min-h-screen bg-gradient-to-br from-purple-50 via-blue-50 to-pink-50">
      {/* Header */}
      <header className="bg-white shadow-sm border-b border-gray-200">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4">
          <div className="flex justify-between items-center">
            <div className="flex items-center space-x-3">
              <div className="text-3xl">📚</div>
              <div>
                <h1 className="text-2xl font-bold bg-gradient-to-r from-purple-600 to-blue-600 bg-clip-text text-transparent">
                  StoryForge
                </h1>
                <p className="text-sm text-gray-500">AI-Powered Reading Platform</p>
              </div>
            </div>

            <div className="flex items-center space-x-4">
              <div className="flex bg-gray-100 rounded-lg p-1">
                <button
                  onClick={() => setUserType('student')}
                  className={`px-4 py-2 rounded-md text-sm font-medium transition-colors ${
                    userType === 'student'
                      ? 'bg-white text-purple-600 shadow-sm'
                      : 'text-gray-600 hover:text-gray-900'
                  }`}
                >
                  Student View
                </button>
                <button
                  onClick={() => setUserType('teacher')}
                  className={`px-4 py-2 rounded-md text-sm font-medium transition-colors ${
                    userType === 'teacher'
                      ? 'bg-white text-blue-600 shadow-sm'
                      : 'text-gray-600 hover:text-gray-900'
                  }`}
                >
                  Teacher View
                </button>
              </div>

              <div className="flex items-center space-x-2">
                <div className="w-8 h-8 bg-gradient-to-br from-purple-500 to-blue-500 rounded-full flex items-center justify-center text-white text-sm font-semibold">
                  A
                </div>
              </div>
            </div>
          </div>
        </div>
      </header>

      {/* Main Content */}
      {userType === 'student' ? <StudentDashboard /> : <TeacherDashboard />}
    </main>
  )
}
