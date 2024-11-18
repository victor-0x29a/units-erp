class FastifyError {
  code: number;
  errors: string[];
  statusCode: number;
  message: string;
  details?: unknown;
  constructor(code: number, errors: string[], statusCode: number, message: string, details?: unknown) {
    this.code = code;
    this.errors = errors;
    this.statusCode = statusCode;
    this.message = message;
    if (details) {
      this.details = details;
    }
  }
}

export { FastifyError };
