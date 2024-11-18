import { AxiosError } from 'axios';
import { ErrorResponse } from '../types/global/response';


export const extractError = (error: AxiosError): ErrorResponse => {
  return {
    ...(error.response?.data as Record<string, unknown> || {}),
    statusCode: error.response?.status || 500,
  } as ErrorResponse;
};
