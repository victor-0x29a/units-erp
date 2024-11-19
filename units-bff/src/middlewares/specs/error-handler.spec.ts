import { FastifyError, FastifyReply, FastifyRequest } from "fastify";
import { errorHandler } from "../error-handler";
import { mountErrorResponse } from "../../utils";

test('should test when have multiple errors', () => {
  const reply = {
    status: jest.fn().mockReturnValue({
      send: jest.fn(),
    }),
  } as unknown as FastifyReply;

  const error = {
    errors: ['a', 'b']
  } as unknown as FastifyError & {
    errors: string[];
  };

  const request = {} as unknown as FastifyRequest;

  errorHandler(error, request, reply);

  expect(reply.status).toHaveBeenCalledWith(422);
  expect(reply.status(200).send).toHaveBeenCalledWith(mountErrorResponse("MULTIPLE_ERRORS", "MULTIPLE_ERRORS", ["a", "b"]));
});
