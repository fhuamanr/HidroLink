import { test, expect } from '@playwright/test';

const USER = { username: 'tester', password: 'pass1234' };

test('Login via UI y dashboard muestra datos', async ({ page }) => {
  // 1) Login por formulario
  await page.goto('/login/');
  await page.getByLabel('Usuario o email').fill(USER.username);
  await page.getByLabel('Contraseña').fill(USER.password);

  // Click, then wait for token persisted by your login JS
  await page.getByRole('button', { name: /Entrar/i }).click();
  await page.waitForFunction(() => !!localStorage.getItem('access'), null, { timeout: 10_000 });

  // Now assert you left the login page and the dashboard loads
  await expect(page).toHaveURL((url) => url.pathname === '/');
  await page.waitForSelector('#lecturas li', { timeout: 10_000 });


  // 2) Token en localStorage
  const access = await page.evaluate(() => localStorage.getItem('access'));
  expect(access).toBeTruthy();

  // 3) El dashboard debe cargar alertas y lecturas
  await page.waitForSelector('#lecturas li', { timeout: 10_000 });
  const items = await page.locator('#lecturas li').all();
  expect(items.length).toBeGreaterThan(0);

  // 4) Evidencia: captura de pantalla del dashboard
  await page.screenshot({ path: 'evidencias/dashboard.png', fullPage: true });
});