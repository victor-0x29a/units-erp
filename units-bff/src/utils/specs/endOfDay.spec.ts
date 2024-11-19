import { endOfDay } from "../endOfDay";

test('should return the end of the day in UTC', () => {
  const date = new Date('2021-09-01T12:00:00Z');

  const result = endOfDay(date);

  expect(result).toEqual(new Date('2021-09-01T23:59:59.999Z'));
});
