export interface ErrorResponse {
    statusCode: number;
    code: number;
    message: string;
    errors: unknown;
}
