import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { Transaction, Alert } from '../models/models';

@Injectable({
  providedIn: 'root'
})
export class ApiService {
  private apiUrl = 'http://localhost:8000';

  constructor(private http: HttpClient) { }

  getTransactions(skip: number = 0, limit: number = 100): Observable<Transaction[]> {
    return this.http.get<Transaction[]>(`${this.apiUrl}/transactions/?skip=${skip}&limit=${limit}`);
  }

  createTransaction(transaction: any): Observable<Transaction> {
    return this.http.post<Transaction>(`${this.apiUrl}/transactions/`, transaction);
  }

  getAlerts(skip: number = 0, limit: number = 100): Observable<Alert[]> {
    return this.http.get<Alert[]>(`${this.apiUrl}/alerts/?skip=${skip}&limit=${limit}`);
  }
}