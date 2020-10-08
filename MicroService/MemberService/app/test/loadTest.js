
import http from 'k6/http';
import { sleep } from 'k6';
export let options = {
  vus: 1000,
  iterations: 3000,
};

let count = 0;

export default function () {
  var url = 'http://127.0.0.1:8000/api/v2/projects';
  var token = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJtZW1iZXJfcHVibGljX2lkIjoiYzg0ZTNjODUtMTM2Yi00YzExLWIwN2YtMzQyMTQwMzBjYmQwIiwiYWRtaW5faWQiOiIxIiwiY29tcGFueV9pZCI6IjMiLCJleHAiOjE2MDMxNzQxMTB9.WbqjfeuVHpc5DZwIgmQRPZepld3rsmAeKiSk9RieOQo'

  var params = {
    headers: {
      'Content-Type': 'application/json',
      'Authorization': 'Bearer ' + token
    },
  };

  var data = {
    project_desc: "ccc" + JSON.stringify(count),
    project_startdate: "1545730073",
    project_name: "project_name",
    project_enddate: "1545730073",
    status_id: 1,
    project_creator_id: 1,
    project_number: "_" + JSON.stringify(count)
  }

  let res = http.post(url, JSON.stringify(data), params);

  console.log(res.body)
  count += 1;
  sleep(1);

}