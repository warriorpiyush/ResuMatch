"use client"

import type React from "react"

import { useState } from "react"
import { Button } from "@/components/ui/button"
import { Card } from "@/components/ui/card"
import { Upload, File, Check } from "lucide-react"

export function ResumeUpload() {
  const [file, setFile] = useState<File | null>(null)
  const [uploading, setUploading] = useState(false)
  const [uploaded, setUploaded] = useState(false)

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files) {
      setFile(e.target.files[0])
    }
  }

  const handleUpload = async () => {
    if (!file) return

    setUploading(true)
    // Simulate upload
    setTimeout(() => {
      setUploading(false)
      setUploaded(true)
      setTimeout(() => {
        setFile(null)
        setUploaded(false)
      }, 2000)
    }, 1500)
  }

  return (
    <Card className="border border-border bg-card p-8">
      <div className="space-y-6">
        <div>
          <h3 className="text-lg font-bold text-foreground mb-2">Upload Your Resume</h3>
          <p className="text-sm text-muted-foreground">Upload your resume to get AI-powered analysis and job matches</p>
        </div>

        {!file && !uploaded && (
          <div className="border-2 border-dashed border-border rounded-lg p-8 text-center hover:border-primary transition-colors cursor-pointer">
            <input
              type="file"
              accept=".pdf,.doc,.docx"
              onChange={handleFileChange}
              className="sr-only"
              id="resume-input"
            />
            <label htmlFor="resume-input" className="cursor-pointer block">
              <Upload className="w-12 h-12 text-accent mx-auto mb-3" />
              <p className="font-medium text-foreground mb-1">Drop your resume here</p>
              <p className="text-xs text-muted-foreground">or click to browse (PDF, DOC, DOCX)</p>
            </label>
          </div>
        )}

        {file && !uploaded && (
          <div className="space-y-4">
            <div className="flex items-center gap-3 p-4 bg-muted rounded-lg">
              <File className="w-5 h-5 text-accent flex-shrink-0" />
              <div className="flex-1 min-w-0">
                <p className="font-medium text-foreground truncate">{file.name}</p>
                <p className="text-xs text-muted-foreground">{(file.size / 1024).toFixed(2)} KB</p>
              </div>
              <button onClick={() => setFile(null)} className="text-xs text-destructive hover:underline">
                Remove
              </button>
            </div>
            <Button onClick={handleUpload} disabled={uploading} className="btn-primary w-full">
              {uploading ? "Uploading..." : "Upload Resume"}
            </Button>
          </div>
        )}

        {uploaded && (
          <div className="flex items-center gap-3 p-4 bg-muted rounded-lg">
            <Check className="w-5 h-5 text-accent flex-shrink-0" />
            <div>
              <p className="font-medium text-foreground">Resume uploaded successfully!</p>
              <p className="text-xs text-muted-foreground">Analyzing your resume...</p>
            </div>
          </div>
        )}
      </div>
    </Card>
  )
}
