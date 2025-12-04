"use client"

import type React from "react"

import { RecruiterSidebar } from "@/components/recruiter-sidebar"
import { Card } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { BarChart3, Briefcase, Users, Settings } from "lucide-react"
import { useState } from "react"

const navItems = [
  { label: "Dashboard", href: "/recruiter/dashboard", icon: <BarChart3 className="w-5 h-5" /> },
  { label: "Job Postings", href: "/recruiter/jobs", icon: <Briefcase className="w-5 h-5" />, badge: "5" },
  { label: "Candidates", href: "/recruiter/candidates", icon: <Users className="w-5 h-5" />, badge: "24" },
  { label: "Settings", href: "/recruiter/settings", icon: <Settings className="w-5 h-5" /> },
]

export default function RecruiterSettings() {
  const [formData, setFormData] = useState({
    companyName: "Tech Corp",
    email: "hr@techcorp.com",
    phone: "+1 (555) 123-4567",
    website: "www.techcorp.com",
    industry: "Technology",
  })

  const handleChange = (e: React.ChangeEvent<HTMLInputElement | HTMLSelectElement>) => {
    const { name, value } = e.target
    setFormData((prev) => ({ ...prev, [name]: value }))
  }

  return (
    <div className="flex h-screen bg-background">
      <RecruiterSidebar items={navItems} title="Recruiter" subtitle="Settings" />

      <main className="flex-1 overflow-auto md:ml-0">
        <div className="p-6 md:p-8 max-w-2xl mx-auto space-y-8">
          <div className="pt-12 md:pt-0">
            <h1 className="text-4xl font-bold text-foreground mb-2">Settings</h1>
            <p className="text-muted-foreground">Manage your company profile and preferences</p>
          </div>

          <Card className="border border-border bg-card p-8 space-y-6">
            <div>
              <h3 className="text-lg font-bold text-foreground mb-1">Company Information</h3>
              <p className="text-sm text-muted-foreground">Update your company details</p>
            </div>

            <div className="space-y-6">
              <div className="space-y-2">
                <label className="block text-sm font-medium text-foreground">Company Name</label>
                <Input
                  name="companyName"
                  value={formData.companyName}
                  onChange={handleChange}
                  className="bg-background border-border text-foreground"
                />
              </div>

              <div className="space-y-2">
                <label className="block text-sm font-medium text-foreground">Email</label>
                <Input
                  name="email"
                  type="email"
                  value={formData.email}
                  onChange={handleChange}
                  className="bg-background border-border text-foreground"
                />
              </div>

              <div className="space-y-2">
                <label className="block text-sm font-medium text-foreground">Phone</label>
                <Input
                  name="phone"
                  value={formData.phone}
                  onChange={handleChange}
                  className="bg-background border-border text-foreground"
                />
              </div>

              <div className="space-y-2">
                <label className="block text-sm font-medium text-foreground">Website</label>
                <Input
                  name="website"
                  value={formData.website}
                  onChange={handleChange}
                  className="bg-background border-border text-foreground"
                />
              </div>

              <div className="space-y-2">
                <label className="block text-sm font-medium text-foreground">Industry</label>
                <select
                  name="industry"
                  value={formData.industry}
                  onChange={handleChange}
                  className="w-full px-3 py-2 rounded-lg bg-background border border-border text-foreground"
                >
                  <option>Technology</option>
                  <option>Finance</option>
                  <option>Healthcare</option>
                  <option>Retail</option>
                  <option>Other</option>
                </select>
              </div>

              <Button className="btn-primary">Save Changes</Button>
            </div>
          </Card>
        </div>
      </main>
    </div>
  )
}
