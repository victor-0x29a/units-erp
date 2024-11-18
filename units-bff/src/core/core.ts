import axios, { AxiosInstance } from "axios";
import axiosRetry from "axios-retry";
import {
  UNITS_VAULT_URL,
  UNITS_VAULT_USER_AGENT,
  UNITS_VAULT_MAX_RETRIES,
} from "../constants";

export const createInstance = (): AxiosInstance => {
  const axiosInstance = axios.create({
    baseURL: UNITS_VAULT_URL
  });
  axiosRetry(axiosInstance, {
    retries: UNITS_VAULT_MAX_RETRIES,
    retryDelay: axiosRetry.exponentialDelay
  });
  axiosInstance.interceptors.request.use((config) => {
    config.headers["User-Agent"] = UNITS_VAULT_USER_AGENT;
    return config;
  });

  return axiosInstance;
};
