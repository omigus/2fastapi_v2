import http from 'k6/http';
import { sleep } from 'k6';
export let options = {
  vus: 100,
  iterations: 1000,
};
export default function () {
  var url = 'http://127.0.0.1:8000/';
  var token = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJtZW1iZXJfcHVibGljX2lkIjoiYzg0ZTNjODUtMTM2Yi00YzExLWIwN2YtMzQyMTQwMzBjYmQwIiwiYWRtaW5faWQiOiIxIiwiY29tcGFueV9pZCI6IjMiLCJleHAiOjE2MDIwNTQ0MTN9.MZz0d87CyV107x_F0JGq8oUDc2o1wb_MJNu1DoqOAj0'

  var params = {
    headers: {
      'Content-Type': 'application/json',
      'Authorization': 'Bearer ' + token
    },
  };

  http.get(url, params);

  sleep(1);
}