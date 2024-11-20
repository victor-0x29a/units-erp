import { FastifyInstance } from 'fastify';
import { SignatureManager } from '../../src/external';

let server: FastifyInstance;

afterEach(async () => {
  if (server) {
    await server.close();
  }
  jest.resetModules();
  jest.resetAllMocks();
});

test("should fill the password", async () => {
  jest.doMock('../../src/core', () => ({
    privateDomains: {
      employeeDomain: {
        fillPassword: jest.fn().mockResolvedValue(undefined)
      }
    }
  }));

  const signatureManager = new SignatureManager();

  const temporaryToken = signatureManager.sign({
    employeeDocument: "123456",
    isTemporary: true,
    employeeRole: "OPERATOR",
    storeUnit: 1
  });

  const { createServer } = await import("../../src/fastify");

  server = createServer();

  const response = await server.inject({
    method: "PUT",
    url: "/v1/employee/fill-password",
    payload: {
      "password": "******"
    },
    headers: {
      authorization: temporaryToken
    }
  });

  expect(response.statusCode).toBe(204);
});

test("should reject when the token is not temporary", async () => {
  const signatureManager = new SignatureManager();

  const token = signatureManager.sign({
    employeeDocument: "123456",
    isTemporary: false,
    employeeRole: "OPERATOR",
    storeUnit: 1
  });

  const { createServer } = await import("../../src/fastify");

  server = createServer();

  const response = await server.inject({
    method: "PUT",
    url: "/v1/employee/fill-password",
    payload: {
      "password": "******"
    },
    headers: {
      authorization: token
    }
  });

  expect(response.statusCode).toBe(422);
  expect(response.json()).toEqual({
    code: 1010,
    message: "Unprocessable",
    errors: [
      "You can't change your password."
    ]
  });
});

test("should reject when the external service broke", async () => {
  jest.doMock('../../src/core', () => ({
    privateDomains: {
      employeeDomain: {
        fillPassword: jest.fn().mockRejectedValue({
          "code": 500,
          "message": "Internal error.",
          "errors": [],
          "statusCode": 500
        })
      }
    }
  }));

  const signatureManager = new SignatureManager();

  const temporaryToken = signatureManager.sign({
    employeeDocument: "123456",
    isTemporary: true,
    employeeRole: "OPERATOR",
    storeUnit: 1
  });

  const { createServer } = await import("../../src/fastify");

  server = createServer();

  const response = await server.inject({
    method: "PUT",
    url: "/v1/employee/fill-password",
    payload: {
      "password": "******"
    },
    headers: {
      authorization: temporaryToken
    }
  });

  expect(response.statusCode).toBe(503);
  expect(response.json()).toEqual({
    code: 1002,
    message: "External error",
    errors: [
      "External error"
    ]
  });
});

test("should reject a password less than 6 chars", async () => {
  const signatureManager = new SignatureManager();

  const temporaryToken = signatureManager.sign({
    employeeDocument: "123456",
    isTemporary: true,
    employeeRole: "OPERATOR",
    storeUnit: 1
  });

  const { createServer } = await import("../../src/fastify");

  server = createServer();

  const response = await server.inject({
    method: "PUT",
    url: "/v1/employee/fill-password",
    payload: {
      "password": "*****"
    },
    headers: {
      authorization: temporaryToken
    }
  });

  expect(response.statusCode).toBe(400);
  expect(response.json()).toEqual({
    code: "FST_ERR_VALIDATION",
    message: "Password must have at least 6 characters",
    errors: [
      "Password must have at least 6 characters"
    ]
  });
});

test("should reject a password greater than 32 chars", async () => {
  const signatureManager = new SignatureManager();

  const temporaryToken = signatureManager.sign({
    employeeDocument: "123456",
    isTemporary: true,
    employeeRole: "OPERATOR",
    storeUnit: 1
  });

  const { createServer } = await import("../../src/fastify");

  server = createServer();

  const response = await server.inject({
    method: "PUT",
    url: "/v1/employee/fill-password",
    payload: {
      "password": "*********************************"
    },
    headers: {
      authorization: temporaryToken
    }
  });

  expect(response.statusCode).toBe(400);
  expect(response.json()).toEqual({
    code: "FST_ERR_VALIDATION",
    message: "Password must have at most 32 characters",
    errors: [
      "Password must have at most 32 characters"
    ]
  });
});

test('should reject when havent password & payload', async () => {
  const signatureManager = new SignatureManager();

  const temporaryToken = signatureManager.sign({
    employeeDocument: "123456",
    isTemporary: true,
    employeeRole: "OPERATOR",
    storeUnit: 1
  });

  const { createServer } = await import("../../src/fastify");

  server = createServer();

  const response = await server.inject({
    method: "PUT",
    url: "/v1/employee/fill-password",
    headers: {
      authorization: temporaryToken
    }
  });

  expect(response.statusCode).toBe(400);

  expect(response.json()).toEqual({
    code: "FST_ERR_VALIDATION",
    message: "Payload is required",
    errors: [
      "Payload is required"
    ]
  });

  const responseWithoutPasword = await server.inject({
    method: "PUT",
    url: "/v1/employee/fill-password",
    headers: {
      authorization: temporaryToken
    },
    payload: {}
  });

  expect(responseWithoutPasword.statusCode).toBe(400);

  expect(responseWithoutPasword.json()).toEqual({
    code: "FST_ERR_VALIDATION",
    message: "Password is required",
    errors: [
      "Password is required"
    ]
  });
});
