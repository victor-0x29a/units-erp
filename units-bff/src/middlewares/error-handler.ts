import type { FastifyError, FastifyReply, FastifyRequest } from "fastify";
import { mountErrorResponse } from "../utils";

export const errorHandler = (
  error: FastifyError & { errors: string[] },
  _request: FastifyRequest,
  reply: FastifyReply
) => {
  const errorsList = error?.errors || [];

  const haveMultipleErrors = errorsList.length > 1;

  if (haveMultipleErrors) {
    reply.status(422).send(mountErrorResponse("MULTIPLE_ERRORS", "MULTIPLE_ERRORS", errorsList));
    return;
  }

  reply.status(error.statusCode || 500).send(mountErrorResponse(error.code, error.message, error.errors));

  return;
};
