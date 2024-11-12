import { createServer } from '../src';

test("should say welcome", async () => {
  const server = createServer();

  const response = await server.inject({
    method: "GET",
    url: "/",
  });

  expect(response.statusCode).toBe(200);
  expect(response.payload).toBe("Welcome to Units-BFF!");

  await server.close();
});

test("should say hello to me", async () => {
  const server = createServer();

  const response = await server.inject({
    method: "POST",
    url: "/",
    payload: {
      name: "me",
    },
  });

  expect(response.statusCode).toBe(200);
  expect(response.payload).toBe("Hello me!");

  await server.close();
});

test("should not say hello to me", async () => {
  const server = createServer();

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

  await server.close();
});
