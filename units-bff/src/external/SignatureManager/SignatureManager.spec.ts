import { JsonWebTokenError, TokenExpiredError } from "jsonwebtoken";
import { InvalidAuthorization, ExpiredAuthorization, InternalError } from "../../exceptions";
import { expiredToken, secret } from "./mocks/SignatureManager.mock";

jest.mock('../../constants', () => ({
  JWT_SECRET: secret
}));

import { SignatureManager } from "./SignatureManager";

let signatureManager: SignatureManager;

beforeEach(() => {
  jest.resetModules();
  jest.clearAllMocks();
  signatureManager = new SignatureManager();
});

describe ('should test all .decode success cases', () => {
  test('should decode an expired token', () => {
    const token = expiredToken;

    const result = signatureManager.decode(token);

    expect(result).not.toBeNull();
    expect(result.employeeDocument).not.toBeNull();
    expect(result.employeeRole).not.toBeNull();
    expect(result.isTemporary).not.toBeNull();
    expect(result.storeUnit).not.toBeNull();
    expect(result.iat).not.toBeNull();
    expect(result.exp).not.toBeNull();

    const isExpired: boolean = signatureManager.checkIsExpired(result.exp);

    expect(isExpired).toBeTruthy();
  });
  test('should decode a valid token', () => {
    const token = signatureManager.sign({
      employeeDocument: '55265344055',
      employeeRole: 'employee',
      isTemporary: false,
      storeUnit: 1
    });

    const result = signatureManager.decode(token);

    expect(result).not.toBeNull();
    expect(result.employeeDocument).not.toBeNull();
    expect(result.employeeRole).not.toBeNull();
    expect(result.isTemporary).not.toBeNull();
    expect(result.storeUnit).not.toBeNull();
    expect(result.iat).not.toBeNull();
    expect(result.exp).not.toBeNull();

    const isExpired: boolean = signatureManager.checkIsExpired(result.exp, true);

    expect(isExpired).toBeFalsy();
  });
});

describe ('should test all .sign success cases', () => {
  test('should sign a token', () => {
    const token = signatureManager.sign({
      employeeDocument: '55265344055',
      employeeRole: 'employee',
      isTemporary: false,
      storeUnit: 1
    });

    expect(token).not.toBeNull();
  });
});

describe ('should test all .checkIsValid cases', () => {
  test('should check a valid token', () => {
    const token = signatureManager.sign({
      employeeDocument: '55265344055',
      employeeRole: 'employee',
      isTemporary: false,
      storeUnit: 1
    });

    const result = signatureManager.checkIsValid(token);

    expect(result).toBeTruthy();

  });

  test('should check an invalid token', async () => {
    const token = signatureManager.sign({
      employeeDocument: '55265344055',
      employeeRole: 'employee',
      isTemporary: false,
      storeUnit: 1
    });

    jest.doMock('../../constants', () => ({
      JWT_SECRET: 'invalid-secret-2'
    }));

    const { SignatureManager } = await import('./SignatureManager');

    signatureManager = new SignatureManager();

    const result = signatureManager.checkIsValid(token);

    await expect(result).rejects.toEqual(
      new InvalidAuthorization(
        ["Invalid token"],
        new JsonWebTokenError("invalid signature")
      )
    );
  });
  test('should check when is an expired token', async () => {
    const token = expiredToken;

    const result = signatureManager.checkIsValid(token);

    await expect(result).rejects.toEqual(
      new ExpiredAuthorization(
        ["Token expired"],
        new TokenExpiredError("jwt expired", new Date())
      )
    );
  });
  test('should check when occur an internal error', async () => {
    jest.doMock('jsonwebtoken', () => ({
      verify: (_token: string, _secret: string, callback: (error: unknown, decoded: unknown) => void) => {
        callback(new Error('test'), null);
      },
      TokenExpiredError,
      JsonWebTokenError
    }));

    const { SignatureManager } = await import('./SignatureManager');

    signatureManager = new SignatureManager();

    const result = signatureManager.checkIsValid('invalid-token');

    await expect(result).rejects.toEqual(
      new InternalError(new Error('test'))
    );
  });
});
