import { FastifyInstance } from 'fastify';

let server: FastifyInstance;

afterEach(async () => {
  if (server) {
    await server.close();
  }
  jest.resetModules();
  jest.resetAllMocks();
});

test("should authenticate an employe", async () => {
  jest.doMock('../../src/core', () => ({
    privateDomains: {
      employeeDomain: {
        login: jest.fn().mockResolvedValue('Bearer token')
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
  const { createServer } = await import("../../src/fastify");

  server = createServer();

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

test('should reject when document is invalid', async () => {
  const { createServer } = await import("../../src/fastify");

  server = createServer();

  const response = await server.inject({
    method: "POST",
    url: "/employee/login",
    payload: {
      "document": "123456789",
    }
  });

  const errorResponse = response.json();

  expect(response.statusCode).toBe(400);
  expect(errorResponse.code).toBe("FST_ERR_VALIDATION");
  expect(errorResponse.message).toBe("Document must be a valid CPF");
  expect(errorResponse.errors.length).toEqual(1);
});

test('should reject when have password and the length is less than 6 chars', async () => {
  const { createServer } = await import("../../src/fastify");

  server = createServer();

  const response = await server.inject({
    method: "POST",
    url: "/employee/login",
    payload: {
      "username": "victor w.",
      "password": "12345"
    }
  });

  const errorResponse = response.json();

  expect(response.statusCode).toBe(400);
  expect(errorResponse.code).toBe("FST_ERR_VALIDATION");
  expect(errorResponse.message).toBe("Password must have at least 6 characters");
  expect(errorResponse.errors.length).toEqual(1);
});
