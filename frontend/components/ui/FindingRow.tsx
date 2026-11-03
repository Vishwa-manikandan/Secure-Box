"use client";
import React from 'react';
import { Finding } from '@/types';
import { SeverityIndicator } from './SeverityIndicator';
import { FileText, AlertCircle, CheckCircle2, Clock } from 'lucide-react';

export const FindingRow = ({ finding }: { finding: Finding }) => {
  return (
    <div className="group flex items-center justify-between p-3 border-b border-border hover:bg-muted/50 transition-colors cursor-pointer">
      <div className="flex items-center gap-4 overflow-hidden">
        <div className="flex-shrink-0">
          {finding.status === 'Fixed' ? (
            <CheckCircle2 className="w-4 h-4 text-green-500" />
          ) : finding.status === 'Ignored' ? (
            <Clock className="w-4 h-4 text-muted-foreground" />
          ) : (
            <AlertCircle className="w-4 h-4 text-red-500" />
          )}
        </div>
        <div className="flex flex-col overflow-hidden">
          <span className="text-sm font-medium truncate">{finding.title}</span>
          <div className="flex items-center gap-2 text-xs text-muted-foreground">
            <FileText className="w-3 h-3" />
            <span className="truncate">{finding.file}:{finding.line}</span>
          </div>
        </div>
      </div>
      <div className="flex items-center gap-4">
        <SeverityIndicator severity={finding.severity} />
        <span className="text-xs text-muted-foreground w-16 text-right">{finding.status}</span>
      </div>
    </div>
  );
};
