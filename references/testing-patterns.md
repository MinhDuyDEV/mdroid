# Testing Patterns

> Reference for writing effective tests. Pulled in by /build, /verify, and /review.

## Test structure

### Arrange-Act-Assert (AAA)
```
// Arrange
const input = "test";
const expected = "TEST";

// Act
const result = transform(input);

// Assert
expect(result).toBe(expected);
```

### Naming
- Test names describe behavior, not implementation.
- Bad: `testUser()`, `test1()`
- Good: `should reject login when password is empty`, `returns 404 when user not found`
- Pattern: `should [expected behavior] when [condition]`

### One assertion per test (guideline)
- Each test should verify one behavior.
- Multiple assertions on the same behavior are fine.
- Multiple assertions on different behaviors = split the test.

## Test types

### Unit tests
- Test a single function/class in isolation.
- Mock external dependencies.
- Fast (<100ms each).
- Run on every commit.

### Integration tests
- Test multiple components together.
- Use real (or realistic) dependencies where feasible.
- Slower (100ms-1s each).
- Run on PR.

### E2E tests
- Test the full user flow end-to-end.
- Use real browser/API/database.
- Slowest (1-10s each).
- Run on merge to main / staging.

## Mocking

### When to mock
- External services (don't depend on network in unit tests).
- Database (use in-memory or mock for unit tests).
- Time (inject a clock, don't depend on real time).
- Random (inject a seed, don't depend on Math.random).

### When NOT to mock
- The thing you're testing (mocking the SUT makes the test useless).
- Simple value objects (just use real values).
- Standard library functions (they're already tested).

### Mock anti-patterns
- Over-mocking: if you mock everything, you're testing the mocks, not the code.
- Mocking too deep: mock at the boundary, not deep in the call chain.
- Behaviorless mocks: a mock that returns undefined doesn't test error handling.

## Examples

### React component test
```tsx
test("should show error message when submission fails", async () => {
  render(<LoginForm onSubmit={jest.fn().mockRejectedValue(new Error("fail"))} />);
  await userEvent.click(screen.getByRole("button", { name: /submit/i }));
  expect(screen.getByRole("alert")).toHaveTextContent("fail");
});
```

### API endpoint test
```ts
test("returns 400 when email is invalid", async () => {
  const res = await request(app)
    .post("/api/users")
    .send({ email: "not-an-email" });
  expect(res.status).toBe(400);
  expect(res.body.error).toContain("email");
});
```

### E2E test (Playwright)
```ts
test("user can log in and see dashboard", async ({ page }) => {
  await page.goto("/login");
  await page.fill("[name=email]", "test@example.com");
  await page.fill("[name=password]", "password");
  await page.click("button[type=submit]");
  await expect(page).toHaveURL("/dashboard");
});
```

## Anti-patterns

- **Testing implementation, not behavior**: `expect(internalState.flag).toBe(true)`. Test the observable output.
- **"Doesn't throw" tests**: `expect(() => fn()).not.toThrow()`. This proves nothing about correctness.
- **Snapshot tests as primary tests**: Snapshots catch changes, not bugs. Use sparingly.
- **Testing the mock**: If the test only verifies mock calls, it's testing the mock, not the code.
- **Giant tests**: A 200-line test is hard to understand. Split it.
- **No edge cases**: Only testing the happy path. Always test: null, empty, boundary, error.
- **Time-dependent tests**: `expect(new Date()).toBe(...)` will fail. Inject the clock.
- **Flaky tests**: Tests that pass sometimes and fail others. Fix immediately or remove.
