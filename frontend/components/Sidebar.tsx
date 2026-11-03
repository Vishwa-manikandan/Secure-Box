"use client";
import React, { useState } from 'react';
import { cn } from '@/lib/utils';
import { 
  LayoutDashboard, 
  Github, 
  ShieldAlert, 
  Code2, 
  Wrench, 
  Cpu, 
  Library, 
  GitMerge, 
  History, 
  Settings,
  ChevronRight,
  Command
} from 'lucide-react';
import Link from 'next/link';
import { usePathname } from 'next/navigation';

const NAVIGATION = [
  { name: 'Dashboard', href: '/', icon: LayoutDashboard },
  { name: 'Repositories', href: '/repositories', icon: Github },
  { name: 'Security Center', href: '/security', icon: ShieldAlert },
  { name: 'Code Review', href: '/review', icon: Code2 },
  { name: 'Auto Repair', href: '/repair', icon: Wrench },
  { name: 'Skill Studio', href: '/studio', icon: Cpu },
  { name: 'Skill Library', href: '/library', icon: Library },
  { name: 'Workflows', href: '/workflows', icon: GitMerge },
  { name: 'Scan History', href: '/history', icon: History },
  { name: 'Settings', href: '/settings', icon: Settings },
];

export const Sidebar = () => {
  const pathname = usePathname();

  return (
    <aside className="fixed left-0 top-0 h-screen w-64 border-r border-border bg-background flex flex-col">
      <div className="p-4 flex items-center gap-3">
        <div className="w-8 h-8 bg-primary rounded-lg flex items-center justify-center text-primary-foreground">
          <Command className="w-5 h-5" />
        </div>
        <span className="font-bold tracking-tight text-lg">Securebox</span>
      </div>

      <nav className="flex-1 px-3 py-4 space-y-1 overflow-y-auto">
        {NAVIGATION.map((item) => {
          const isActive = pathname === item.href;
          return (
            <Link
              key={item.name}
              href={item.href}
              className={cn(
                "flex items-center justify-between px-3 py-2 rounded-md text-sm font-medium transition-colors group",
                isActive 
                  ? "bg-secondary text-foreground" 
                  : "text-muted-foreground hover:bg-muted hover:text-foreground"
              )}
            >
              <div className="flex items-center gap-3">
                <item.icon className={cn("w-4 h-4", isActive ? "text-foreground" : "text-muted-foreground group-hover:text-foreground")} />
                {item.name}
              </div>
              {isActive && <ChevronRight className="w-3 h-3" />}
            </Link>
          );
        })}
      </nav>

      <div className="p-4 border-t border-border">
        <div className="flex items-center gap-3 p-2 rounded-lg hover:bg-muted cursor-pointer transition-colors">
          <div className="w-8 h-8 rounded-full bg-muted-foreground/20 flex items-center justify-center text-xs font-bold">
            JD
          </div>
          <div className="flex-1 overflow-hidden">
            <p className="text-xs font-medium truncate">John Doe</p>
            <p className="text-[10px] text-muted-foreground truncate">Enterprise Plan</p>
          </div>
          <Settings className="w-4 h-4 text-muted-foreground" />
        </div>
      </div>
    </aside>
  );
};
