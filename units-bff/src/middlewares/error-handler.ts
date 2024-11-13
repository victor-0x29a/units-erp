import type { FastifyError, FastifyReply, FastifyRequest } from "fastify";

export const errorHandler = (
  error: FastifyError & { errors: string[] },
  _request: FastifyRequest,
  reply: FastifyReply
) => {
  const errorsList = error?.errors || [];

  const haveMultipleErrors = errorsList.length > 1;

  const errorTemplate = {
    code: error.code,
  };

  if (haveMultipleErrors) {
    reply.status(400).send({
      ...errorTemplate,
      error: errorsList,
    });
    return;
  }

  reply.status(error.statusCode || 500).send({
    ...errorTemplate,
    error: errorsList[0] || error.message,
  });

  return;
};
