"use client"

import { RecruiterSidebar } from "@/components/recruiter-sidebar"
import { JobPostingForm } from "@/components/job-posting-form"
import { BarChart3, Briefcase, Users, Settings } from "lucide-react"

const navItems = [
  { label: "Dashboard", href: "/recruiter/dashboard", icon: <BarChart3 className="w-5 h-5" /> },
  { label: "Job Postings", href: "/recruiter/jobs", icon: <Briefcase className="w-5 h-5" />, badge: "5" },
  { label: "Candidates", href: "/recruiter/candidates", icon: <Users className="w-5 h-5" />, badge: "24" },
  { label: "Settings", href: "/recruiter/settings", icon: <Settings className="w-5 h-5" /> },
]

export default function NewJobPage() {
  const handleSubmit = (data: any) => {
    console.log("Submitting job:", data)
  }

  return (
    <div className="flex h-screen bg-background">
      <RecruiterSidebar items={navItems} title="Recruiter" subtitle="Post Job" />

      <main className="flex-1 overflow-auto md:ml-0">
        <div className="p-6 md:p-8 max-w-2xl mx-auto space-y-8">
          <div className="pt-12 md:pt-0">
            <h1 className="text-4xl font-bold text-foreground mb-2">Post New Job</h1>
            <p className="text-muted-foreground">Fill in the details to create a new job posting</p>
          </div>

          <JobPostingForm onSubmit={handleSubmit} />
        </div>
      </main>
    </div>
  )
}
