const BASE_URL='https://your-render-app.onrender.com/api'; 
const API= {
    
    login: (data)=>fetch(`${BASE_URL}/auth/login`,{
        method: 'POST', headers: {'Content-Type':'application/json'},
        body: JSON.stringify(data)
    }).then(r=>r.json()),
    
    register: (data)=>fetch(`${BASE_URL}/auth/register`,{
        method: 'POST', headers:{'Content-Type':'application/json'},
        body: JSON.stringify(data)
  }).then(r => r.json()),

  get: (path)=> fetch(`${BASE_URL}${path}`,{
    method: 'POST',
    headers: {
        'Content-Type':'application/json',
        'Authorization':`Bearer ${localStorage.getItem('token')}`
    },
    body: JSON.stringify(data)
  }).then(r=>r.json()),

  put: (path, data) => fetch(`${BASE_URL}${path}`, {
    method: 'PUT',
    headers: {
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${localStorage.getItem('token')}`
    },
    body: JSON.stringify(data)
  }).then(r => r.json()),

  delete: (path) => fetch(`${BASE_URL}${path}`, {
    method: 'DELETE',
    headers: { 'Authorization': `Bearer ${localStorage.getItem('token')}` }
  }).then(r => r.json()),
};
    
