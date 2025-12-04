"use client"

import { SidebarNav } from "@/components/sidebar-nav"
import { Card } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { BarChart3, Sparkles, Briefcase, Settings, Download, Edit2, Trash2 } from "lucide-react"

const navItems = [
  { label: "Dashboard", href: "/dashboard", icon: <BarChart3 className="w-5 h-5" /> },
  { label: "My Resume", href: "/dashboard/resume", icon: <Sparkles className="w-5 h-5" /> },
  { label: "Job Matches", href: "/dashboard/matches", icon: <Briefcase className="w-5 h-5" />, badge: "12" },
  { label: "Settings", href: "/dashboard/settings", icon: <Settings className="w-5 h-5" /> },
]

const resumes = [
  {
    id: 1,
    name: "John_Doe_Resume.pdf",
    score: 85,
    uploadedAt: "2 days ago",
    size: "234 KB",
  },
  {
    id: 2,
    name: "John_Doe_Senior_Dev.pdf",
    score: 78,
    uploadedAt: "1 week ago",
    size: "198 KB",
  },
  {
    id: 3,
    name: "John_Doe_Extended.pdf",
    score: 72,
    uploadedAt: "3 weeks ago",
    size: "412 KB",
  },
]

export default function ResumePage() {
  return (
    <div className="flex h-screen bg-background">
      <SidebarNav items={navItems} title="Candidate" subtitle="My Resume" />

      <main className="flex-1 overflow-auto md:ml-0">
        <div className="p-6 md:p-8 max-w-4xl mx-auto space-y-8">
          <div className="pt-12 md:pt-0">
            <h1 className="text-4xl font-bold text-foreground mb-2">My Resumes</h1>
            <p className="text-muted-foreground">Manage and optimize your resumes</p>
          </div>

          <div className="space-y-4">
            {resumes.map((resume) => (
              <Card key={resume.id} className="border border-border bg-card p-6">
                <div className="flex items-center justify-between gap-4">
                  <div className="flex-1 min-w-0">
                    <h3 className="font-bold text-foreground mb-1 truncate">{resume.name}</h3>
                    <p className="text-xs text-muted-foreground">
                      Uploaded {resume.uploadedAt} • {resume.size}
                    </p>
                  </div>

                  <div className="flex items-center gap-4">
                    <div className="text-right">
                      <div className="text-2xl font-bold text-foreground">{resume.score}</div>
                      <div className="text-xs text-muted-foreground">Score</div>
                    </div>

                    <div className="flex gap-2">
                      <Button
                        variant="outline"
                        size="sm"
                        className="border-border text-foreground hover:bg-muted gap-2 bg-transparent"
                      >
                        <Edit2 className="w-4 h-4" />
                        <span className="hidden sm:inline">Edit</span>
                      </Button>
                      <Button
                        variant="outline"
                        size="sm"
                        className="border-border text-foreground hover:bg-muted gap-2 bg-transparent"
                      >
                        <Download className="w-4 h-4" />
                        <span className="hidden sm:inline">Download</span>
                      </Button>
                      <Button
                        variant="outline"
                        size="sm"
                        className="border-border text-destructive hover:bg-destructive/10 gap-2 bg-transparent"
                      >
                        <Trash2 className="w-4 h-4" />
                        <span className="hidden sm:inline">Delete</span>
                      </Button>
                    </div>
                  </div>
                </div>
              </Card>
            ))}
          </div>
        </div>
      </main>
    </div>
  )
}
