export type Severity = 'Low' | 'Medium' | 'High' | 'Critical';

export interface SecurityMetric {
  label: string;
  value: string | number;
  trend: 'up' | 'down' | 'stable';
  severity?: Severity;
}

export interface Finding {
  id: string;
  title: string;
  severity: Severity;
  file: string;
  line: number;
  description: string;
  status: 'Open' | 'Fixed' | 'Ignored';
}

export interface Repository {
  id: string;
  name: string;
  lastScan: string;
  findingsCount: number;
  status: 'Secure' | 'Warning' | 'Critical';
}
