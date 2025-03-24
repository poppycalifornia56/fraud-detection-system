import { Component, OnInit } from '@angular/core';
import { ApiService } from '../../services/api.service';
import { Transaction } from '../../models/models';
import { HighchartsChartModule } from 'highcharts-angular';
import * as Highcharts from 'highcharts';
import 'highcharts/modules/heatmap';
import { MatCardModule } from '@angular/material/card';
import { MatProgressSpinnerModule } from '@angular/material/progress-spinner';
import { MatTableModule } from '@angular/material/table';
import { MatIconModule } from '@angular/material/icon';
import { CommonModule } from '@angular/common';
import { TableModule } from 'primeng/table';
import { CardModule } from 'primeng/card';
import { ProgressSpinnerModule } from 'primeng/progressspinner';

@Component({
  selector: 'app-transaction-analysis',
  standalone: true,
  imports: [
    HighchartsChartModule,
    MatCardModule,
    MatProgressSpinnerModule,
    MatTableModule,
    MatIconModule,
    CommonModule,
    TableModule,
    CardModule,
    ProgressSpinnerModule,
  ],
  templateUrl: './transaction-analysis.component.html',
  styleUrls: ['./transaction-analysis.component.scss'],
})
export class TransactionAnalysisComponent implements OnInit {
  transactions: Transaction[] = [];
  loading = true;

  // Highcharts configuration
  highcharts = Highcharts;
  heatmapOptions: Highcharts.Options = {};

  constructor(private apiService: ApiService) {}

  ngOnInit(): void {
    this.fetchData();
  }

  fetchData(): void {
    this.loading = true;

    // Get transactions
    this.apiService.getTransactions(0, 1000).subscribe(
      (data) => {
        this.transactions = data;
        this.loading = false;
        this.createHeatmap();
      },
      (error) => {
        console.error('Error fetching transactions', error);
        this.loading = false;
      }
    );
  }

  createHeatmap(): void {
    // Skip if no data
    if (!this.transactions.length) {
      return;
    }

    // Get departments and vendors
    const departments = [
      ...new Set(this.transactions.map((t) => t.department_id)),
    ];
    const vendors = [...new Set(this.transactions.map((t) => t.vendor_id))];

    // Create heatmap data
    const heatmapData: [number, number, number, number][] = [];
    departments.forEach((dept, deptIndex) => {
      vendors.forEach((vendor, vendorIndex) => {
        // Find transactions between this dept and vendor
        const relevantTransactions = this.transactions.filter(
          (t) => t.department_id === dept && t.vendor_id === vendor
        );

        // Calculate average risk score
        let avgRisk = 0;
        if (relevantTransactions.length) {
          avgRisk =
            relevantTransactions.reduce((sum, t) => sum + t.risk_score, 0) /
            relevantTransactions.length;
        }

        // Add transaction count as the fourth element
        heatmapData.push([
          vendorIndex,
          deptIndex,
          avgRisk,
          relevantTransactions.length,
        ]);
      });
    });

    // Set up Highcharts heatmap
    this.heatmapOptions = {
      chart: {
        type: 'heatmap',
        height: 600,
      },
      title: {
        text: 'Department-Vendor Risk Heatmap',
      },
      xAxis: {
        categories: vendors.map(String),
        title: {
          text: 'Vendors',
        },
      },
      yAxis: {
        categories: departments.map(String),
        title: {
          text: 'Departments',
        },
      },
      colorAxis: {
        min: 0,
        max: 1,
        minColor: '#FFFFFF',
        maxColor: Highcharts.getOptions().colors?.[0] || '#0000FF',
      },
      series: [
        {
          name: 'Risk Score',
          type: 'heatmap',
          data: heatmapData,
          dataLabels: {
            enabled: true,
            format: '{point.value:.2f}',
          },
          tooltip: {
            pointFormatter: function () {
              const point = this as any;
              return `<b>Vendor:</b> ${vendors[point.x]}<br>
                      <b>Department:</b> ${departments[point.y]}<br>
                      <b>Risk Score:</b> ${point.value?.toFixed(2)}<br>
                      <b>Transactions:</b> ${point.count}`;
            },
          },
        },
      ],
    };
  }

  getHighRiskTransactions(): Transaction[] {
    // Return top 10 highest risk transactions
    return [...this.transactions]
      .sort((a, b) => b.risk_score - a.risk_score)
      .slice(0, 10);
  }

  getRiskClass(transaction: Transaction): string {
    if (transaction.risk_score >= 0.8) return 'very-high-risk';
    if (transaction.risk_score >= 0.6) return 'high-risk';
    if (transaction.risk_score >= 0.4) return 'medium-risk';
    if (transaction.risk_score >= 0.2) return 'low-risk';
    return 'very-low-risk';
  }
}
