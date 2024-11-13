import { FastifyInstance } from 'fastify';
import { createServer } from '../../src/fastify';

jest.mock('../../src/core', () => ({
  privateDomains: {
    employeeDomain: {
      login: jest.fn().mockResolvedValue('Bearer token')
    }
  }
}));

let server: FastifyInstance;

beforeEach(() => {
  server = createServer();
});

afterEach(async () => {
  if (server) {
    await server.close();
  }
  jest.resetModules();
});

test("should authenticate an employe", async () => {
  const response = await server.inject({
    method: "POST",
    url: "/employee/login",
    payload: {
      "username": "victor-0x29a"
    }
  });

  expect(response.statusCode).toBe(204);
  expect(response.headers['authorization']).toBe('Bearer token');
});

test("should not authenticate an unexists employee", async () => {
  jest.doMock('../../src/core', () => ({
    privateDomains: {
      employeeDomain: {
        login: jest.fn().mockRejectedValue({
          "code": 1003,
          "message": "Employee not found.",
          "errors": [],
          "statusCode": 404
        })
      }
    }
  }));

  const { createServer } = await import("../../src/fastify");

  server = createServer();

  const response = await server.inject({
    method: "POST",
    url: "/employee/login",
    payload: {
      "username": "victor-0x29a"
    }
  });

  expect(response.statusCode).toBe(401);
});

test("should not authenticate when the password is wrong", async () => {
  jest.doMock('../../src/core', () => ({
    privateDomains: {
      employeeDomain: {
        login: jest.fn().mockRejectedValue({
          "code": 1070,
          "message": "Failed on process.",
          "errors": [],
          "statusCode": 422
        })
      }
    }
  }));

  const { createServer } = await import("../../src/fastify");

  server = createServer();

  const response = await server.inject({
    method: "POST",
    url: "/employee/login",
    payload: {
      "username": "victor-0x29a"
    }
  });

  expect(response.statusCode).toBe(401);
});

test("should reject when havent field on login payload", async () => {
  const response = await server.inject({
    method: "POST",
    url: "/employee/login",
    payload: {}
  });

  const errorResponse = response.json();

  expect(response.statusCode).toBe(400);
  expect(errorResponse.code).toBe("FST_ERR_VALIDATION");
  expect(errorResponse.message).toBe("You must provide at least one of the fields: document, username");
  expect(errorResponse.errors.length).toEqual(1);
});

test("should reject when have an unexpected external error", async () => {
  jest.doMock('../../src/core', () => ({
    privateDomains: {
      employeeDomain: {
        login: jest.fn().mockRejectedValue({
          "code": 1555,
          "message": "Failed on process.",
          "errors": [],
          "statusCode": 500
        })
      }
    }
  }));

  const { createServer } = await import("../../src/fastify");

  server = createServer();

  const response = await server.inject({
    method: "POST",
    url: "/employee/login",
    payload: {
      "username": "victor-0x29a"
    }
  });

  const errorResponse = response.json();

  expect(response.statusCode).toBe(503);
  expect(errorResponse.code).toBe(1002);
  expect(errorResponse.message).toBe("External error");
  expect(errorResponse.errors.length).toEqual(1);
});
