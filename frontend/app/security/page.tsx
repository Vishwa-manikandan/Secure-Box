"use client";
import React from 'react';
import { ShieldAlert } from 'lucide-react';

export default function SecurityCenter() {
  return (
    <div className="p-8">
      <h1 className="text-2xl font-bold">Security Center</h1>
      <p className="text-muted-foreground mt-2">Unified view of all repository vulnerabilities and secrets.</p>
      <div className="mt-6 p-8 border-2 border-dashed rounded-xl flex flex-col items-center justify-center text-center space-y-4 bg-muted/30">
        <ShieldAlert className="w-12 h-12 text-muted-foreground" />
        <div className="space-y-1">
          <p className="font-medium">No Active Scans</p>
          <p className="text-sm text-muted-foreground">Start a repository scan to see security intelligence here.</p>
        </div>
        <button className="px-4 py-2 bg-primary text-primary-foreground rounded-md text-sm font-medium">Run New Scan</button>
      </div>
    </div>
  );
}
