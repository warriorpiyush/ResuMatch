"use client"

import type React from "react"

import { useState } from "react"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Card } from "@/components/ui/card"

export function JobPostingForm({ onSubmit }: { onSubmit: (data: any) => void }) {
  const [formData, setFormData] = useState({
    title: "",
    description: "",
    requirements: "",
    benefits: "",
    location: "",
    salary: "",
    jobType: "Full-time",
  })

  const handleChange = (e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement | HTMLSelectElement>) => {
    const { name, value } = e.target
    setFormData((prev) => ({ ...prev, [name]: value }))
  }

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault()
    onSubmit(formData)
  }

  return (
    <Card className="border border-border bg-card p-8">
      <form onSubmit={handleSubmit} className="space-y-6">
        <div>
          <h3 className="text-xl font-bold text-foreground mb-6">Post a New Job</h3>
        </div>

        <div className="space-y-2">
          <label className="block text-sm font-medium text-foreground">Job Title</label>
          <Input
            name="title"
            placeholder="e.g., Senior Software Engineer"
            value={formData.title}
            onChange={handleChange}
            required
            className="bg-background border-border text-foreground"
          />
        </div>

        <div className="grid md:grid-cols-2 gap-6">
          <div className="space-y-2">
            <label className="block text-sm font-medium text-foreground">Location</label>
            <Input
              name="location"
              placeholder="e.g., San Francisco, CA"
              value={formData.location}
              onChange={handleChange}
              className="bg-background border-border text-foreground"
            />
          </div>
          <div className="space-y-2">
            <label className="block text-sm font-medium text-foreground">Salary Range</label>
            <Input
              name="salary"
              placeholder="e.g., $150K - $200K"
              value={formData.salary}
              onChange={handleChange}
              className="bg-background border-border text-foreground"
            />
          </div>
        </div>

        <div className="space-y-2">
          <label className="block text-sm font-medium text-foreground">Job Type</label>
          <select
            name="jobType"
            value={formData.jobType}
            onChange={handleChange}
            className="w-full px-3 py-2 rounded-lg bg-background border border-border text-foreground"
          >
            <option>Full-time</option>
            <option>Part-time</option>
            <option>Contract</option>
            <option>Temporary</option>
          </select>
        </div>

        <div className="space-y-2">
          <label className="block text-sm font-medium text-foreground">Job Description</label>
          <textarea
            name="description"
            placeholder="Describe the role and responsibilities..."
            value={formData.description}
            onChange={handleChange}
            rows={6}
            className="w-full px-3 py-2 rounded-lg bg-background border border-border text-foreground placeholder:text-muted-foreground"
          />
        </div>

        <div className="space-y-2">
          <label className="block text-sm font-medium text-foreground">Requirements</label>
          <textarea
            name="requirements"
            placeholder="List key requirements, one per line..."
            value={formData.requirements}
            onChange={handleChange}
            rows={4}
            className="w-full px-3 py-2 rounded-lg bg-background border border-border text-foreground placeholder:text-muted-foreground"
          />
        </div>

        <div className="space-y-2">
          <label className="block text-sm font-medium text-foreground">Benefits</label>
          <textarea
            name="benefits"
            placeholder="List benefits, one per line..."
            value={formData.benefits}
            onChange={handleChange}
            rows={4}
            className="w-full px-3 py-2 rounded-lg bg-background border border-border text-foreground placeholder:text-muted-foreground"
          />
        </div>

        <div className="flex gap-3">
          <Button type="submit" className="btn-primary">
            Post Job
          </Button>
          <Button
            type="button"
            variant="outline"
            className="border-border text-foreground hover:bg-muted bg-transparent"
          >
            Save as Draft
          </Button>
        </div>
      </form>
    </Card>
  )
}
