import http from 'k6/http';
//var API_URL   = process.env.API_URL;

export default function () {
  const url = `http://${__ENV.API_HOST}/api/users`;
  const u1 = JSON.stringify({username: 'melissa.ross', email: 'melissa.ross@gmail.com'});
  const u2 = JSON.stringify({username: 'richard.bautista', email: 'richard.bautista@gmail.com'});
  const u3 = JSON.stringify({username: 'david.ray', email: 'david.ray@yahoo.com'});
  const u4 = JSON.stringify({username: 'gregory.watson', email: 'gregory.watson@gmail.co'});
  const u5 = JSON.stringify({username: 'lisa.baldwin', email: 'lisa.baldwin@yahoo.como'});

  const params = {
    headers: {
      'Content-Type': 'application/json',
    },
  };

  http.batch([
    ['POST', url, u1, params],
    ['POST', url, u2, params],
    ['POST', url, u3, params],
    ['POST', url, u4, params],
    ['POST', url, u5, params]
  ]);
}
