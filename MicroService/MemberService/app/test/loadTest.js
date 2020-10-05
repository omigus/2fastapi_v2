import http from 'k6/http';
import { sleep } from 'k6';
export let options = {
  vus: 100,
  iterations: 100,
};
export default function () {
  var url = 'http://127.0.0.1:8000/api/v2/projects';
  var token = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJtZW1iZXJfcHVibGljX2lkIjoiYmQzNzQ4MGEtZWNmMy00OGMyLThiNGMtMDAyMjMwZWQ4MWQyIiwiYWRtaW5faWQiOiIyIiwiY29tcGFueV9pZCI6IjMiLCJleHAiOjE2MDI0ODMyMjJ9.WGLRdcSm6x81Jh2v53HzdwcgXKdORSlgldv0GQGf1Vs'

  var params = {
    headers: {
      'Content-Type': 'application/json',
      'Authorization': 'Bearer ' + token
    },
  };

  http.get(url, params);

  sleep(1);
}