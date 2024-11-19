import { FastifyReply, FastifyRequest } from "fastify";
import { SignatureManager } from "../../external";
import { protectByEmployeeRole } from "../protectByEmployeeRole";
import { requestsMock } from "./mocks/requestsMock";
import { InsufficientPermissions, InternalError, InvalidAuthorization } from "../../exceptions";
import { Roles } from "../../types/employee";

const signatureManager = new SignatureManager();

let reply: FastifyReply;

beforeEach(() => {
  jest.resetModules();
  reply = jest.fn() as unknown as FastifyReply;
});

afterEach(() => {
  jest.clearAllMocks();
});

const genToken = (role: Roles) => signatureManager.sign({
  employeeDocument: '55265344055',
  employeeRole: role,
  isTemporary: false,
  storeUnit: 1
});


test('should fail when havent authorization token', async () => {
  const middleware = protectByEmployeeRole(["ADMIN"], signatureManager);

  const request = requestsMock.withoutAuthorizationToken as unknown as FastifyRequest;

  await expect(middleware(request, reply))
    .rejects
    .toBeInstanceOf(InvalidAuthorization);
});

test('should pass when is valid and is an admin', async () => {
  const middleware = protectByEmployeeRole(["ADMIN"], signatureManager);

  const request = { ...requestsMock.withAuthorizationTemplate } as unknown as FastifyRequest;

  request.headers.authorization = genToken("ADMIN");

  await middleware(request, reply);

  expect(reply).not.toHaveBeenCalled();
});

test('should fail when have insufficient permissions', async () => {
  const middleware = protectByEmployeeRole(["INVENTOR"], signatureManager);

  const request = { ...requestsMock.withAuthorizationTemplate } as unknown as FastifyRequest;

  request.headers.authorization = genToken("OPERATOR");;

  await expect(middleware(request, reply)).rejects.toBeInstanceOf(InsufficientPermissions);

  await expect(middleware(request, reply)).rejects.toHaveProperty('message', "Required permissions: INVENTOR");
});

test('should pass when have sufficient permissions', async () => {
  const middleware = protectByEmployeeRole(["OPERATOR"], signatureManager);

  const request = { ...requestsMock.withAuthorizationTemplate } as unknown as FastifyRequest;

  request.headers.authorization = genToken("OPERATOR");

  await middleware(request, reply);

  expect(reply).not.toHaveBeenCalled();
});

test('should throw the SignatureManager exception', async () => {
  const mockedSignatureManager = {
    checkIsValid: jest.fn().mockRejectedValue(new InternalError()),
  } as unknown as SignatureManager;

  const { protectByEmployeeRole: mockedProtectByEmployeeRole } =  await import("../protectByEmployeeRole");

  const middleware = mockedProtectByEmployeeRole(["OPERATOR"], mockedSignatureManager);

  const request = { ...requestsMock.withAuthorizationTemplate } as unknown as FastifyRequest;

  request.headers.authorization = genToken("OPERATOR");

  await expect(
    middleware(request, reply)
  ).rejects.toBeInstanceOf(InternalError);
});
