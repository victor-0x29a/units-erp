import { createInstance } from './core';
import { extractError } from './utils/extract-error';

export const createService = (basePath: string) => {
  const coreInstance = createInstance();

  const { baseURL } = coreInstance.defaults;

  coreInstance.defaults.baseURL = baseURL + basePath;

  coreInstance.interceptors.response.use(
    (response) => response,
    (error) => {
      return Promise.reject(extractError(error));
    },
  );

  return coreInstance;
};
