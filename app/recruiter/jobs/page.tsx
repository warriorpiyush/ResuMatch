"use client"

import { RecruiterSidebar } from "@/components/recruiter-sidebar"
import { Card } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { Badge } from "@/components/ui/badge"
import { BarChart3, Briefcase, Users, Settings, Edit2, Trash2, Eye } from "lucide-react"

const navItems = [
  { label: "Dashboard", href: "/recruiter/dashboard", icon: <BarChart3 className="w-5 h-5" /> },
  { label: "Job Postings", href: "/recruiter/jobs", icon: <Briefcase className="w-5 h-5" />, badge: "5" },
  { label: "Candidates", href: "/recruiter/candidates", icon: <Users className="w-5 h-5" />, badge: "24" },
  { label: "Settings", href: "/recruiter/settings", icon: <Settings className="w-5 h-5" /> },
]

const jobs = [
  {
    id: 1,
    title: "Senior Software Engineer",
    posted: "2 days ago",
    views: 234,
    applications: 18,
    status: "Active",
    salary: "$150K - $200K",
  },
  {
    id: 2,
    title: "Full Stack Developer",
    posted: "1 week ago",
    views: 156,
    applications: 12,
    status: "Active",
    salary: "$120K - $160K",
  },
  {
    id: 3,
    title: "Product Manager",
    posted: "2 weeks ago",
    views: 89,
    applications: 5,
    status: "Closed",
    salary: "$130K - $170K",
  },
  {
    id: 4,
    title: "UX/UI Designer",
    posted: "3 weeks ago",
    views: 145,
    applications: 8,
    status: "Active",
    salary: "$100K - $140K",
  },
]

export default function JobsPage() {
  return (
    <div className="flex h-screen bg-background">
      <RecruiterSidebar items={navItems} title="Recruiter" subtitle="Job Postings" />

      <main className="flex-1 overflow-auto md:ml-0">
        <div className="p-6 md:p-8 max-w-6xl mx-auto space-y-8">
          <div className="pt-12 md:pt-0 flex items-center justify-between">
            <div>
              <h1 className="text-4xl font-bold text-foreground mb-2">Job Postings</h1>
              <p className="text-muted-foreground">Manage and track your job postings</p>
            </div>
            <Button className="btn-primary">New Posting</Button>
          </div>

          <div className="space-y-4">
            {jobs.map((job) => (
              <Card key={job.id} className="border border-border bg-card p-6 hover:border-primary transition-colors">
                <div className="flex items-start justify-between gap-4">
                  <div className="flex-1">
                    <div className="flex items-center gap-3 mb-2">
                      <h3 className="text-lg font-bold text-foreground">{job.title}</h3>
                      <Badge
                        className={
                          job.status === "Active"
                            ? "bg-accent text-accent-foreground"
                            : "bg-muted text-muted-foreground"
                        }
                      >
                        {job.status}
                      </Badge>
                    </div>
                    <p className="text-sm text-muted-foreground mb-3">{job.salary}</p>
                    <p className="text-xs text-muted-foreground">Posted {job.posted}</p>
                  </div>

                  <div className="flex items-center gap-6 text-sm border-l border-border pl-6">
                    <div className="text-center">
                      <div className="text-2xl font-bold text-foreground">{job.views}</div>
                      <div className="text-xs text-muted-foreground">Views</div>
                    </div>
                    <div className="text-center">
                      <div className="text-2xl font-bold text-foreground">{job.applications}</div>
                      <div className="text-xs text-muted-foreground">Applications</div>
                    </div>
                  </div>

                  <div className="flex gap-2">
                    <Button
                      variant="outline"
                      size="sm"
                      className="border-border text-foreground hover:bg-muted gap-2 bg-transparent"
                    >
                      <Eye className="w-4 h-4" />
                      <span className="hidden sm:inline">View</span>
                    </Button>
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
                      className="border-border text-destructive hover:bg-destructive/10 gap-2 bg-transparent"
                    >
                      <Trash2 className="w-4 h-4" />
                      <span className="hidden sm:inline">Delete</span>
                    </Button>
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
