'use client'

import { useState, useEffect } from 'react'

interface QuizInterfaceProps {
  onClose: () => void
}

interface Question {
  id: number
  text: string
  options: string[]
  correctAnswer: number
}

interface QuizTopic {
  id: number
  title: string
  questions: Question[]
}

const QuizInterface = ({ onClose }: QuizInterfaceProps) => {
  const [selectedTopic, setSelectedTopic] = useState<string | null>(null)
  const [currentQuestionIndex, setCurrentQuestionIndex] = useState(0)
  const [selectedAnswers, setSelectedAnswers] = useState<{[key: number]: number}>({})
  const [showResults, setShowResults] = useState(false)
  const [score, setScore] = useState(0)

  // Sample quiz topics with 5 questions each
  const quizTopics: QuizTopic[] = [
    {
      id: 1,
      title: 'Reading Comprehension',
      questions: [
        {
          id: 1,
          text: 'What was the main character\'s name in the story?',
          options: ['Tom', 'Luna', 'Sarah', 'Mike'],
          correctAnswer: 1
        },
        {
          id: 2,
          text: 'Where did the story take place?',
          options: ['In a city', 'On a farm', 'In a magic forest', 'At school'],
          correctAnswer: 2
        },
        {
          id: 3,
          text: 'What did the main character find?',
          options: ['A treasure map', 'A glowing flower', 'A lost pet', 'A magic wand'],
          correctAnswer: 1
        },
        {
          id: 4,
          text: 'How did the story end?',
          options: ['With sadness', 'With a celebration', 'With a mystery', 'With a challenge'],
          correctAnswer: 1
        },
        {
          id: 5,
          text: 'What lesson did the characters learn?',
          options: ['Teamwork makes everything easier', 'Always listen to parents', 'Friendship is precious', 'Hard work pays off'],
          correctAnswer: 2
        }
      ]
    },
    {
      id: 2,
      title: 'Vocabulary Building',
      questions: [
        {
          id: 1,
          text: 'What does "curious" mean?',
          options: ['Angry', 'Sleepy', 'Interested in learning', 'Tired'],
          correctAnswer: 2
        },
        {
          id: 2,
          text: 'Which word means the opposite of "happy"?',
          options: ['Joyful', 'Cheerful', 'Glad', 'Sad'],
          correctAnswer: 3
        },
        {
          id: 3,
          text: 'What is another word for "beautiful"?',
          options: ['Ugly', 'Pretty', 'Large', 'Old'],
          correctAnswer: 1
        },
        {
          id: 4,
          text: 'Which word describes something that gives light?',
          options: ['Dark', 'Cold', 'Bright', 'Heavy'],
          correctAnswer: 2
        },
        {
          id: 5,
          text: 'What does "enormous" mean?',
          options: ['Very small', 'Medium size', 'Very large', 'Average'],
          correctAnswer: 2
        }
      ]
    },
    {
      id: 3,
      title: 'Story Elements',
      questions: [
        {
          id: 1,
          text: 'What is the setting of a story?',
          options: ['The main character', 'The time and place', 'The problem', 'The solution'],
          correctAnswer: 1
        },
        {
          id: 2,
          text: 'Who is the protagonist?',
          options: ['The bad guy', 'The main character', 'The narrator', 'The teacher'],
          correctAnswer: 1
        },
        {
          id: 3,
          text: 'What is the climax of a story?',
          options: ['The beginning', 'The most exciting part', 'The ending', 'The middle'],
          correctAnswer: 1
        },
        {
          id: 4,
          text: 'What does plot refer to?',
          options: ['The author', 'The main idea', 'The sequence of events', 'The title'],
          correctAnswer: 2
        },
        {
          id: 5,
          text: 'What is the theme of a story?',
          options: ['The main lesson', 'The place', 'The time', 'The characters'],
          correctAnswer: 0
        }
      ]
    }
  ]

  const currentTopic = quizTopics.find(topic => topic.title === selectedTopic)
  const currentQuestion = currentTopic?.questions[currentQuestionIndex]

  const handleAnswerSelect = (optionIndex: number) => {
    if (!currentQuestion) return

    setSelectedAnswers({
      ...selectedAnswers,
      [currentQuestion.id]: optionIndex
    })
  }

  const handleNextQuestion = () => {
    if (currentQuestionIndex < 4) {
      setCurrentQuestionIndex(currentQuestionIndex + 1)
    } else {
      calculateScore()
      setShowResults(true)
    }
  }

  const handlePreviousQuestion = () => {
    if (currentQuestionIndex > 0) {
      setCurrentQuestionIndex(currentQuestionIndex - 1)
    }
  }

  const calculateScore = () => {
    if (!currentTopic) return

    let calculatedScore = 0
    currentTopic.questions.forEach(question => {
      if (selectedAnswers[question.id] === question.correctAnswer) {
        calculatedScore++
      }
    })
    setScore(calculatedScore)
  }

  const restartQuiz = () => {
    setSelectedAnswers({})
    setCurrentQuestionIndex(0)
    setShowResults(false)
    setScore(0)
  }

  const getScoreMessage = () => {
    if (score >= 4) return 'Excellent! Great job!'
    if (score >= 3) return 'Good work! Keep it up!'
    if (score >= 2) return 'Not bad! Keep studying!'
    return 'Keep practicing! You\'ll improve!'
  }

  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4">
      <div className="bg-white rounded-xl max-w-3xl w-full max-h-[90vh] overflow-y-auto">
        <div className="sticky top-0 bg-white border-b p-4 flex justify-between items-center z-10">
          <h2 className="text-xl font-bold text-gray-800">Practice Quiz</h2>
          <button
            onClick={onClose}
            className="text-gray-500 hover:text-gray-700 text-2xl"
          >
            &times;
          </button>
        </div>

        <div className="p-6">
          {!selectedTopic ? (
            <div>
              <h3 className="text-lg font-semibold mb-4">Choose a Quiz Topic:</h3>
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                {quizTopics.map((topic) => (
                  <div
                    key={topic.id}
                    className="border rounded-lg p-4 cursor-pointer hover:bg-gray-50 transition-colors"
                    onClick={() => setSelectedTopic(topic.title)}
                  >
                    <h4 className="font-semibold text-gray-800">{topic.title}</h4>
                    <p className="text-sm text-gray-600 mt-1">5 Questions • Reading Level</p>
                  </div>
                ))}
              </div>
            </div>
          ) : !showResults ? (
            currentTopic && (
              <div>
                <div className="mb-4">
                  <h3 className="text-lg font-semibold text-gray-800">{currentTopic.title}</h3>
                  <div className="text-sm text-gray-600 mt-1">
                    Question {currentQuestionIndex + 1} of {currentTopic.questions.length}
                  </div>
                </div>

                <div className="mb-6">
                  <h4 className="font-medium text-gray-800 mb-4">{currentQuestion?.text}</h4>

                  <div className="space-y-2">
                    {currentQuestion?.options.map((option, index) => (
                      <div
                        key={index}
                        className={`p-3 border rounded-lg cursor-pointer ${
                          selectedAnswers[currentQuestion?.id ?? -1] === index
                            ? 'border-blue-500 bg-blue-50'
                            : 'border-gray-200 hover:bg-gray-50'
                        }`}
                        onClick={() => handleAnswerSelect(index)}
                      >
                        <input
                          type="radio"
                          id={`option-${index}`}
                          name="answer"
                          checked={selectedAnswers[currentQuestion?.id ?? -1] === index}
                          onChange={() => handleAnswerSelect(index)}
                          className="mr-3"
                        />
                        <label htmlFor={`option-${index}`} className="cursor-pointer">
                          {String.fromCharCode(65 + index)}. {option}
                        </label>
                      </div>
                    ))}
                  </div>
                </div>

                <div className="flex justify-between mt-6">
                  <button
                    onClick={handlePreviousQuestion}
                    disabled={currentQuestionIndex === 0}
                    className={`px-4 py-2 rounded-lg ${
                      currentQuestionIndex === 0
                        ? 'bg-gray-200 text-gray-500 cursor-not-allowed'
                        : 'bg-gray-200 text-gray-700 hover:bg-gray-300'
                    }`}
                  >
                    Previous
                  </button>

                  <button
                    onClick={handleNextQuestion}
                    disabled={selectedAnswers[currentQuestion?.id ?? -1] === undefined}
                    className={`px-4 py-2 rounded-lg ${
                      selectedAnswers[currentQuestion?.id ?? -1] === undefined
                        ? 'bg-gray-200 text-gray-500 cursor-not-allowed'
                        : 'bg-blue-500 text-white hover:bg-blue-600'
                    }`}
                  >
                    {currentQuestionIndex < 4 ? 'Next Question' : 'Finish Quiz'}
                  </button>
                </div>
              </div>
            )
          ) : (
            currentTopic && (
              <div className="text-center">
                <h3 className="text-2xl font-bold text-gray-800 mb-2">Quiz Completed!</h3>
                <p className="text-lg text-gray-700 mb-6">{getScoreMessage()}</p>

                <div className="bg-gradient-to-r from-blue-100 to-purple-100 rounded-xl p-6 mb-6">
                  <div className="text-5xl font-bold text-indigo-600 mb-2">{score}/{currentTopic.questions.length}</div>
                  <div className="text-gray-700">Your Score</div>
                </div>

                <div className="mb-6">
                  <h4 className="font-semibold text-gray-800 mb-3">Review Answers:</h4>
                  <div className="text-left space-y-4 max-h-60 overflow-y-auto">
                    {currentTopic.questions.map((question, qIndex) => {
                      const userAnswer = selectedAnswers[question.id]
                      const isCorrect = userAnswer === question.correctAnswer

                      return (
                        <div
                          key={question.id}
                          className={`p-3 rounded-lg border ${
                            isCorrect ? 'bg-green-50 border-green-200' : 'bg-red-50 border-red-200'
                          }`}
                        >
                          <div className="font-medium">Q{qIndex + 1}: {question.text}</div>
                          <div className="mt-2">
                            <div className={`text-sm ${isCorrect ? 'text-green-700' : 'text-red-700'}`}>
                              Your answer: {userAnswer !== undefined
                                ? String.fromCharCode(65 + userAnswer) + '. ' + question.options[userAnswer]
                                : 'No answer'}
                              {!isCorrect && (
                                <div className="text-green-700">
                                  Correct answer: {String.fromCharCode(65 + question.correctAnswer)}. {question.options[question.correctAnswer]}
                                </div>
                              )}
                            </div>
                          </div>
                        </div>
                      )
                    })}
                  </div>
                </div>

                <div className="flex justify-center space-x-4">
                  <button
                    onClick={restartQuiz}
                    className="px-6 py-2 bg-blue-500 text-white rounded-lg hover:bg-blue-600"
                  >
                    Retake Quiz
                  </button>
                  <button
                    onClick={() => setSelectedTopic(null)}
                    className="px-6 py-2 bg-gray-200 text-gray-700 rounded-lg hover:bg-gray-300"
                  >
                    Choose Another Topic
                  </button>
                </div>
              </div>
            )
          )}
        </div>
      </div>
    </div>
  )
}

export default QuizInterface