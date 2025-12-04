"use client"

import { Card } from "@/components/ui/card"
import { CheckCircle2, AlertCircle } from "lucide-react"

interface AnalysisMetric {
  label: string
  value: number
  max: number
  status: "good" | "warning" | "critical"
}

const analysisData: AnalysisMetric[] = [
  { label: "Keyword Optimization", value: 85, max: 100, status: "good" },
  { label: "Format Clarity", value: 78, max: 100, status: "good" },
  { label: "Experience Details", value: 72, max: 100, status: "warning" },
  { label: "Achievement Metrics", value: 65, max: 100, status: "warning" },
]

export function ResumeAnalysis() {
  const overallScore = Math.round(analysisData.reduce((a, b) => a + b.value, 0) / analysisData.length)

  return (
    <div className="space-y-6">
      <Card className="border border-border bg-card p-8">
        <div className="space-y-6">
          <div>
            <h3 className="text-lg font-bold text-foreground mb-2">Resume Analysis</h3>
            <p className="text-sm text-muted-foreground">AI-powered insights to improve your resume</p>
          </div>

          {/* Overall Score */}
          <div className="grid md:grid-cols-2 gap-6">
            <div className="flex items-center gap-6">
              <div className="relative w-24 h-24">
                <svg className="w-24 h-24 transform -rotate-90">
                  <circle
                    cx="48"
                    cy="48"
                    r="44"
                    fill="none"
                    stroke="currentColor"
                    strokeWidth="2"
                    className="text-muted"
                  />
                  <circle
                    cx="48"
                    cy="48"
                    r="44"
                    fill="none"
                    stroke="currentColor"
                    strokeWidth="2"
                    strokeDasharray={`${(overallScore / 100) * 276.32} 276.32`}
                    className="text-accent transition-all duration-500"
                  />
                </svg>
                <div className="absolute inset-0 flex items-center justify-center">
                  <div className="text-center">
                    <div className="text-2xl font-bold text-foreground">{overallScore}</div>
                    <div className="text-xs text-muted-foreground">/100</div>
                  </div>
                </div>
              </div>
              <div className="space-y-2">
                <p className="font-medium text-foreground">Overall Score</p>
                <p className="text-sm text-muted-foreground">
                  Your resume is well-structured and ready for applications
                </p>
              </div>
            </div>

            {/* Key Metrics */}
            <div className="space-y-3">
              {analysisData.map((metric) => (
                <div key={metric.label} className="space-y-1">
                  <div className="flex items-center justify-between">
                    <label className="text-sm font-medium text-foreground flex items-center gap-2">
                      {metric.status === "good" && <CheckCircle2 className="w-4 h-4 text-accent" />}
                      {metric.status !== "good" && <AlertCircle className="w-4 h-4 text-destructive" />}
                      {metric.label}
                    </label>
                    <span className="text-xs font-medium text-muted-foreground">
                      {metric.value}/{metric.max}
                    </span>
                  </div>
                  <div className="w-full bg-muted rounded-full h-2">
                    <div
                      className={`h-2 rounded-full transition-all ${
                        metric.status === "good"
                          ? "bg-accent"
                          : metric.status === "warning"
                            ? "bg-yellow-500"
                            : "bg-destructive"
                      }`}
                      style={{ width: `${metric.value}%` }}
                    />
                  </div>
                </div>
              ))}
            </div>
          </div>
        </div>
      </Card>

      {/* Recommendations */}
      <Card className="border border-border bg-card p-8">
        <div className="space-y-4">
          <h4 className="font-bold text-foreground">Recommendations</h4>
          <ul className="space-y-3">
            <li className="flex gap-3 items-start">
              <div className="w-2 h-2 rounded-full bg-accent mt-2 flex-shrink-0" />
              <span className="text-sm text-foreground">
                Add more quantifiable achievements to your experience section
              </span>
            </li>
            <li className="flex gap-3 items-start">
              <div className="w-2 h-2 rounded-full bg-accent mt-2 flex-shrink-0" />
              <span className="text-sm text-foreground">
                Include industry-specific keywords related to your target roles
              </span>
            </li>
            <li className="flex gap-3 items-start">
              <div className="w-2 h-2 rounded-full bg-accent mt-2 flex-shrink-0" />
              <span className="text-sm text-foreground">
                Expand your skills section with relevant technical competencies
              </span>
            </li>
          </ul>
        </div>
      </Card>
    </div>
  )
}
