import http from 'k6/http';
import { check } from 'k6';

export default function () {
    const url = 'http://order-service:8000/health/';
    
    const res = http.get(url);
    check(res, {
        'is status 200': (r) => r.status === 200,
    });
}