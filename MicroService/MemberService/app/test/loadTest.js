import http from 'k6/http';
import { sleep } from 'k6';
export let options = {
  vus: 100,
  iterations: 200,
};
export default function() {
  http.get('http://127.0.0.1:5000/api/v1/');
  sleep(1);
}