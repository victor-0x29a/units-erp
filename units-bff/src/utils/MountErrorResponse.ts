export const MountErrorResponse = (code: number | string | number[] | string[], message: string, errors: unknown[]) => ({
  code,
  message,
  errors
});
