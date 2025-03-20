import { Routes } from '@angular/router';
import { DashboardComponent } from './components/dashboard/dashboard.component';
import { TransactionAnalysisComponent } from './components/transaction-analysis/transaction-analysis.component';

export const routes: Routes = [
  { path: 'dashboard', component: DashboardComponent },
  { path: 'analysis', component: TransactionAnalysisComponent },
  { path: '', redirectTo: '/dashboard', pathMatch: 'full' }, 
];
