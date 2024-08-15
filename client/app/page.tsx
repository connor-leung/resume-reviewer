"use client";
import { useState, ChangeEvent, FormEvent } from 'react';

interface SuccessResult {
  score: number;
  [key: string]: any; 
}

interface ErrorResult {
  error: string;
}

type Result = SuccessResult | ErrorResult;

export default function Home() {
  const [file, setFile] = useState<File | null>(null);
  const [jobType, setJobType] = useState<string>('SWE');
  const [jobDescription, setJobDescription] = useState<string>('');
  const [result, setResult] = useState<Result | null>(null);

  const handleFileChange = (e: ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files.length > 0) {
      setFile(e.target.files[0]);
    }
  };

  const handleSubmit = async (e: FormEvent<HTMLFormElement>) => {
    e.preventDefault();

    if (!file) return;

    const formData = new FormData();
    formData.append('file', file);
    formData.append('job_type', jobType);
    formData.append('job_description', jobDescription);

    try {
      const response = await fetch('http://127.0.0.1:5000/api/parse_resume', {
        method: 'POST',
        body: formData,
      });

      const data: SuccessResult = await response.json();
      setResult(data);
    } catch (error) {
      console.error('Error:', error);
      setResult({ error: 'Something went wrong.' } as ErrorResult); 
    }
  };

  return (
    <div className="flex flex-col items-center justify-center min-h-screen bg-gray-100">
      <h1 className="text-4xl font-bold mb-8 text-center">Resume Reviewer</h1>
      <form onSubmit={handleSubmit} className="w-full max-w-lg bg-white p-8 rounded-lg shadow-md">
        <div className="mb-6">
          <label htmlFor="resume" className="block text-gray-700 text-lg font-medium mb-2">Upload Resume (PDF):</label>
          <input
            type="file"
            id="resume"
            accept=".pdf"
            onChange={handleFileChange}
            required
            className="w-full p-3 border border-gray-300 rounded-lg"
          />
        </div>
        <div className="mb-6">
          <label htmlFor="job_type" className="block text-gray-700 text-lg font-medium mb-2">Job Type:</label>
          <select
            id="job_type"
            value={jobType}
            onChange={(e) => setJobType(e.target.value)}
            className="w-full p-3 border border-gray-300 rounded-lg"
          >
            <option value="SWE">Software Engineer</option>
            <option value="Business">Business</option>
          </select>
        </div>
        <div className="mb-6">
          <label htmlFor="job_description" className="block text-gray-700 text-lg font-medium mb-2">Job Description:</label>
          <textarea
            id="job_description"
            value={jobDescription}
            onChange={(e) => setJobDescription(e.target.value)}
            rows={6}
            className="w-full p-3 border border-gray-300 rounded-lg"
            required
          ></textarea>
        </div>
        <button type="submit" className="w-full bg-blue-500 text-white py-3 rounded-lg hover:bg-blue-600 transition duration-200">Submit</button>
      </form>

      {result && (
        <div className="mt-8 w-full max-w-lg bg-white p-6 rounded-lg shadow-md">
          <h2 className="text-2xl font-bold mb-4">Result:</h2>
          {'score' in result ? (
            <>
              <pre className="bg-gray-100 p-4 rounded-lg overflow-x-auto">{JSON.stringify(result.score, null, 2)}</pre>
              <progress value={result.score} max="100" className="w-full"></progress>
            </>
          ) : (
            <p className="text-red-500">{result.error}</p>
          )}
        </div>
      )}
    </div>
  );
}
