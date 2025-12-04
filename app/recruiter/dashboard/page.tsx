"use client"

import { RecruiterSidebar } from "@/components/recruiter-sidebar"
import { Card } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { BarChart3, Briefcase, Users, Settings, Eye, Heart } from "lucide-react"

const navItems = [
  { label: "Dashboard", href: "/recruiter/dashboard", icon: <BarChart3 className="w-5 h-5" /> },
  { label: "Job Postings", href: "/recruiter/jobs", icon: <Briefcase className="w-5 h-5" />, badge: "5" },
  { label: "Candidates", href: "/recruiter/candidates", icon: <Users className="w-5 h-5" />, badge: "24" },
  { label: "Settings", href: "/recruiter/settings", icon: <Settings className="w-5 h-5" /> },
]

const recentJobs = [
  {
    id: 1,
    title: "Senior Software Engineer",
    posted: "2 days ago",
    views: 234,
    applications: 18,
    status: "Active",
  },
  {
    id: 2,
    title: "Full Stack Developer",
    posted: "1 week ago",
    views: 156,
    applications: 12,
    status: "Active",
  },
  {
    id: 3,
    title: "Product Manager",
    posted: "2 weeks ago",
    views: 89,
    applications: 5,
    status: "Closed",
  },
]

export default function RecruiterDashboard() {
  return (
    <div className="flex h-screen bg-background">
      <RecruiterSidebar items={navItems} title="Recruiter" subtitle="Dashboard" />

      <main className="flex-1 overflow-auto md:ml-0">
        <div className="p-6 md:p-8 max-w-7xl mx-auto space-y-8">
          <div className="pt-12 md:pt-0">
            <h1 className="text-4xl font-bold text-foreground mb-2">Dashboard</h1>
            <p className="text-muted-foreground">Welcome back! Manage your job postings and candidates.</p>
          </div>

          {/* Stats */}
          <div className="grid md:grid-cols-4 gap-4">
            <Card className="border border-border bg-card p-6">
              <div className="space-y-2">
                <p className="text-xs font-medium text-muted-foreground uppercase">Active Postings</p>
                <p className="text-3xl font-bold text-foreground">5</p>
                <p className="text-xs text-accent">2 new this week</p>
              </div>
            </Card>
            <Card className="border border-border bg-card p-6">
              <div className="space-y-2">
                <p className="text-xs font-medium text-muted-foreground uppercase">Applications</p>
                <p className="text-3xl font-bold text-foreground">47</p>
                <p className="text-xs text-accent">12 this week</p>
              </div>
            </Card>
            <Card className="border border-border bg-card p-6">
              <div className="space-y-2">
                <p className="text-xs font-medium text-muted-foreground uppercase">Total Views</p>
                <p className="text-3xl font-bold text-foreground">892</p>
                <p className="text-xs text-accent">+156 this week</p>
              </div>
            </Card>
            <Card className="border border-border bg-card p-6">
              <div className="space-y-2">
                <p className="text-xs font-medium text-muted-foreground uppercase">Interviews</p>
                <p className="text-3xl font-bold text-foreground">8</p>
                <p className="text-xs text-accent">Scheduled</p>
              </div>
            </Card>
          </div>

          {/* Recent Jobs */}
          <Card className="border border-border bg-card p-6">
            <div className="space-y-6">
              <div className="flex items-center justify-between">
                <h3 className="text-lg font-bold text-foreground">Recent Job Postings</h3>
                <Button className="btn-primary">View All</Button>
              </div>

              <div className="space-y-4">
                {recentJobs.map((job) => (
                  <div key={job.id} className="flex items-center justify-between p-4 bg-muted rounded-lg">
                    <div className="flex-1">
                      <h4 className="font-bold text-foreground mb-1">{job.title}</h4>
                      <p className="text-xs text-muted-foreground">Posted {job.posted}</p>
                    </div>

                    <div className="flex items-center gap-6 text-sm">
                      <div className="text-right">
                        <div className="flex items-center gap-1 text-foreground">
                          <Eye className="w-4 h-4" />
                          {job.views}
                        </div>
                        <p className="text-xs text-muted-foreground">Views</p>
                      </div>
                      <div className="text-right">
                        <div className="flex items-center gap-1 text-foreground">
                          <Heart className="w-4 h-4" />
                          {job.applications}
                        </div>
                        <p className="text-xs text-muted-foreground">Applications</p>
                      </div>
                      <div>
                        <div
                          className={`px-3 py-1 rounded-full text-xs font-medium ${
                            job.status === "Active"
                              ? "bg-accent text-accent-foreground"
                              : "bg-muted text-muted-foreground"
                          }`}
                        >
                          {job.status}
                        </div>
                      </div>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          </Card>
        </div>
      </main>
    </div>
  )
}
