import { test, expect } from '@playwright/test';

test.describe('Securebox Repair Workflow', () => {
  
  test('should propose, approve, and verify a repair', async ({ page }) => {
    await page.goto('/security');
    
    // 1. Select a finding to repair
    await page.click('text=AWS Access Key Leaked');
    
    // 2. Trigger AI Fix
    await page.click('button:has-text("Generate AI Fix")');
    
    // 3. Verify Diff Preview
    await expect(page.locator('text=Proposed Patch')).toBeVisible();
    await expect(page.locator('.diff-added')).toBeVisible();
    await expect(page.locator('.diff-removed')).toBeVisible();
    
    // 4. Approve and Apply
    await page.click('button:has-text("Approve and Apply")');
    
    // 5. Verify Application state
    await expect(page.locator('text=Applying Patch...')).toBeVisible();
    await expect(page.locator('text=Patch Applied Successfully')).toBeVisible();
    
    // 6. Check Rescan results
    await expect(page.locator('text=Verification Passed')).toBeVisible();
    await expect(page.locator('text=Finding Resolved')).toBeVisible();
  });
});
