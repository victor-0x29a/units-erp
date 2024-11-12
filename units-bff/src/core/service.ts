import { createInstance } from './core';

export const createService = (basePath: string) => {
  const coreInstance = createInstance();

  const { baseURL } = coreInstance.defaults;

  coreInstance.defaults.baseURL = baseURL + basePath;

  return coreInstance;
};
