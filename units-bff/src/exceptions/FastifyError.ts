class FastifyError {
  code: number;
  errors: string[];
  statusCode: number;
  message: string;
  details?: unknown;
  extraData?: unknown;
  constructor(code: number, errors: string[], statusCode: number, message: string, details?: unknown, extraData?: unknown) {
    this.code = code;
    this.errors = errors;
    this.statusCode = statusCode;
    this.message = message;
    if (extraData) {
      this.extraData = extraData;
    }
    if (details) {
      this.details = details;
    }
  }
}

export { FastifyError };
