import Axios, { AxiosError, AxiosInstance, AxiosResponse } from "axios";
import axiosRetry from "axios-retry";
import type { ICoreModuleResponse } from "./core.module.d";
import {
  UNITS_VAULT_URL,
  UNITS_VAULT_USER_AGENT,
  UNITS_VAULT_MAX_RETRIES,
} from "@constants";

class CoreModule {
  private axios: typeof Axios;
  private requestHeaders: Record<string, string> = {};
  private requestURI: string = UNITS_VAULT_URL;

  private axiosInstance: AxiosInstance;

  private readonly generateConfig = () => {
    const { Authorization } = this.requestHeaders;
    const contentType = this.payload ? "application/json" : undefined;

    return {
      headers: {
        Authorization: Authorization || "",
        "User-Agent": UNITS_VAULT_USER_AGENT,
        "Content-Type": contentType,
      },
    };
  };

  /* c8 ignore start */
  private extractData = (response: AxiosResponse) => {
    return Promise.resolve({
      statusCode: response.status,
      data: response.data,
      headers: response.headers,
    }) as unknown as Promise<AxiosResponse>;
  };

  /* c8 ignore start */
  private extractError = (error: AxiosError) => {
    return Promise.reject(error);
  };

  constructor(
    axios: typeof Axios,
    path: string,
    private readonly payload?: Record<
      string | number,
      string | object | number | null
    >,
    paramsData: Record<string, string> | undefined = undefined,
    queryData: Record<string, string> | undefined = undefined,
    requestHeaders: Record<string, string> = {}
  ) {
    this.axios = axios;
    this.createInstance();
    this.requestURI += `/${path}`;
    if (paramsData) {
      this.requestURI += this.parseParamsData(paramsData);
    }
    if (queryData) {
      this.requestURI += this.parseQueryData(queryData);
    }
    this.requestHeaders = requestHeaders;

    this.axiosInstance.interceptors.response.use(
      this.extractData,
      this.extractError
    );
  }

  private createInstance = () => {
    this.axiosInstance = this.axios.create({
      baseURL: UNITS_VAULT_URL,
    });
    axiosRetry(this.axiosInstance, {
      retries: UNITS_VAULT_MAX_RETRIES,
      retryDelay: axiosRetry.exponentialDelay,
    });
  };

  private parseParamsData = (paramsData: Record<string, string>) => {
    const keys = Object.keys(paramsData);

    let parsedParamsData = "";

    for (const key of keys) {
      parsedParamsData += `/${key}/${paramsData[key]}`;
    }

    return parsedParamsData;
  };

  private parseQueryData = (queryData: Record<string, string>) => {
    const keys = Object.keys(queryData);
    const keysLength = keys.length;
    return keys.reduce((acc, curr, currIdx) => {
      acc += `${curr}=${queryData[curr]}`;
      if (currIdx < keysLength - 1) {
        acc += "&";
      }
      return acc;
    }, "?");
  };

  public get = async (): Promise<ICoreModuleResponse> => {
    return await this.axiosInstance.get(this.requestURI, this.generateConfig());
  };

  public post = async (): Promise<ICoreModuleResponse> => {
    return await this.axiosInstance.post(
      this.requestURI,
      this.payload,
      this.generateConfig()
    );
  };

  public put = async (): Promise<ICoreModuleResponse> => {
    return await this.axiosInstance.put(
      this.requestURI,
      this.payload,
      this.generateConfig()
    );
  };

  public patch = async (): Promise<ICoreModuleResponse> => {
    return await this.axiosInstance.patch(
      this.requestURI,
      this.payload,
      this.generateConfig()
    );
  };

  public delete = async (): Promise<ICoreModuleResponse> => {
    return await this.axiosInstance.delete(
      this.requestURI,
      this.generateConfig()
    );
  };
}

export { CoreModule };
