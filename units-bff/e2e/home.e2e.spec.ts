import { FastifyInstance } from 'fastify';
import { createServer } from '../src/fastify';

let server: FastifyInstance;

beforeEach(() => {
  server = createServer();
});

afterEach(async () => {
  if (server) {
    await server.close();
  }
});

test("should say welcome", async () => {
  const response = await server.inject({
    method: "GET",
    url: "/",
  });

  expect(response.statusCode).toBe(200);
  expect(response.payload).toBe("Welcome to Units-BFF!");
});

test("should say hello to me", async () => {
  const response = await server.inject({
    method: "POST",
    url: "/",
    payload: {
      name: "me",
    },
  });

  expect(response.statusCode).toBe(200);
  expect(response.payload).toBe("Hello me!");
});

test("should not say hello to me", async () => {
  const response = await server.inject({
    method: "POST",
    url: "/",
    payload: {
      name: "",
    },
  });

  expect(response.statusCode).toBe(400);
  expect(response.json()).toEqual({
    code: "FST_ERR_VALIDATION",
    error: ["O nome é obrigatório", "Nome muito curto"],
  });
});
