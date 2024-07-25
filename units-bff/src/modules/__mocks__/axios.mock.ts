import axios from "axios";

const defaultAxiosResponse = {
  statusCode: 200,
  data: null,
  headers: {},
};

jest.mock("axios", () => ({
  create: jest.fn().mockReturnValue({
    get: jest.fn(() => Promise.resolve(defaultAxiosResponse)),
    post: jest.fn(() => Promise.resolve(defaultAxiosResponse)),
    put: jest.fn(() => Promise.resolve(defaultAxiosResponse)),
    patch: jest.fn(() => Promise.resolve(defaultAxiosResponse)),
    delete: jest.fn(() => Promise.resolve(defaultAxiosResponse)),
    interceptors: {
      request: {
        use: jest.fn(),
      },
      response: {
        use: jest.fn(),
      },
    },
  }),
}));

export const mockedAxios = axios as jest.Mocked<typeof axios>;
