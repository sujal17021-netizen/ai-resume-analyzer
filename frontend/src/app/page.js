"use client";

import { useState } from "react";

export default function Home() {
  const [file, setFile] = useState(null);
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);

  const handleUpload = async () => {
    if (!file) {
      alert("Please upload a PDF");
      return;
    }

    const formData = new FormData();
    formData.append("file", file);

    setLoading(true);

    try {
      const response = await fetch(
        `${process.env.NEXT_PUBLIC_API_URL}/analyze`,
        {
          method: "POST",
          body: formData,
        }
      );

      if (!response.ok) {
        throw new Error("Failed to analyze resume");
      }

      const data = await response.json();

      setResult(data);
    } catch (error) {
      console.error(error);
      alert("Something went wrong");
    }

    setLoading(false);
  };

  const getScoreColor = (score) => {
    if (score >= 80) return "text-green-500";
    if (score >= 60) return "text-yellow-500";
    return "text-red-500";
  };

  return (
    <main className="min-h-screen bg-gray-100 p-6 flex justify-center">
      <div className="w-full max-w-4xl">

        {/* Header */}
        <div className="bg-white rounded-2xl shadow-lg p-8 mb-6">
          <h1 className="text-4xl font-bold text-center mb-6">
            AI Resume Analyzer
          </h1>

          <div className="flex flex-col md:flex-row gap-4 items-center">
            <input
              type="file"
              accept=".pdf"
              onChange={(e) => setFile(e.target.files[0])}
              className="border p-3 rounded-lg w-full"
            />

            <button
              onClick={handleUpload}
              disabled={loading}
              className="bg-black text-white px-6 py-3 rounded-lg hover:bg-gray-800 transition"
            >
              {loading ? "Analyzing..." : "Analyze Resume"}
            </button>
          </div>
        </div>

        {/* Results */}
        {result && (
          <div className="space-y-6">

            {/* ATS Score */}
            <div className="bg-white rounded-2xl shadow-lg p-8">
              <h2 className="text-2xl font-bold mb-4">
                ATS Score
              </h2>

              <div
                className={`text-6xl font-bold mb-4 ${getScoreColor(
                  result.ats_score
                )}`}
              >
                {result.ats_score}/100
              </div>

              {/* Progress Bar */}
              <div className="w-full bg-gray-300 rounded-full h-5">
                <div
                  className="bg-green-500 h-5 rounded-full"
                  style={{
                    width: `${result.ats_score}%`,
                  }}
                ></div>
              </div>
            </div>

            {/* Breakdown */}
            <div className="bg-white rounded-2xl shadow-lg p-8">
              <h2 className="text-2xl font-bold mb-6">
                Score Breakdown
              </h2>

              <div className="grid grid-cols-2 md:grid-cols-3 gap-4">

                <div className="bg-gray-100 p-4 rounded-xl">
                  <h3 className="font-semibold">Skills Match</h3>
                  <p className="text-2xl font-bold">
                    {result.breakdown.skills_match}
                  </p>
                </div>

                <div className="bg-gray-100 p-4 rounded-xl">
                  <h3 className="font-semibold">Formatting</h3>
                  <p className="text-2xl font-bold">
                    {result.breakdown.formatting}
                  </p>
                </div>

                <div className="bg-gray-100 p-4 rounded-xl">
                  <h3 className="font-semibold">Keywords</h3>
                  <p className="text-2xl font-bold">
                    {result.breakdown.keywords}
                  </p>
                </div>

                <div className="bg-gray-100 p-4 rounded-xl">
                  <h3 className="font-semibold">Experience</h3>
                  <p className="text-2xl font-bold">
                    {result.breakdown.experience}
                  </p>
                </div>

                <div className="bg-gray-100 p-4 rounded-xl">
                  <h3 className="font-semibold">Readability</h3>
                  <p className="text-2xl font-bold">
                    {result.breakdown.readability}
                  </p>
                </div>

                <div className="bg-gray-100 p-4 rounded-xl">
                  <h3 className="font-semibold">Grammar</h3>
                  <p className="text-2xl font-bold">
                    {result.breakdown.grammar}
                  </p>
                </div>

              </div>
            </div>

            {/* Strengths */}
            <div className="bg-white rounded-2xl shadow-lg p-8">
              <h2 className="text-2xl font-bold text-green-600 mb-4">
                Strengths
              </h2>

              <ul className="list-disc pl-6 space-y-2">
                {result.strengths.map((item, index) => (
                  <li key={index}>{item}</li>
                ))}
              </ul>
            </div>

            {/* Weaknesses */}
            <div className="bg-white rounded-2xl shadow-lg p-8">
              <h2 className="text-2xl font-bold text-red-600 mb-4">
                Weaknesses
              </h2>

              <ul className="list-disc pl-6 space-y-2">
                {result.weaknesses.map((item, index) => (
                  <li key={index}>{item}</li>
                ))}
              </ul>
            </div>

            {/* Missing Skills */}
            <div className="bg-white rounded-2xl shadow-lg p-8">
              <h2 className="text-2xl font-bold text-yellow-600 mb-4">
                Missing Skills
              </h2>

              <ul className="list-disc pl-6 space-y-2">
                {result.missing_skills.map((item, index) => (
                  <li key={index}>{item}</li>
                ))}
              </ul>
            </div>

            {/* Suggestions */}
            <div className="bg-white rounded-2xl shadow-lg p-8">
              <h2 className="text-2xl font-bold text-blue-600 mb-4">
                Improvement Suggestions
              </h2>

              <ul className="list-disc pl-6 space-y-2">
                {result.improvement_suggestions.map((item, index) => (
                  <li key={index}>{item}</li>
                ))}
              </ul>
            </div>

          </div>
        )}
      </div>
    </main>
  );
}