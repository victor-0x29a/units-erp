export const mountErrorResponse = (code: number | string | number[] | string[], message: string, errors: unknown[]) => ({
  code,
  message,
  errors
});
