import type { FastifyError, FastifyReply, FastifyRequest } from "fastify";
import { MountErrorResponse } from "../utils";

export const errorHandler = (
  error: FastifyError & { errors: string[] },
  _request: FastifyRequest,
  reply: FastifyReply
) => {
  const errorsList = error?.errors || [];

  const haveMultipleErrors = errorsList.length > 1;

  if (haveMultipleErrors) {
    reply.status(422).send(MountErrorResponse("MULTIPLE_ERRORS", "MULTIPLE_ERRORS", errorsList));
    return;
  }

  reply.status(error.statusCode || 500).send(MountErrorResponse(error.code, error.message, error.errors));

  return;
};
