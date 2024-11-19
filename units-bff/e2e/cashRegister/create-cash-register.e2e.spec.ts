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

const authorizationToken = new SignatureManager().sign({
  employeeDocument: "80067135021",
  employeeRole: "ADMIN",
  isTemporary: false,
  storeUnit: 1
});

test("should create a cash register", async () => {
  jest.doMock('../../src/entity', () => ({
    CashRegisterClock: {
      findOne: jest.fn().mockResolvedValue(null),
      create: jest.fn().mockResolvedValue({
        toJSON: jest.fn().mockReturnValue({ id: 1 })
      })
    }
  }));

  const { createServer } = await import("../../src/fastify");

  server = createServer();

  const response = await server.inject({
    method: "POST",
    url: "/v1/cash-register",
    headers: {
      authorization: authorizationToken
    }
  });

  expect(response.statusCode).toBe(201);
  expect(response.json()).toEqual({ cashRegisterId: 1 });
});

test('should fail when has already registered', async () => {
  jest.doMock('../../src/entity', () => ({
    CashRegisterClock: {
      findOne: jest.fn().mockResolvedValue({})
    }
  }));

  const { createServer } = await import("../../src/fastify");

  server = createServer();

  const response = await server.inject({
    method: "POST",
    url: "/v1/cash-register",
    headers: {
      authorization: authorizationToken
    }
  });

  expect(response.statusCode).toBe(422);
  expect(response.json()).toEqual({
    code: 1006,
    message: "Conflict error",
    errors: ["You can't clock in twice by day."]
  });
});

test('should show an internal error when the creation fails', async () => {
  jest.doMock('../../src/entity', () => ({
    CashRegisterClock: {
      findOne: jest.fn().mockResolvedValue(null),
      create: jest.fn().mockRejectedValue(new Error("Connection lost"))
    }
  }));

  const { createServer } = await import("../../src/fastify");

  server = createServer();

  const response = await server.inject({
    method: "POST",
    url: "/v1/cash-register",
    headers: {
      authorization: authorizationToken
    }
  });

  expect(response.statusCode).toBe(500);
  expect(response.json()).toEqual({
    code: 1005,
    message: "Internal error",
    errors: ["Internal error"]
  });
});

test('should show an internal error when the findOne fails', async () => {
  jest.doMock('../../src/entity', () => ({
    CashRegisterClock: {
      findOne: jest.fn().mockRejectedValue(new Error("Connection lost"))
    }
  }));

  const { createServer } = await import("../../src/fastify");

  server = createServer();

  const response = await server.inject({
    method: "POST",
    url: "/v1/cash-register",
    headers: {
      authorization: authorizationToken
    }
  });

  expect(response.statusCode).toBe(500);
  expect(response.json()).toEqual({
    code: 1005,
    message: "Internal error",
    errors: ["Internal error"]
  });
});

test('should fails when the employee is not an operator', async () => {
  const inventorAuthorizationToken = new SignatureManager().sign({
    employeeDocument: "80067135021",
    employeeRole: "INVENTOR",
    isTemporary: false,
    storeUnit: 1
  });

  const { createServer } = await import("../../src/fastify");

  server = createServer();

  const response = await server.inject({
    method: "POST",
    url: "/v1/cash-register",
    headers: {
      authorization: inventorAuthorizationToken
    }
  });

  expect(response.statusCode).toBe(403);
  expect(response.json()).toEqual({
    code: 1009,
    message: "Required permissions: OPERATOR",
    errors: ["Insufficient permissions"]
  });
});
