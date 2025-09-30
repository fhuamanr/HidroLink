import { test, expect } from '@playwright/test';

const USER = { username: 'tester', password: 'pass1234' };

async function getToken(request) {
  const r = await request.post('/api/token/', { data: USER });
  expect(r.ok()).toBeTruthy();
  const j = await r.json();
  return j.access as string;
}

test('API smoke: /readings y /readings/cost', async ({ request }) => {
  const token = await getToken(request);
  const headers = { Authorization: `Bearer ${token}` };

  // Lecturas
  const r1 = await request.get('/api/readings/', { headers });
  expect(r1.ok()).toBeTruthy();
  const lecturas = await r1.json();
  expect(Array.isArray(lecturas)).toBeTruthy();
  expect(lecturas.length).toBeGreaterThan(0);

  // Costo (al menos igual a la tarifa fija si hay 1+ lectura)
  const r2 = await request.get('/api/readings/cost/?household=Casa%20Miraflores&from=2025-01-01&to=2030-01-01', { headers });
  expect(r2.ok()).toBeTruthy();
  const cost = await r2.json();
  expect(cost.estimated_cost).toBeGreaterThanOrEqual(10.0);
});