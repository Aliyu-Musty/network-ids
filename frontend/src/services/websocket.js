const WS_URL = import.meta.env.VITE_WS_URL || 'ws://localhost:8000/ws/alerts';

export class LiveAlertSocket {
  constructor(onMessageCallback) {
    this.url = WS_URL;
    this.onMessage = onMessageCallback;
    this.ws = null;
  }

  connect() {
    this.ws = new WebSocket(this.url);

    this.ws.onopen = () => {
      console.log('Connected to Real-Time Network Alert WebSocket stream');
    };

    this.ws.onmessage = (event) => {
      try {
        const data = JSON.parse(event.data);
        if (this.onMessage) {
          this.onMessage(data);
        }
      } catch (err) {
        console.error('Failed to parse incoming WebSocket message', err);
      }
    };

    this.ws.onclose = () => {
      console.warn('WebSocket connection closed. Attempting reconnect in 3s...');
      setTimeout(() => this.connect(), 3000);
    };

    this.ws.onerror = (err) => {
      console.error('WebSocket error:', err);
      this.ws.close();
    };
  }

  disconnect() {
    if (this.ws) {
      this.ws.close();
    }
  }
}
