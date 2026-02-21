"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import {
  LayoutDashboard,
  CheckSquare,
  FileText,
  Calendar,
  Users,
  Building2,
  Brain,
  Menu,
  X,
  FlaskConical,
} from "lucide-react";
import { useState } from "react";
import { cn } from "@/lib/utils";

const navigation = [
  { name: "Dashboard", href: "/", icon: LayoutDashboard },
  { name: "Tasks", href: "/task-board", icon: CheckSquare },
  { name: "Content", href: "/content-pipeline", icon: FileText },
  { name: "Calendar", href: "/calendar", icon: Calendar },
  { name: "Memory", href: "/memory", icon: Brain },
  { name: "Team", href: "/team", icon: Users },
  { name: "Office", href: "/office", icon: Building2 },
  { name: "Peptides", href: "/peptide-inventory.html", icon: FlaskConical },
];

export function Sidebar() {
  const pathname = usePathname();
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false);

  return (
    <>
      {/* Mobile menu button */}
      <button
        onClick={() => setMobileMenuOpen(!mobileMenuOpen)}
        className="lg:hidden fixed top-4 left-4 z-50 p-2 rounded-md bg-[#141414] text-white"
      >
        {mobileMenuOpen ? <X size={24} /> : <Menu size={24} />}
      </button>

      {/* Sidebar */}
      <aside
        className={cn(
          "fixed left-0 top-0 h-full w-64 bg-[#0a0a0a] border-r border-[#1e1e1e] z-40 transition-transform lg:translate-x-0",
          mobileMenuOpen ? "translate-x-0" : "-translate-x-full"
        )}
      >
        <div className="flex flex-col h-full">
          {/* Logo */}
          <div className="p-6 border-b border-[#1e1e1e]">
            <h1 className="text-xl font-bold text-white">Mission Control</h1>
            <p className="text-sm text-gray-400 mt-1">AI Dashboard</p>
          </div>

          {/* Navigation */}
          <nav className="flex-1 p-4 space-y-1">
            {navigation.map((item) => {
              const isActive = pathname === item.href;
              return (
                <Link
                  key={item.name}
                  href={item.href}
                  onClick={() => setMobileMenuOpen(false)}
                  className={cn(
                    "flex items-center gap-3 px-4 py-3 rounded-lg transition-colors",
                    isActive
                      ? "bg-[#1e1e1e] text-white"
                      : "text-gray-400 hover:bg-[#141414] hover:text-white"
                  )}
                >
                  <item.icon size={20} />
                  <span className="font-medium">{item.name}</span>
                </Link>
              );
            })}
          </nav>

          {/* Footer */}
          <div className="p-4 border-t border-[#1e1e1e]">
            <div className="flex items-center gap-3">
              <div className="w-8 h-8 rounded-full bg-gradient-to-br from-blue-500 to-purple-500" />
              <div className="flex-1">
                <p className="text-sm font-medium text-white">Jason</p>
                <p className="text-xs text-gray-400">Owner</p>
              </div>
            </div>
          </div>
        </div>
      </aside>

      {/* Overlay for mobile */}
      {mobileMenuOpen && (
        <div
          className="lg:hidden fixed inset-0 bg-black/50 z-30"
          onClick={() => setMobileMenuOpen(false)}
        />
      )}
    </>
  );
}
