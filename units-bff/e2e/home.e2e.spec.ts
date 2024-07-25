import { Server } from "../src/server";

test("should say welcome", async () => {
  const server = new Server(false).start();

  const response = await server.inject({
    method: "GET",
    url: "/",
  });

  expect(response.statusCode).toBe(200);
  expect(response.payload).toBe("Welcome to Units-BFF!");

  await server.close();
});
