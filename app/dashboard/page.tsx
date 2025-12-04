"use client"

import { SidebarNav } from "@/components/sidebar-nav"
import { ResumeUpload } from "@/components/resume-upload"
import { ResumeAnalysis } from "@/components/resume-analysis"
import { Card } from "@/components/ui/card"
import { BarChart3, Sparkles, Briefcase, Settings } from "lucide-react"
import { useState } from "react"

const navItems = [
  { label: "Dashboard", href: "/dashboard", icon: <BarChart3 className="w-5 h-5" /> },
  { label: "My Resume", href: "/dashboard/resume", icon: <Sparkles className="w-5 h-5" /> },
  { label: "Job Matches", href: "/dashboard/matches", icon: <Briefcase className="w-5 h-5" />, badge: "12" },
  { label: "Settings", href: "/dashboard/settings", icon: <Settings className="w-5 h-5" /> },
]

export default function DashboardPage() {
  const [showAnalysis, setShowAnalysis] = useState(false)

  return (
    <div className="flex h-screen bg-background">
      <SidebarNav items={navItems} title="Candidate" subtitle="Dashboard" />

      {/* Main Content */}
      <main className="flex-1 overflow-auto md:ml-0">
        <div className="p-6 md:p-8 max-w-7xl mx-auto space-y-8">
          {/* Header */}
          <div className="pt-12 md:pt-0">
            <h1 className="text-4xl font-bold text-foreground mb-2">Dashboard</h1>
            <p className="text-muted-foreground">Welcome back! Upload your resume to get started.</p>
          </div>

          {/* Stats */}
          <div className="grid md:grid-cols-4 gap-4">
            <Card className="border border-border bg-card p-6">
              <div className="space-y-2">
                <p className="text-xs font-medium text-muted-foreground uppercase tracking-wider">Resume Score</p>
                <p className="text-3xl font-bold text-foreground">85</p>
                <p className="text-xs text-accent">+2 from last update</p>
              </div>
            </Card>
            <Card className="border border-border bg-card p-6">
              <div className="space-y-2">
                <p className="text-xs font-medium text-muted-foreground uppercase tracking-wider">Job Matches</p>
                <p className="text-3xl font-bold text-foreground">12</p>
                <p className="text-xs text-accent">This week</p>
              </div>
            </Card>
            <Card className="border border-border bg-card p-6">
              <div className="space-y-2">
                <p className="text-xs font-medium text-muted-foreground uppercase tracking-wider">Applications</p>
                <p className="text-3xl font-bold text-foreground">8</p>
                <p className="text-xs text-accent">Active</p>
              </div>
            </Card>
            <Card className="border border-border bg-card p-6">
              <div className="space-y-2">
                <p className="text-xs font-medium text-muted-foreground uppercase tracking-wider">Profile Views</p>
                <p className="text-3xl font-bold text-foreground">48</p>
                <p className="text-xs text-accent">This month</p>
              </div>
            </Card>
          </div>

          {/* Content */}
          <div className="grid lg:grid-cols-3 gap-8">
            <div className="lg:col-span-2">
              <ResumeUpload />
            </div>

            {/* Quick Tips */}
            <Card className="border border-border bg-card p-6 h-fit">
              <div className="space-y-4">
                <h3 className="font-bold text-foreground">Quick Tips</h3>
                <ul className="space-y-3">
                  <li className="text-sm text-foreground">
                    <span className="font-medium block mb-1">Keep it concise</span>
                    <span className="text-muted-foreground text-xs">One page for entry-level, two for experienced</span>
                  </li>
                  <li className="text-sm text-foreground border-t border-border pt-3">
                    <span className="font-medium block mb-1">Use keywords</span>
                    <span className="text-muted-foreground text-xs">Match job descriptions for better matches</span>
                  </li>
                  <li className="text-sm text-foreground border-t border-border pt-3">
                    <span className="font-medium block mb-1">Show impact</span>
                    <span className="text-muted-foreground text-xs">Use metrics and results, not just duties</span>
                  </li>
                </ul>
              </div>
            </Card>
          </div>

          {/* Analysis Section */}
          {showAnalysis && <ResumeAnalysis />}

          {!showAnalysis && (
            <Card className="border border-border bg-card p-8 text-center">
              <p className="text-muted-foreground mb-4">Upload a resume to see AI-powered analysis</p>
              <button onClick={() => setShowAnalysis(true)} className="btn-primary">
                View Sample Analysis
              </button>
            </Card>
          )}
        </div>
      </main>
    </div>
  )
}
