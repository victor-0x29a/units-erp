import { FastifyInstance } from 'fastify';
import { SignatureManager } from '../../src/external';
import { Roles } from '../../src/types/employee';
import { mockedRepository } from "./mocks/hit-clocks.mock";

let server: FastifyInstance;

afterEach(async () => {
  if (server) {
    await server.close();
  }
  jest.resetModules();
  jest.clearAllMocks();
});

const genToken = (role: Roles) => new SignatureManager().sign({
  employeeDocument: "80067135021",
  employeeRole: role,
  isTemporary: false,
  storeUnit: 1
});

const ADMIN_TOKEN = genToken("ADMIN");

const INVENTOR_TOKEN = genToken("INVENTOR");

test("should clock in", async () => {
  jest.doMock('../../src/entity', () => ({
    CashRegisterClock: mockedRepository.toggleCases.success.clockIn
  }));

  const { createServer } = await import("../../src/fastify");

  server = createServer();

  const response = await server.inject({
    method: "POST",
    url: "/v1/cash-register/hit-clock/1",
    headers: {
      authorization: ADMIN_TOKEN
    }
  });

  expect(response.statusCode).toBe(204);
});

test("should clock lunch in", async () => {
  jest.doMock('../../src/entity', () => ({
    CashRegisterClock: mockedRepository.toggleCases.success.clockLunchIn
  }));

  const { createServer } = await import("../../src/fastify");

  server = createServer();

  const response = await server.inject({
    method: "POST",
    url: "/v1/cash-register/hit-clock/1",
    headers: {
      authorization: ADMIN_TOKEN
    }
  });

  expect(response.statusCode).toBe(204);
});

test("should clock lunch out", async () => {
  jest.doMock('../../src/entity', () => ({
    CashRegisterClock: mockedRepository.toggleCases.success.clockLunchOut
  }));

  const { createServer } = await import("../../src/fastify");

  server = createServer();

  const response = await server.inject({
    method: "POST",
    url: "/v1/cash-register/hit-clock/1",
    headers: {
      authorization: ADMIN_TOKEN
    }
  });

  expect(response.statusCode).toBe(204);
});

test("should clock out", async () => {
  jest.doMock('../../src/entity', () => ({
    CashRegisterClock: mockedRepository.toggleCases.success.lastClockOut
  }));

  const { createServer } = await import("../../src/fastify");

  server = createServer();

  const response = await server.inject({
    method: "POST",
    url: "/v1/cash-register/hit-clock/1",
    headers: {
      authorization: ADMIN_TOKEN
    }
  });

  expect(response.statusCode).toBe(204);
});

test("should fails when has already clocked out", async () => {
  jest.doMock('../../src/entity', () => ({
    CashRegisterClock: mockedRepository.toggleCases.fail.clockedOut
  }));

  const { createServer } = await import("../../src/fastify");

  server = createServer();

  const response = await server.inject({
    method: "POST",
    url: "/v1/cash-register/hit-clock/1",
    headers: {
      authorization: ADMIN_TOKEN
    }
  });

  expect(response.statusCode).toBe(423);
  expect(response.json()).toEqual({
    "code": 1004,
    "message": "Retroactive action",
    "errors": ["You can't clock out twice by day."]
  });
});

test("should fails when not found", async () => {
  jest.doMock('../../src/entity', () => ({
    CashRegisterClock: mockedRepository.toggleCases.fail.notFound
  }));

  const { createServer } = await import("../../src/fastify");

  server = createServer();

  const response = await server.inject({
    method: "POST",
    url: "/v1/cash-register/hit-clock/1",
    headers: {
      authorization: ADMIN_TOKEN
    }
  });

  expect(response.statusCode).toBe(404);
  expect(response.json()).toEqual({
    "code": 1003,
    "message": "Missing doc",
    "errors": ["Register not found."]
  });
});

test("should fails when clock lunch in update fails", async () => {
  jest.doMock('../../src/entity', () => ({
    CashRegisterClock: mockedRepository.toggleCases.fail.clockLunchInUpdateFail
  }));

  const { createServer } = await import("../../src/fastify");

  server = createServer();

  const response = await server.inject({
    method: "POST",
    url: "/v1/cash-register/hit-clock/1",
    headers: {
      authorization: ADMIN_TOKEN
    }
  });

  expect(response.statusCode).toBe(500);
  expect(response.json()).toEqual({
    "code": 1005,
    "message": "Internal error",
    "errors": ["Internal error"]
  });
});

test("should fails when orm fails", async () => {
  jest.doMock('../../src/entity', () => ({
    CashRegisterClock: mockedRepository.toggleCases.fail.ormInternalError
  }));

  const { createServer } = await import("../../src/fastify");

  server = createServer();

  const response = await server.inject({
    method: "POST",
    url: "/v1/cash-register/hit-clock/1",
    headers: {
      authorization: ADMIN_TOKEN
    }
  });

  expect(response.statusCode).toBe(500);
  expect(response.json()).toEqual({
    "code": 1005,
    "message": "Internal error",
    "errors": ["Internal error"]
  });
});

test("should fails when not is operator", async () => {
  const { createServer } = await import("../../src/fastify");

  server = createServer();

  const response = await server.inject({
    method: "POST",
    url: "/v1/cash-register/hit-clock/1",
    headers: {
      authorization: INVENTOR_TOKEN
    }
  });

  expect(response.statusCode).toBe(403);
  expect(response.json()).toEqual({
    code: 1009,
    message: "Required permissions: OPERATOR",
    errors: ["Insufficient permissions"],
    extraData: ["OPERATOR"]
  });
});
