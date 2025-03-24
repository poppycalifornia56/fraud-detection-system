import { Component, OnInit } from '@angular/core';
import { ApiService } from '../../services/api.service';
import { Transaction, Alert } from '../../models/models';
import { HighchartsChartModule } from 'highcharts-angular';
import Highcharts from 'highcharts';
import { MatCardModule } from '@angular/material/card';
import { MatProgressSpinnerModule } from '@angular/material/progress-spinner';
import { MatListModule } from '@angular/material/list';
import { MatIconModule } from '@angular/material/icon';
import { CommonModule } from '@angular/common';
import { TableModule } from 'primeng/table';
import { CardModule } from 'primeng/card';
import { ProgressSpinnerModule } from 'primeng/progressspinner';


@Component({
  selector: 'app-dashboard',
  standalone: true,
  imports: [
    HighchartsChartModule,
    MatCardModule,
    MatProgressSpinnerModule,
    MatListModule,
    MatIconModule,
    CommonModule,
    TableModule,
    CardModule,
    ProgressSpinnerModule
  ],
  templateUrl: './dashboard.component.html',
  styleUrls: ['./dashboard.component.scss'],
})
export class DashboardComponent implements OnInit {
  transactions: Transaction[] = [];
  alerts: Alert[] = [];
  loading = true;

  // Highcharts configuration
  highcharts = Highcharts;
  chartOptions: Highcharts.Options = {};

  constructor(private apiService: ApiService) {}

  ngOnInit(): void {
    this.fetchData();
  }

  getFlaggedTransactionsLength(): number {
  return this.transactions.filter(t => t.is_flagged).length;
}

  fetchData(): void {
    this.loading = true;

    // Get transactions
    this.apiService.getTransactions(0, 1000).subscribe(
      (data) => {
        this.transactions = data;
        this.loading = false;
        this.updateChart();
      },
      (error) => {
        console.error('Error fetching transactions', error);
        this.loading = false;
      }
    );

    // Get alerts
    this.apiService.getAlerts().subscribe(
      (data) => {
        this.alerts = data;
      },
      (error) => {
        console.error('Error fetching alerts', error);
      }
    );
  }

  updateChart(): void {
    const riskDistribution = this.getRiskDistribution();

    this.chartOptions = {
      chart: {
        type: 'column',
      },
      title: {
        text: 'Transaction Risk Distribution',
      },
      xAxis: {
        categories: riskDistribution.map((bucket) => bucket.name),
        title: {
          text: 'Risk Level',
        },
      },
      yAxis: {
        title: {
          text: 'Number of Transactions',
        },
      },
      series: [
        {
          name: 'Transactions',
          type: 'column',
          data: riskDistribution.map((bucket) => bucket.value),
          colorByPoint: true,
        },
      ],
    };
  }

  getRiskDistribution() {
    // Create risk buckets (0-0.2, 0.2-0.4, etc.)
    const buckets = [
      { name: 'Very Low', value: 0 },
      { name: 'Low', value: 0 },
      { name: 'Medium', value: 0 },
      { name: 'High', value: 0 },
      { name: 'Very High', value: 0 },
    ];

    // Count transactions in each bucket
    this.transactions.forEach((t) => {
      if (t.risk_score < 0.2) buckets[0].value++;
      else if (t.risk_score < 0.4) buckets[1].value++;
      else if (t.risk_score < 0.6) buckets[2].value++;
      else if (t.risk_score < 0.8) buckets[3].value++;
      else buckets[4].value++;
    });

    return buckets;
  }
}
