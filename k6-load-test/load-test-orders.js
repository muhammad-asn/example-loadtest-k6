import http from 'k6/http';
import { check } from 'k6';

export default function () {
    const url = 'http://order-service:8000/orders/';
    const payload = JSON.stringify({ user_id: 1, item: 'Item1' });

    const params = {
        headers: {
            'Content-Type': 'application/json',
        },
    };

    const res = http.post(url, payload, params);
    check(res, {
        'is status 200': (r) => r.status === 200,
    });
}