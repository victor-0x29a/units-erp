export const MountErrorResponse = (code: number, message: string, errors: unknown[]) => ({
  code,
  message,
  errors
});
