"use client";
import React from 'react';
import { Search, Bell, ChevronDown, Globe } from 'lucide-react';
import { cn } from '@/lib/utils';

export const TopNav = () => {
  return (
    <header className="h-14 border-b border-border bg-background/80 backdrop-blur-md sticky top-0 z-10 flex items-center justify-between px-6">
      <div className="flex items-center gap-4">
        <div className="flex items-center gap-2 px-3 py-1.5 rounded-md border border-border bg-muted/30 cursor-pointer hover:bg-muted transition-colors group">
          <Globe className="w-3.5 h-3.5 text-muted-foreground" />
          <span className="text-xs font-medium">Main Production</span>
          <ChevronDown className="w-3.5 h-3.5 text-muted-foreground" />
        </div>
      </div>

      <div className="flex items-center gap-4">
        <div className="relative group">
          <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-3.5 h-3.5 text-muted-foreground group-focus-within:text-foreground transition-colors" />
          <input 
            type="text" 
            placeholder="Search resources... (⌘K)" 
            className="pl-9 pr-4 py-1.5 text-xs rounded-md border border-border bg-muted/50 focus:bg-background focus:ring-1 focus:ring-ring outline-none w-64 transition-all"
          />
        </div>
        <button className="p-2 rounded-md hover:bg-muted relative transition-colors">
          <Bell className="w-4 h-4 text-muted-foreground" />
          <span className="absolute top-2 right-2 w-2 h-2 bg-red-500 rounded-full border-2 border-background"></span>
        </button>
      </div>
    </header>
  );
};
