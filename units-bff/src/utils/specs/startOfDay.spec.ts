import { startOfDay } from "../startOfDay";

test('should return the start of the day in UTC', () => {
  const date = new Date('2021-09-01T12:00:00Z');

  const result = startOfDay(date);

  expect(result).toEqual(new Date('2021-09-01T00:00:00.000Z'));
});
