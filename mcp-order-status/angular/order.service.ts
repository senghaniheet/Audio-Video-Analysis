/**
 * Angular Service for Order Status Checking via SSE
 */
import { Injectable } from '@angular/core';
import { Observable, Subject } from 'rxjs';

export interface OrderStatusEvent {
  stage?: string;
  message?: string;
  mobile?: string;
  order_id?: string;
  status?: string;
  error?: string;
}

@Injectable({
  providedIn: 'root'
})
export class OrderService {
  private apiUrl = 'http://localhost:3000/api/order-status-stream';

  /**
   * Check order status using SSE
   * @param text - Input text (transcribed audio)
   * @returns Observable that emits order status events
   */
  checkOrderStatus(text: string): Observable<OrderStatusEvent> {
    const subject = new Subject<OrderStatusEvent>();

    // Create EventSource for SSE
    const eventSource = new EventSource(`${this.apiUrl}?text=${encodeURIComponent(text)}`);

    // Listen for processing event
    eventSource.addEventListener('processing', (event: MessageEvent) => {
      try {
        const data = JSON.parse(event.data);
        subject.next(data);
      } catch (e) {
        subject.next({ stage: 'processing', message: 'Processing...' });
      }
    });

    // Listen for extracting_keywords event
    eventSource.addEventListener('extracting_keywords', (event: MessageEvent) => {
      try {
        const data = JSON.parse(event.data);
        subject.next(data);
      } catch (e) {
        subject.next({ stage: 'extracting_keywords', message: 'Extracting keywords...' });
      }
    });

    // Listen for excel_lookup event
    eventSource.addEventListener('excel_lookup', (event: MessageEvent) => {
      try {
        const data = JSON.parse(event.data);
        subject.next(data);
      } catch (e) {
        subject.next({ stage: 'excel_lookup', message: 'Looking up in database...' });
      }
    });

    // Listen for final_result event
    eventSource.addEventListener('final_result', (event: MessageEvent) => {
      try {
        const data = JSON.parse(event.data);
        subject.next({
          mobile: data.mobile || '',
          order_id: data.order_id || '',
          status: data.status || '',
          message: data.message || ''
        });
        subject.complete();
        eventSource.close();
      } catch (e) {
        subject.error({ error: 'Error parsing final result' });
        eventSource.close();
      }
    });

    // Listen for error event
    eventSource.addEventListener('error', (event: MessageEvent) => {
      try {
        const data = JSON.parse(event.data);
        subject.error(data);
      } catch (e) {
        subject.error({ error: 'Unknown error occurred' });
      }
      eventSource.close();
    });

    // Handle connection errors
    eventSource.onerror = (error) => {
      subject.error({ error: 'Connection error occurred' });
      eventSource.close();
    };

    return subject.asObservable();
  }

  /**
   * Alternative: Check order status using REST API (non-SSE)
   * @param text - Input text (transcribed audio)
   * @returns Promise with order status result
   */
  async checkOrderStatusRest(text: string): Promise<OrderStatusEvent> {
    try {
      const response = await fetch('http://localhost:3000/api/order-status', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({ text })
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const data = await response.json();
      return {
        mobile: data.mobile || '',
        order_id: data.order_id || '',
        status: data.status || '',
        message: data.message || ''
      };
    } catch (error) {
      throw { error: error instanceof Error ? error.message : 'Unknown error' };
    }
  }
}

