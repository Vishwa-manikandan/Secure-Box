"use client";
import React from 'react';
import { SecurityMetric } from '@/components/ui/SecurityMetric';
import { FindingRow } from '@/components/ui/FindingRow';
import { ShieldAlert, CheckCircle, AlertTriangle, Zap } from 'lucide-react';

const MOCK_METRICS = [
  { label: 'Critical Findings', value: 12, trend: 'down', severity: 'Critical' },
  { label: 'High Severity', value: 45, trend: 'up', severity: 'High' },
  { label: 'Medium Severity', value: 128, trend: 'stable', severity: 'Medium' },
  { label: 'Total Scanned Files', value: '1.2k', trend: 'up', severity: 'Low' },
];

const MOCK_FINDINGS = [
  { id: '1', title: 'Hardcoded AWS Access Key', severity: 'Critical', file: 'src/config/aws.ts', line: 12, description: 'Plaintext API key detected', status: 'Open' },
  { id: '2', title: 'SQL Injection Vulnerability', severity: 'High', file: 'app/api/user.py', line: 45, description: 'Unsanitized input in query', status: 'Open' },
  { id: '3', title: 'Insecure Dependency Version', severity: 'Medium', file: 'package.json', line: 10, description: 'Outdated lodash version', status: 'Fixed' },
  { id: '4', title: 'Missing CSRF Protection', severity: 'High', file: 'app/auth.py', line: 102, description: 'Missing validation token', status: 'Ignored' },
  { id: '5', title: 'Exposed .env file', severity: 'Critical', file: '.env', line: 1, description: 'Environment file public', status: 'Open' },
];

export default function Dashboard() {
  return (
    <div className="space-y-8">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold tracking-tight">Security Overview</h1>
          <p className="text-muted-foreground text-sm">Real-time security posture across your organization.</p>
        </div>
        <div className="flex gap-3">
          <button className="px-4 py-2 text-xs font-medium bg-muted hover:bg-muted/80 rounded-md transition-colors border border-border">
            Export Report
          </button>
          <button className="px-4 py-2 text-xs font-medium bg-primary text-primary-foreground hover:bg-primary/90 rounded-md transition-colors shadow-sm">
            Run New Scan
          </button>
        </div>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
        {MOCK_METRICS.map((m, i) => (
          <SecurityMetric key={i} {...m} />
        ))}
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <div className="lg:col-span-2 space-y-4">
          <div className="flex items-center justify-between">
            <h2 className="text-lg font-semibold flex items-center gap-2">
              <ShieldAlert className="w-5 h-5 text-red-500" />
              Top Critical Findings
            </h2>
            <button className="text-xs text-primary hover:underline font-medium">View All</button>
          </div>
          <div className="border border-border rounded-lg bg-card overflow-hidden">
            <div className="grid grid-cols-1 px-4 py-2 border-b border-border bg-muted/30 text-[10px] font-bold text-muted-foreground uppercase tracking-wider">
              <span>Finding Details</span>
              <span className="text-right">Severity & Status</span>
            </div>
            <div className="divide-y divide-border">
              {MOCK_FINDINGS.map((f) => (
                <FindingRow key={f.id} finding={f} />
              ))}
            </div>
          </div>
        </div>

        <div className="space-y-4">
          <h2 className="text-lg font-semibold flex items-center gap-2">
            <Zap className="w-5 h-5 text-yellow-500" />
            Quick Actions
          </h2>
          <div className="grid grid-cols-1 gap-3">
            {[
              { label: 'Scan current branch', icon: Github, desc: 'Analyze latest commits' },
              { label: 'Review Skill Studio', icon: Cpu, desc: 'Optimize agent skills' },
              { label: 'Check Auto-Repair', icon: Wrench, desc: 'Apply pending fixes' },
            ].map((action, i) => (
              <button key={i} className="flex items-start gap-3 p-3 rounded-lg border border-border bg-card hover:bg-muted/50 transition-all text-left group">
                <div className="p-2 rounded-md bg-muted group-hover:bg-primary group-hover:text-primary-foreground transition-colors">
                  <action.icon className="w-4 h-4" />
                </div>
                <div>
                  <p className="text-xs font-medium">{action.label}</p>
                  <p className="text-[10px] text-muted-foreground">{action.desc}</p>
                </div>
              </button>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
}
