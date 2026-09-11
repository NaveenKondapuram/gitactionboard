import { test, expect } from '@playwright/test';

test('simple arithmetic test', () => {
  expect(1 + 1).toBe(2);
});

test('string comparison test', () => {
  const greeting = 'Hello, World!';
  expect(greeting).toContain('Hello');
});

test('array test', () => {
  const numbers = [1, 2, 3, 4, 5];
  expect(numbers).toHaveLength(5);
  expect(numbers).toContain(3);
});

test('object test', () => {
  const user = {
    name: 'John',
    age: 30,
    active: true
  };
  expect(user.name).toBe('John');
  expect(user.age).toBeGreaterThan(18);
});
