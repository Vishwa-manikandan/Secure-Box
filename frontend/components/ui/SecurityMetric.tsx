"use client";
import React from 'react';
import { SecurityMetric as MetricType } from '@/types';
import { cn } from '@/lib/utils';
import { TrendingUp, TrendingDown, Minus } from 'lucide-react';

export const SecurityMetric = ({ label, value, trend, severity }: MetricType & { className?: string }) => {
  const trendIcon = {
    up: <TrendingUp className="w-3 h-3 text-red-500" />,
    down: <TrendingDown className="w-3 h-3 text-green-500" />,
    stable: <Minus className="w-3 h-3 text-muted-foreground" />,
  }[trend];

  const severityColor = {
    Critical: 'text-red-500',
    High: 'text-orange-500',
    Medium: 'text-yellow-500',
    Low: 'text-blue-500',
  }[severity || 'Low'];

  return (
    <div className={cn("p-4 rounded-lg border bg-card", className)}>
      <p className="text-xs font-medium text-muted-foreground mb-1">{label}</p>
      <div className="flex items-baseline gap-2">
        <h3 className={cn("text-2xl font-semibold tracking-tight", severityColor)}>
          {value}
        </h3>
        <span className="flex items-center gap-1 text-xs font-medium text-muted-foreground">
          {trendIcon} {trend === 'down' ? 'improved' : trend === 'up' ? 'increased' : 'stable'}
        </span>
      </div>
    </div>
  );
};
