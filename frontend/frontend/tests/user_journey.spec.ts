import { test, expect } from '@playwright/test';

test.describe('Securebox End-to-End User Journey', () => {
  
  test('should connect GitHub, scan a repo, and view findings', async ({ page }) => {
    // 1. Navigate to Application
    await page.goto('/');
    
    // 2. Navigate to Integrations/GitHub
    // Assuming we have a settings link in the sidebar
    await page.click('text=Settings');
    await page.click('text=Connect GitHub');
    
    // 3. Simulate GitHub OAuth (using a mock for E2E tests)
    // In a real test, we'd use a test user or intercept the redirect
    await page.fill('input[name="github_token"]', 'test_token_123');
    await page.click('button:has-text("Authorize")');
    
    await expect(page.locator('text=GitHub Connected')).toBeVisible();
    
    // 4. Select Repository
    await page.click('text=List Repositories');
    await page.click('text=secure-test-repo');
    await page.click('button:has-text("Sync Repository")');
    
    await expect(page.locator('text=Repository Synced')).toBeVisible();
    
    // 5. Start Scan
    await page.click('text=Repositories');
    await page.click('text=secure-test-repo');
    await page.click('button:has-text("Run New Scan")');
    
    // Verify loading state
    await expect(page.locator('text=Scan in progress')).toBeVisible();
    
    // Wait for scan completion (mocked timing)
    await page.waitForSelector('text=Scan Completed', { timeout: 30000 });
    
    // 6. View Findings
    await page.click('text=Security Center');
    
    // Verify findings are displayed
    const findings = page.locator('.divide-y > div');
    await expect(findings).toBeVisible();
    await expect(findings.first()).toContainText('AWS Access Key');
    
    // Open finding details
    await findings.first().click();
    await expect(page.locator('text=Finding Details')).toBeVisible();
    await expect(page.locator('text=Severity la')).toBeVisible(); // Check for severity indicator
  });
});
