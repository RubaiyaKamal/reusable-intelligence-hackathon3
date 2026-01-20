'use client'

import { useState } from 'react'
import StoryReading from './StoryReading'
import QuizInterface from './QuizInterface'
import ProgressReview from './ProgressReview'

export default function StudentDashboard() {
  const [selectedStory, setSelectedStory] = useState<number | null>(null)
  const [showStoryModal, setShowStoryModal] = useState(false)
  const [showQuizModal, setShowQuizModal] = useState(false)
  const [showProgressModal, setShowProgressModal] = useState(false)

  const stats = {
    completed: 12,
    dayStreak: 7,
    currentLevel: 'Level 3',
    achievements: 8,
  }

  const stories = [
    {
      id: 1,
      title: 'Reading Basics',
      level: 'Level 1',
      progress: 100,
      icon: '📖',
      color: 'from-green-200 to-green-300',
      quizzes: [
        { title: 'Letters and Sounds', completed: true, score: 5 },
        { title: 'Simple Words', completed: true, score: 4 },
        { title: 'Short Sentences', completed: true, score: 5 },
        { title: 'Story Time', completed: true, score: 5 },
        { title: 'Reading Practice', completed: true, score: 4 },
      ],
    },
    {
      id: 2,
      title: 'Vocabulary Building',
      level: 'Level 2',
      progress: 75,
      icon: '📝',
      color: 'from-blue-200 to-blue-300',
      quizzes: [
        { title: 'Common Words', completed: true, score: 5 },
        { title: 'Action Words', completed: true, score: 4 },
        { title: 'Describing Words', completed: true, score: 5 },
        { title: 'Synonyms & Antonyms', completed: false, score: 0 },
        { title: 'Word Families', completed: false, score: 0 },
      ],
    },
    {
      id: 3,
      title: 'Story Comprehension',
      level: 'Level 3',
      progress: 40,
      icon: '🧠',
      color: 'from-purple-200 to-purple-300',
      quizzes: [
        { title: 'Main Ideas', completed: true, score: 4 },
        { title: 'Character Analysis', completed: true, score: 3 },
        { title: 'Plot Understanding', completed: false, score: 0 },
        { title: 'Theme Recognition', completed: false, score: 0 },
        { title: 'Making Predictions', completed: false, score: 0 },
      ],
    },
    {
      id: 4,
      title: 'Creative Writing',
      level: 'Level 4',
      progress: 0,
      icon: '✍️',
      color: 'from-pink-200 to-pink-300',
      quizzes: [
        { title: 'Story Starters', completed: false, score: 0 },
        { title: 'Character Creation', completed: false, score: 0 },
        { title: 'Plot Development', completed: false, score: 0 },
        { title: 'Descriptive Writing', completed: false, score: 0 },
        { title: 'Story Endings', completed: false, score: 0 },
      ],
    },
  ]

  const assignments = [
    { title: 'Read "The Magic Forest" story', due: 'Today', status: 'pending' },
    { title: 'Complete vocabulary quiz', due: 'Tomorrow', status: 'pending' },
    { title: 'Answer comprehension questions', due: 'This Week', status: 'completed' },
  ]

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      <div className="flex gap-6">
        {/* Left Sidebar */}
        <aside className="w-64 flex-shrink-0">
          <div className="bg-white rounded-lg shadow-sm p-4 mb-4">
            <h2 className="text-lg font-semibold text-gray-800 mb-4 flex items-center">
              <span className="text-xl mr-2">📊</span>
              My Progress
            </h2>

            <div className="space-y-3">
              <div className="bg-gradient-to-r from-green-50 to-green-100 rounded-lg p-3 border border-green-200">
                <div className="text-2xl font-bold text-green-600">{stats.completed}</div>
                <div className="text-xs text-green-700">Stories Completed</div>
              </div>

              <div className="bg-gradient-to-r from-orange-50 to-orange-100 rounded-lg p-3 border border-orange-200">
                <div className="text-2xl font-bold text-orange-600">{stats.dayStreak} 🔥</div>
                <div className="text-xs text-orange-700">Day Streak</div>
              </div>

              <div className="bg-gradient-to-r from-blue-50 to-blue-100 rounded-lg p-3 border border-blue-200">
                <div className="text-2xl font-bold text-blue-600">{stats.currentLevel}</div>
                <div className="text-xs text-blue-700">Current Level</div>
              </div>

              <div className="bg-gradient-to-r from-purple-50 to-purple-100 rounded-lg p-3 border border-purple-200">
                <div className="text-2xl font-bold text-purple-600">{stats.achievements} 🏆</div>
                <div className="text-xs text-purple-700">Achievements</div>
              </div>
            </div>
          </div>

          <div className="bg-gradient-to-br from-yellow-50 to-yellow-100 rounded-lg shadow-sm p-4 mb-4 border border-yellow-200">
            <h3 className="text-sm font-semibold text-yellow-800 mb-2 flex items-center">
              <span className="mr-2">💡</span>
              Tip of the Day
            </h3>
            <p className="text-xs text-yellow-700">
              Read for 20 minutes daily to improve your vocabulary by 10 new words per week!
            </p>
          </div>

          <div className="bg-white rounded-lg shadow-sm p-4">
            <h3 className="text-sm font-semibold text-gray-800 mb-3 flex items-center">
              <span className="mr-2">📋</span>
              Your Assignments
            </h3>
            <div className="space-y-2">
              {assignments.map((assignment, index) => (
                <div
                  key={index}
                  className={`text-xs p-2 rounded border ${
                    assignment.status === 'completed'
                      ? 'bg-green-50 border-green-200 text-green-700'
                      : 'bg-gray-50 border-gray-200 text-gray-700'
                  }`}
                >
                  <div className="font-medium">{assignment.title}</div>
                  <div className="text-gray-500 mt-1">{assignment.due}</div>
                </div>
              ))}
            </div>
          </div>
        </aside>

        {/* Middle Section */}
        <main className="flex-1">
          <div className="mb-6">
            <h2 className="text-2xl font-bold text-gray-800 mb-2">Your Reading Journey</h2>
            <p className="text-gray-600">Continue learning and unlock new stories!</p>
          </div>

          {/* Story Modules */}
          <div className="space-y-4">
            {stories.map((story) => (
              <div key={story.id} className="bg-white rounded-lg shadow-sm overflow-hidden">
                <div
                  className={`bg-gradient-to-r ${story.color} p-4 cursor-pointer`}
                  onClick={() => setSelectedStory(selectedStory === story.id ? null : story.id)}
                >
                  <div className="flex items-center justify-between">
                    <div className="flex items-center space-x-3">
                      <span className="text-3xl">{story.icon}</span>
                      <div>
                        <h3 className="text-white font-semibold text-lg">{story.title}</h3>
                        <p className="text-white/80 text-sm">{story.level}</p>
                      </div>
                    </div>
                    <div className="text-right">
                      <div className="text-white font-bold text-2xl">{story.progress}%</div>
                      <div className="text-white/80 text-xs">Complete</div>
                    </div>
                  </div>
                  <div className="mt-3 bg-white/20 rounded-full h-2">
                    <div
                      className="bg-white rounded-full h-2 transition-all duration-300"
                      style={{ width: `${story.progress}%` }}
                    />
                  </div>
                </div>

                {selectedStory === story.id && (
                  <div className="p-4 bg-gray-50">
                    <h4 className="font-semibold text-gray-800 mb-3">Quizzes (MCQs - 5 each)</h4>
                    <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
                      {story.quizzes.map((quiz, index) => (
                        <div
                          key={index}
                          className={`p-3 rounded-lg border ${
                            quiz.completed
                              ? 'bg-green-50 border-green-200'
                              : 'bg-white border-gray-200'
                          }`}
                        >
                          <div className="flex items-center justify-between">
                            <div className="flex items-center space-x-2">
                              <span className="text-lg">
                                {quiz.completed ? '✅' : '⭕'}
                              </span>
                              <span className="text-sm font-medium text-gray-800">
                                {quiz.title}
                              </span>
                            </div>
                            {quiz.completed && (
                              <span className="text-xs font-semibold text-green-600">
                                {quiz.score}/5
                              </span>
                            )}
                          </div>
                        </div>
                      ))}
                    </div>
                  </div>
                )}
              </div>
            ))}
          </div>

          {/* Mastery Breakdown */}
          <div className="mt-6 bg-white rounded-lg shadow-sm p-6">
            <h3 className="text-lg font-semibold text-gray-800 mb-4 flex items-center">
              <span className="mr-2">📈</span>
              Mastery Breakdown
            </h3>
            <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
              <div className="text-center">
                <div className="text-3xl font-bold text-purple-500">85%</div>
                <div className="text-xs text-gray-600 mt-1">Reading Comprehension</div>
              </div>
              <div className="text-center">
                <div className="text-3xl font-bold text-blue-500">78%</div>
                <div className="text-xs text-gray-600 mt-1">Vocabulary</div>
              </div>
              <div className="text-center">
                <div className="text-3xl font-bold text-green-500">92%</div>
                <div className="text-xs text-gray-600 mt-1">Story Completion</div>
              </div>
              <div className="text-center">
                <div className="text-3xl font-bold text-pink-500">65%</div>
                <div className="text-xs text-gray-600 mt-1">Creative Writing</div>
              </div>
            </div>
          </div>

          {/* Interactive Story Section */}
          <div className="mt-6 bg-gradient-to-r from-indigo-300 to-purple-400 rounded-lg shadow-lg p-6 text-white">
            <h3 className="text-xl font-bold mb-2">📖 Start Reading Now!</h3>
            <p className="text-white/90 mb-4">
              Dive into an exciting adventure story or practice your vocabulary with fun exercises.
            </p>
            <div className="flex space-x-3">
              <button
                onClick={() => setShowStoryModal(true)}
                className="bg-white text-indigo-600 px-6 py-2 rounded-lg font-semibold hover:bg-gray-100 transition-colors"
              >
                Read Story
              </button>
              <button
                onClick={() => setShowQuizModal(true)}
                className="bg-indigo-200 text-indigo-700 px-6 py-2 rounded-lg font-semibold hover:bg-indigo-300 transition-colors"
              >
                Practice Quiz
              </button>
              <button
                onClick={() => setShowProgressModal(true)}
                className="bg-purple-200 text-purple-700 px-6 py-2 rounded-lg font-semibold hover:bg-purple-300 transition-colors"
              >
                Review Progress
              </button>
            </div>
          </div>
        </main>
      </div>

      {/* Modal Components */}
      {showStoryModal && (
        <StoryReading onClose={() => setShowStoryModal(false)} />
      )}

      {showQuizModal && (
        <QuizInterface onClose={() => setShowQuizModal(false)} />
      )}

      {showProgressModal && (
        <ProgressReview onClose={() => setShowProgressModal(false)} />
      )}
    </div>
  )
}
