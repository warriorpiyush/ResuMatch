"use client"

import { RecruiterSidebar } from "@/components/recruiter-sidebar"
import { Card } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { BarChart3, Briefcase, Users, Settings, Star, MessageSquare } from "lucide-react"

const navItems = [
  { label: "Dashboard", href: "/recruiter/dashboard", icon: <BarChart3 className="w-5 h-5" /> },
  { label: "Job Postings", href: "/recruiter/jobs", icon: <Briefcase className="w-5 h-5" />, badge: "5" },
  { label: "Candidates", href: "/recruiter/candidates", icon: <Users className="w-5 h-5" />, badge: "24" },
  { label: "Settings", href: "/recruiter/settings", icon: <Settings className="w-5 h-5" /> },
]

const candidates = [
  {
    id: 1,
    name: "Sarah Johnson",
    title: "Senior Software Engineer",
    matchScore: 95,
    status: "Interview Scheduled",
    appliedFor: "Senior Software Engineer",
    avatar: "🧑‍💼",
  },
  {
    id: 2,
    name: "Michael Chen",
    title: "Full Stack Developer",
    matchScore: 88,
    status: "Under Review",
    appliedFor: "Full Stack Developer",
    avatar: "👨‍💼",
  },
  {
    id: 3,
    name: "Emma Davis",
    title: "Product Manager",
    matchScore: 82,
    status: "Rejected",
    appliedFor: "Product Manager",
    avatar: "👩‍💼",
  },
  {
    id: 4,
    name: "Alex Martinez",
    title: "UX/UI Designer",
    matchScore: 91,
    status: "Offer Sent",
    appliedFor: "UX/UI Designer",
    avatar: "🧑‍💼",
  },
]

export default function CandidatesPage() {
  return (
    <div className="flex h-screen bg-background">
      <RecruiterSidebar items={navItems} title="Recruiter" subtitle="Candidates" />

      <main className="flex-1 overflow-auto md:ml-0">
        <div className="p-6 md:p-8 max-w-6xl mx-auto space-y-8">
          <div className="pt-12 md:pt-0">
            <h1 className="text-4xl font-bold text-foreground mb-2">Candidates</h1>
            <p className="text-muted-foreground">Review and manage candidates across all positions</p>
          </div>

          <div className="space-y-4">
            {candidates.map((candidate) => (
              <Card
                key={candidate.id}
                className="border border-border bg-card p-6 hover:border-primary transition-colors"
              >
                <div className="flex items-start justify-between gap-4">
                  <div className="flex items-start gap-4 flex-1">
                    <div className="text-3xl">{candidate.avatar}</div>
                    <div className="flex-1 min-w-0">
                      <h3 className="text-lg font-bold text-foreground">{candidate.name}</h3>
                      <p className="text-sm text-muted-foreground mb-1">{candidate.title}</p>
                      <p className="text-xs text-accent">Applied for: {candidate.appliedFor}</p>
                    </div>
                  </div>

                  <div className="flex items-center gap-6">
                    <div className="text-right">
                      <div className="text-2xl font-bold text-accent">{candidate.matchScore}%</div>
                      <div className="text-xs text-muted-foreground">Match</div>
                    </div>

                    <div
                      className={`px-3 py-1 rounded-full text-xs font-medium whitespace-nowrap ${
                        candidate.status === "Interview Scheduled"
                          ? "bg-accent text-accent-foreground"
                          : candidate.status === "Offer Sent"
                            ? "bg-primary text-primary-foreground"
                            : candidate.status === "Under Review"
                              ? "bg-secondary text-secondary-foreground"
                              : "bg-destructive text-destructive-foreground"
                      }`}
                    >
                      {candidate.status}
                    </div>

                    <div className="flex gap-2">
                      <Button
                        variant="outline"
                        size="sm"
                        className="border-border text-foreground hover:bg-muted gap-2 bg-transparent"
                      >
                        <Star className="w-4 h-4" />
                      </Button>
                      <Button
                        variant="outline"
                        size="sm"
                        className="border-border text-foreground hover:bg-muted gap-2 bg-transparent"
                      >
                        <MessageSquare className="w-4 h-4" />
                      </Button>
                      <Button className="btn-primary" size="sm">
                        View
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
