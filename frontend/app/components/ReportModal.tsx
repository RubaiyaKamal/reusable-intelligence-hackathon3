'use client'

import { useState } from 'react'

interface ReportModalProps {
  onClose: () => void
  onExportReport: (report: {
    type: string
    format: string
    dateRange: { start: string; end: string }
    include: string[]
  }) => void
}

const ReportModal = ({ onClose, onExportReport }: ReportModalProps) => {
  const [type, setType] = useState('overall')
  const [format, setFormat] = useState('pdf')
  const [dateRange, setDateRange] = useState({ start: '', end: '' })
  const [include, setInclude] = useState<string[]>(['progress', 'scores', 'assignments'])

  const reportTypes = [
    { id: 'overall', name: 'Overall Class Report' },
    { id: 'individual', name: 'Individual Student Reports' },
    { id: 'progress', name: 'Progress Report' },
    { id: 'performance', name: 'Performance Analysis' },
    { id: 'engagement', name: 'Engagement Metrics' }
  ]

  const reportFormats = [
    { id: 'pdf', name: 'PDF' },
    { id: 'excel', name: 'Excel (XLSX)' },
    { id: 'csv', name: 'CSV' },
    { id: 'json', name: 'JSON' }
  ]

  const reportOptions = [
    { id: 'progress', name: 'Progress Tracking' },
    { id: 'scores', name: 'Test Scores' },
    { id: 'assignments', name: 'Assignment Completion' },
    { id: 'attendance', name: 'Reading Time' },
    { id: 'behavior', name: 'Behavior Insights' },
    { id: 'goals', name: 'Goal Achievement' }
  ]

  const handleOptionToggle = (optionId: string) => {
    if (include.includes(optionId)) {
      setInclude(include.filter(id => id !== optionId))
    } else {
      setInclude([...include, optionId])
    }
  }

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault()

    onExportReport({
      type,
      format,
      dateRange,
      include
    })
  }

  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4">
      <div className="bg-white rounded-xl max-w-2xl w-full max-h-[90vh] overflow-y-auto">
        <div className="sticky top-0 bg-white border-b p-4 flex justify-between items-center z-10">
          <h2 className="text-xl font-bold text-gray-800">Export Report</h2>
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
              Report Type
            </label>
            <select
              value={type}
              onChange={(e) => setType(e.target.value)}
              className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
            >
              {reportTypes.map((report) => (
                <option key={report.id} value={report.id}>
                  {report.name}
                </option>
              ))}
            </select>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-6 mb-6">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Export Format
              </label>
              <select
                value={format}
                onChange={(e) => setFormat(e.target.value)}
                className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
              >
                {reportFormats.map((format) => (
                  <option key={format.id} value={format.id}>
                    {format.name}
                  </option>
                ))}
              </select>
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Date Range
              </label>
              <div className="grid grid-cols-2 gap-2">
                <input
                  type="date"
                  value={dateRange.start}
                  onChange={(e) => setDateRange({...dateRange, start: e.target.value})}
                  className="px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500 text-sm"
                />
                <input
                  type="date"
                  value={dateRange.end}
                  onChange={(e) => setDateRange({...dateRange, end: e.target.value})}
                  className="px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500 text-sm"
                />
              </div>
            </div>
          </div>

          <div className="mb-6">
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Include in Report
            </label>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-2 max-h-40 overflow-y-auto border border-gray-200 rounded-lg p-3">
              {reportOptions.map((option) => (
                <div key={option.id} className="flex items-center">
                  <input
                    type="checkbox"
                    id={`include-${option.id}`}
                    checked={include.includes(option.id)}
                    onChange={() => handleOptionToggle(option.id)}
                    className="h-4 w-4 text-blue-600 rounded focus:ring-blue-500"
                  />
                  <label htmlFor={`include-${option.id}`} className="ml-2 text-gray-700 text-sm">
                    {option.name}
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
              Export Report
            </button>
          </div>
        </form>
      </div>
    </div>
  )
}

export default ReportModal