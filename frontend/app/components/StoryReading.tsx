'use client'

import { useState } from 'react'

interface StoryProps {
  onClose: () => void
}

interface StorySection {
  id: number
  title: string
  content: string
  imageUrl?: string
}

const StoryReading = ({ onClose }: StoryProps) => {
  const [currentSection, setCurrentSection] = useState(0)
  const [selectedStory, setSelectedStory] = useState<string | null>(null)
  const [generatedStory, setGeneratedStory] = useState<any>(null)
  const [isGenerating, setIsGenerating] = useState(false)
  const [error, setError] = useState<string | null>(null)

  // Story type options
  const storyTypes = [
    { id: 'adventure', name: 'Adventure Story', icon: '🗺️', description: 'Exciting journeys and discoveries' },
    { id: 'friendship', name: 'Friendship Story', icon: '👫', description: 'Stories about making friends' },
    { id: 'fantasy', name: 'Fantasy Story', icon: '🧙', description: 'Magical worlds and creatures' },
    { id: 'mystery', name: 'Mystery Story', icon: '🔍', description: 'Solving puzzles and mysteries' },
    { id: 'animal', name: 'Animal Story', icon: '🐾', description: 'Adventures with animals' },
    { id: 'science', name: 'Science Story', icon: '🔬', description: 'Learning through discovery' },
  ]

  const handleGenerateStory = async (storyType: string) => {
    setIsGenerating(true)
    setError(null)

    try {
      const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8001'
      const response = await fetch(`${API_URL}/api/v1/story/generate`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          story_type: storyType,
          reading_level: 50,
          length: 'medium',
          student_id: 'STU-001',
        }),
      })

      if (!response.ok) {
        throw new Error(`Failed to generate story: ${response.statusText}`)
      }

      const data = await response.json()

      if (data.success) {
        setGeneratedStory(data)
        setSelectedStory(storyType)
      } else {
        setError(data.error || 'Failed to generate story')
      }
    } catch (err: any) {
      console.error('Story generation error:', err)
      setError(err.message || 'Failed to connect to story generation service')
    } finally {
      setIsGenerating(false)
    }
  }

  const splitStoryIntoSections = (story: string, title: string): StorySection[] => {
    const paragraphs = story.split('\n\n').filter(p => p.trim().length > 0)
    return paragraphs.map((paragraph, index) => ({
      id: index + 1,
      title: index === 0 ? 'Beginning' : index === paragraphs.length - 1 ? 'Ending' : `Part ${index + 1}`,
      content: paragraph.trim(),
    }))
  }

  const storySections = generatedStory
    ? splitStoryIntoSections(generatedStory.story, generatedStory.title)
    : []

  return (
    <div className="fixed inset-0 bg-black/50 flex items-center justify-center z-50 p-4">
      <div className="bg-white rounded-xl shadow-2xl max-w-4xl w-full max-h-[90vh] overflow-y-auto">
        <div className="sticky top-0 bg-gradient-to-r from-indigo-500 to-purple-600 text-white p-6 flex justify-between items-center">
          <div>
            <h2 className="text-2xl font-bold">📖 Story Reading</h2>
            <p className="text-indigo-100 text-sm mt-1">AI-generated interactive stories</p>
          </div>
          <button
            onClick={onClose}
            className="text-white hover:text-gray-200 text-2xl"
          >
            &times;
          </button>
        </div>

        <div className="p-6">
          {!selectedStory ? (
            <div>
              <h3 className="text-lg font-semibold mb-4 text-gray-800">Choose a Story Type:</h3>
              {error && (
                <div className="mb-4 p-4 bg-red-50 border border-red-200 rounded-lg">
                  <p className="text-red-700 text-sm">
                    <strong>Error:</strong> {error}
                  </p>
                  <p className="text-red-600 text-xs mt-2">
                    Note: Make sure the backend server is running at http://localhost:8001
                  </p>
                </div>
              )}
              <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
                {storyTypes.map((type) => (
                  <button
                    key={type.id}
                    onClick={() => handleGenerateStory(type.id)}
                    disabled={isGenerating}
                    className="border-2 border-gray-200 rounded-lg p-4 hover:border-indigo-500 hover:bg-indigo-50 transition-all text-left disabled:opacity-50 disabled:cursor-not-allowed"
                  >
                    <div className="text-3xl mb-2">{type.icon}</div>
                    <h4 className="font-semibold text-gray-800">{type.name}</h4>
                    <p className="text-sm text-gray-600 mt-1">{type.description}</p>
                  </button>
                ))}
              </div>

              {isGenerating && (
                <div className="mt-6 text-center">
                  <div className="inline-block animate-spin rounded-full h-12 w-12 border-t-2 border-b-2 border-indigo-500 mb-3"></div>
                  <p className="text-gray-700 font-medium">🪄 Creating your story...</p>
                  <p className="text-gray-500 text-sm mt-1">This may take a few seconds</p>
                </div>
              )}
            </div>
          ) : (
            <div>
              {generatedStory && (
                <div className="mb-6">
                  <div className="flex items-center justify-between mb-4">
                    <div>
                      <h3 className="text-2xl font-bold text-gray-800">{generatedStory.title}</h3>
                      <div className="flex items-center space-x-4 mt-2 text-sm text-gray-600">
                        <span className="bg-indigo-100 text-indigo-700 px-3 py-1 rounded-full">
                          {generatedStory.story_type}
                        </span>
                        <span className="bg-purple-100 text-purple-700 px-3 py-1 rounded-full">
                          {generatedStory.reading_level} Level
                        </span>
                        <span className="bg-blue-100 text-blue-700 px-3 py-1 rounded-full">
                          {generatedStory.length}
                        </span>
                      </div>
                    </div>
                    <button
                      onClick={() => {
                        setSelectedStory(null)
                        setGeneratedStory(null)
                        setCurrentSection(0)
                      }}
                      className="text-indigo-600 hover:text-indigo-800 text-sm font-medium"
                    >
                      ← Choose Different Story
                    </button>
                  </div>

                  {/* Story Progress */}
                  <div className="mb-6">
                    <div className="flex items-center justify-between text-sm text-gray-600 mb-2">
                      <span>Section {currentSection + 1} of {storySections.length}</span>
                      <span>{Math.round(((currentSection + 1) / storySections.length) * 100)}% Complete</span>
                    </div>
                    <div className="bg-gray-200 rounded-full h-2">
                      <div
                        className="bg-gradient-to-r from-indigo-500 to-purple-600 rounded-full h-2 transition-all duration-300"
                        style={{ width: `${((currentSection + 1) / storySections.length) * 100}%` }}
                      />
                    </div>
                  </div>

                  {/* Story Content */}
                  <div className="bg-gradient-to-br from-yellow-50 to-amber-50 rounded-lg p-6 border-2 border-amber-200 mb-6">
                    <h4 className="text-lg font-semibold text-amber-900 mb-3">
                      {storySections[currentSection]?.title}
                    </h4>
                    <p className="text-gray-800 leading-relaxed text-lg">
                      {storySections[currentSection]?.content}
                    </p>
                  </div>

                  {/* Navigation Buttons */}
                  <div className="flex justify-between items-center">
                    <button
                      onClick={() => setCurrentSection(Math.max(0, currentSection - 1))}
                      disabled={currentSection === 0}
                      className="px-6 py-2 rounded-lg bg-gray-200 text-gray-700 hover:bg-gray-300 disabled:opacity-50 disabled:cursor-not-allowed font-medium"
                    >
                      ← Previous
                    </button>

                    {currentSection < storySections.length - 1 ? (
                      <button
                        onClick={() => setCurrentSection(currentSection + 1)}
                        className="px-6 py-2 rounded-lg bg-gradient-to-r from-indigo-500 to-purple-600 text-white hover:from-indigo-600 hover:to-purple-700 font-medium"
                      >
                        Next →
                      </button>
                    ) : (
                      <button
                        onClick={() => {
                          setSelectedStory(null)
                          setGeneratedStory(null)
                          setCurrentSection(0)
                        }}
                        className="px-6 py-2 rounded-lg bg-gradient-to-r from-green-500 to-emerald-600 text-white hover:from-green-600 hover:to-emerald-700 font-medium"
                      >
                        ✓ Finish Story
                      </button>
                    )}
                  </div>

                  {/* Vocabulary Words */}
                  {generatedStory.vocabulary_words && generatedStory.vocabulary_words.length > 0 && (
                    <div className="mt-6 p-4 bg-blue-50 rounded-lg border border-blue-200">
                      <h4 className="font-semibold text-blue-900 mb-2">📚 New Vocabulary Words:</h4>
                      <div className="flex flex-wrap gap-2">
                        {generatedStory.vocabulary_words.map((word: string, index: number) => (
                          <span
                            key={index}
                            className="bg-white text-blue-700 px-3 py-1 rounded-full text-sm border border-blue-300"
                          >
                            {word}
                          </span>
                        ))}
                      </div>
                    </div>
                  )}

                  {/* Story Metadata */}
                  {generatedStory.metadata && (
                    <div className="mt-4 p-4 bg-purple-50 rounded-lg border border-purple-200">
                      <div className="flex items-center justify-between text-sm text-purple-700">
                        <span>📊 Word Count: {generatedStory.metadata.word_count}</span>
                        <span>⏱️ Reading Time: {generatedStory.metadata.estimated_reading_time} min</span>
                      </div>
                    </div>
                  )}
                </div>
              )}
            </div>
          )}
        </div>
      </div>
    </div>
  )
}

export default StoryReading
