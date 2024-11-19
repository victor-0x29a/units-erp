import type { FastifyError, FastifyReply, FastifyRequest } from "fastify";
import { mountErrorResponse } from "../utils";
import { FastifyError as CustomFastifyError } from "../exceptions/FastifyError";

export const errorHandler = (
  error: FastifyError & { errors: string[] },
  _request: FastifyRequest,
  reply: FastifyReply
) => {
  const errorsList = error?.errors || [];

  const haveMultipleErrors = errorsList.length > 1;

  if (haveMultipleErrors) {
    const error = new CustomFastifyError(0, errorsList, 422, "Have multiple errors", errorsList);
    reply.status(422).send(mountErrorResponse(error));
    return;
  }

  const mountedError = mountErrorResponse(error as unknown as CustomFastifyError);

  reply.status(error.statusCode || 500).send(mountedError);

  return;
};
