"use client";
import React from 'react';
import { Severity } from '@/types';
import { cn } from '@/lib/utils';

export const SeverityIndicator = ({ severity, className }: { severity: Severity; className?: string }) => {
  const styles = {
    Critical: 'bg-red-500/10 text-red-500 border-red-500/20',
    High: 'bg-orange-500/10 text-orange-500 border-orange-500/20',
    Medium: 'bg-yellow-500/10 text-yellow-500 border-yellow-500/20',
    Low: 'bg-blue-500/10 text-blue-500 border-blue-500/20',
  };

  return (
    <span className={cn(
      "px-2 py-0.5 rounded-full text-[10px] font-bold uppercase tracking-wider border",
      styles[severity],
      className
    )}>
      {severity}
    </span>
  );
};
