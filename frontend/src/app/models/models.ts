export interface Transaction {
    id: number;
    transaction_date: string;
    amount: number;
    vendor_id: number;
    department_id: number;
    description: string;
    is_flagged: boolean;
    risk_score: number;
  }
  
  export interface Alert {
    id: number;
    transaction_id: number;
    creation_date: string;
    severity: number;
    description: string;
    is_resolved: boolean;
  }