"use client"

import { SidebarNav } from "@/components/sidebar-nav"
import { Card } from "@/components/ui/card"
import { Badge } from "@/components/ui/badge"
import { Button } from "@/components/ui/button"
import { BarChart3, Sparkles, Briefcase, Settings, MapPin, DollarSign, Heart } from "lucide-react"
import { useState } from "react"

const navItems = [
  { label: "Dashboard", href: "/dashboard", icon: <BarChart3 className="w-5 h-5" /> },
  { label: "My Resume", href: "/dashboard/resume", icon: <Sparkles className="w-5 h-5" /> },
  { label: "Job Matches", href: "/dashboard/matches", icon: <Briefcase className="w-5 h-5" />, badge: "12" },
  { label: "Settings", href: "/dashboard/settings", icon: <Settings className="w-5 h-5" /> },
]

const matches = [
  {
    id: 1,
    title: "Senior Software Engineer",
    company: "Tech Corp",
    location: "San Francisco, CA",
    salary: "$150K - $200K",
    matchScore: 95,
    tags: ["React", "Node.js", "TypeScript"],
    posted: "2 days ago",
  },
  {
    id: 2,
    title: "Full Stack Developer",
    company: "Startup Inc",
    location: "New York, NY",
    salary: "$120K - $160K",
    matchScore: 88,
    tags: ["React", "Python", "AWS"],
    posted: "1 week ago",
  },
  {
    id: 3,
    title: "Frontend Engineer",
    company: "Design Studio",
    location: "Remote",
    salary: "$100K - $140K",
    matchScore: 82,
    tags: ["React", "Vue.js", "CSS"],
    posted: "3 days ago",
  },
]

export default function MatchesPage() {
  const [saved, setSaved] = useState<number[]>([])

  return (
    <div className="flex h-screen bg-background">
      <SidebarNav items={navItems} title="Candidate" subtitle="Job Matches" />

      <main className="flex-1 overflow-auto md:ml-0">
        <div className="p-6 md:p-8 max-w-4xl mx-auto space-y-8">
          <div className="pt-12 md:pt-0">
            <h1 className="text-4xl font-bold text-foreground mb-2">Personalized Job Matches</h1>
            <p className="text-muted-foreground">We found 12 jobs that match your profile</p>
          </div>

          <div className="space-y-4">
            {matches.map((job) => (
              <Card key={job.id} className="border border-border bg-card p-6 hover:border-primary transition-colors">
                <div className="space-y-4">
                  <div className="flex items-start justify-between gap-4">
                    <div className="flex-1 min-w-0">
                      <h3 className="text-lg font-bold text-foreground mb-1">{job.title}</h3>
                      <p className="text-sm text-muted-foreground mb-3">{job.company}</p>

                      <div className="flex flex-wrap gap-2 mb-4">
                        {job.tags.map((tag) => (
                          <Badge key={tag} variant="secondary" className="bg-secondary text-secondary-foreground">
                            {tag}
                          </Badge>
                        ))}
                      </div>

                      <div className="flex flex-wrap gap-4 text-sm text-muted-foreground">
                        <div className="flex items-center gap-1">
                          <MapPin className="w-4 h-4" />
                          {job.location}
                        </div>
                        <div className="flex items-center gap-1">
                          <DollarSign className="w-4 h-4" />
                          {job.salary}
                        </div>
                        <div className="text-xs">{job.posted}</div>
                      </div>
                    </div>

                    <div className="flex flex-col items-end gap-3">
                      <div className="text-right">
                        <div className="text-2xl font-bold text-accent">{job.matchScore}%</div>
                        <div className="text-xs text-muted-foreground">Match</div>
                      </div>

                      <div className="flex gap-2">
                        <Button
                          variant="outline"
                          size="sm"
                          className="border-border text-foreground hover:bg-muted bg-transparent"
                          onClick={() =>
                            setSaved(saved.includes(job.id) ? saved.filter((id) => id !== job.id) : [...saved, job.id])
                          }
                        >
                          <Heart className={`w-4 h-4 ${saved.includes(job.id) ? "fill-current text-accent" : ""}`} />
                        </Button>
                        <Button className="btn-primary" size="sm">
                          Apply
                        </Button>
                      </div>
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
