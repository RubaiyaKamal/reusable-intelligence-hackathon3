'use client'

import { useState } from 'react'

interface ProgressReviewProps {
  onClose: () => void
}

interface ProgressData {
  readingComprehension: number
  vocabulary: number
  storyCompletion: number
  creativeWriting: number
  totalStoriesRead: number
  dayStreak: number
  achievements: number
  weeklyProgress: Array<{day: string, progress: number}>
  monthlyGoals: Array<{goal: string, completed: boolean}>
  readingTime: {hours: number, minutes: number}
}

const ProgressReview = ({ onClose }: ProgressReviewProps) => {
  const [activeTab, setActiveTab] = useState('overview')

  // Sample progress data
  const progressData: ProgressData = {
    readingComprehension: 85,
    vocabulary: 78,
    storyCompletion: 92,
    creativeWriting: 65,
    totalStoriesRead: 12,
    dayStreak: 7,
    achievements: 8,
    weeklyProgress: [
      { day: 'Mon', progress: 60 },
      { day: 'Tue', progress: 75 },
      { day: 'Wed', progress: 40 },
      { day: 'Thu', progress: 90 },
      { day: 'Fri', progress: 80 },
      { day: 'Sat', progress: 100 },
      { day: 'Sun', progress: 70 }
    ],
    monthlyGoals: [
      { goal: 'Read 10 stories', completed: true },
      { goal: 'Complete 5 vocabulary quizzes', completed: true },
      { goal: 'Write 2 creative stories', completed: false },
      { goal: 'Achieve 80% comprehension average', completed: true },
      { goal: 'Maintain 5-day reading streak', completed: true }
    ],
    readingTime: { hours: 3, minutes: 45 }
  }

  const renderOverview = () => (
    <div>
      <h3 className="text-lg font-semibold text-gray-800 mb-4">Your Reading Progress</h3>

      <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-6">
        <div className="bg-gradient-to-r from-purple-50 to-purple-100 rounded-lg p-4 border border-purple-200">
          <div className="text-2xl font-bold text-purple-600">{progressData.readingComprehension}%</div>
          <div className="text-xs text-purple-700">Comprehension</div>
        </div>

        <div className="bg-gradient-to-r from-blue-50 to-blue-100 rounded-lg p-4 border border-blue-200">
          <div className="text-2xl font-bold text-blue-600">{progressData.vocabulary}%</div>
          <div className="text-xs text-blue-700">Vocabulary</div>
        </div>

        <div className="bg-gradient-to-r from-green-50 to-green-100 rounded-lg p-4 border border-green-200">
          <div className="text-2xl font-bold text-green-600">{progressData.storyCompletion}%</div>
          <div className="text-xs text-green-700">Stories</div>
        </div>

        <div className="bg-gradient-to-r from-pink-50 to-pink-100 rounded-lg p-4 border border-pink-200">
          <div className="text-2xl font-bold text-pink-600">{progressData.creativeWriting}%</div>
          <div className="text-xs text-pink-700">Writing</div>
        </div>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-6 mb-6">
        <div className="bg-white border rounded-lg p-4">
          <h4 className="font-semibold text-gray-800 mb-3">Weekly Progress</h4>
          <div className="flex items-end justify-between h-32">
            {progressData.weeklyProgress.map((day, index) => (
              <div key={index} className="flex flex-col items-center">
                <div
                  className="w-8 bg-gradient-to-t from-blue-500 to-blue-300 rounded-t"
                  style={{ height: `${day.progress}%` }}
                ></div>
                <div className="text-xs text-gray-600 mt-2">{day.day}</div>
              </div>
            ))}
          </div>
        </div>

        <div className="bg-white border rounded-lg p-4">
          <h4 className="font-semibold text-gray-800 mb-3">Reading Stats</h4>
          <div className="space-y-3">
            <div className="flex justify-between">
              <span className="text-gray-600">Total Stories Read:</span>
              <span className="font-medium">{progressData.totalStoriesRead}</span>
            </div>
            <div className="flex justify-between">
              <span className="text-gray-600">Day Streak:</span>
              <span className="font-medium">{progressData.dayStreak} 🔥</span>
            </div>
            <div className="flex justify-between">
              <span className="text-gray-600">Reading Time:</span>
              <span className="font-medium">{progressData.readingTime.hours}h {progressData.readingTime.minutes}m</span>
            </div>
            <div className="flex justify-between">
              <span className="text-gray-600">Achievements:</span>
              <span className="font-medium">{progressData.achievements} 🏆</span>
            </div>
          </div>
        </div>
      </div>
    </div>
  )

  const renderGoals = () => (
    <div>
      <h3 className="text-lg font-semibold text-gray-800 mb-4">Monthly Goals</h3>

      <div className="space-y-3">
        {progressData.monthlyGoals.map((goal, index) => (
          <div
            key={index}
            className={`flex items-center justify-between p-3 rounded-lg border ${
              goal.completed
                ? 'bg-green-50 border-green-200'
                : 'bg-yellow-50 border-yellow-200'
            }`}
          >
            <div className="flex items-center">
              <div className={`w-6 h-6 rounded-full flex items-center justify-center mr-3 ${
                goal.completed
                  ? 'bg-green-500 text-white'
                  : 'bg-yellow-500 text-white'
              }`}>
                {goal.completed ? '✓' : index + 1}
              </div>
              <span className={`${goal.completed ? 'text-green-800' : 'text-yellow-800'}`}>
                {goal.goal}
              </span>
            </div>
            <div className={`px-3 py-1 rounded-full text-xs font-medium ${
              goal.completed
                ? 'bg-green-100 text-green-800'
                : 'bg-yellow-100 text-yellow-800'
            }`}>
              {goal.completed ? 'Completed' : 'In Progress'}
            </div>
          </div>
        ))}
      </div>
    </div>
  )

  const renderAchievements = () => (
    <div>
      <h3 className="text-lg font-semibold text-gray-800 mb-4">Your Achievements</h3>

      <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
        {[1, 2, 3, 4, 5, 6, 7, 8].map((achievement) => (
          <div key={achievement} className="bg-gradient-to-br from-yellow-100 to-yellow-50 border border-yellow-200 rounded-lg p-4 text-center">
            <div className="text-3xl mb-2">🏆</div>
            <div className="text-sm font-medium text-yellow-800">Achievement {achievement}</div>
            <div className="text-xs text-yellow-600 mt-1">Badge earned</div>
          </div>
        ))}
      </div>
    </div>
  )

  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4">
      <div className="bg-white rounded-xl max-w-4xl w-full max-h-[90vh] overflow-y-auto">
        <div className="sticky top-0 bg-white border-b p-4 flex justify-between items-center z-10">
          <h2 className="text-xl font-bold text-gray-800">Review Progress</h2>
          <button
            onClick={onClose}
            className="text-gray-500 hover:text-gray-700 text-2xl"
          >
            &times;
          </button>
        </div>

        <div className="p-6">
          <div className="border-b border-gray-200 mb-6">
            <nav className="flex space-x-8">
              <button
                onClick={() => setActiveTab('overview')}
                className={`pb-3 px-1 font-medium text-sm ${
                  activeTab === 'overview'
                    ? 'border-b-2 border-indigo-500 text-indigo-600'
                    : 'text-gray-500 hover:text-gray-700'
                }`}
              >
                Overview
              </button>
              <button
                onClick={() => setActiveTab('goals')}
                className={`pb-3 px-1 font-medium text-sm ${
                  activeTab === 'goals'
                    ? 'border-b-2 border-indigo-500 text-indigo-600'
                    : 'text-gray-500 hover:text-gray-700'
                }`}
              >
                Goals
              </button>
              <button
                onClick={() => setActiveTab('achievements')}
                className={`pb-3 px-1 font-medium text-sm ${
                  activeTab === 'achievements'
                    ? 'border-b-2 border-indigo-500 text-indigo-600'
                    : 'text-gray-500 hover:text-gray-700'
                }`}
              >
                Achievements
              </button>
            </nav>
          </div>

          {activeTab === 'overview' && renderOverview()}
          {activeTab === 'goals' && renderGoals()}
          {activeTab === 'achievements' && renderAchievements()}
        </div>
      </div>
    </div>
  )
}

export default ProgressReview