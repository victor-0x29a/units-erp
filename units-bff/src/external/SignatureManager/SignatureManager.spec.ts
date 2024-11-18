import { expiredToken, secret } from "./mocks/SignatureManager.mock";

jest.mock('../../constants', () => ({
  JWT_SECRET: secret
}));

import { SignatureManager } from "./SignatureManager";
describe ('should test all .decode success cases', () => {
  test('should decode an expired token', () => {
    const signatureManager = new SignatureManager();

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
    const signatureManager = new SignatureManager();

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
    const signatureManager = new SignatureManager();

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
    const signatureManager = new SignatureManager();

    const token = signatureManager.sign({
      employeeDocument: '55265344055',
      employeeRole: 'employee',
      isTemporary: false,
      storeUnit: 1
    });

    const result = signatureManager.checkIsValid(token);

    expect(result).toBeTruthy();

  });

  test('should check an invalid token', () => {
    jest.doMock('../../constants', () => ({
      JWT_SECRET: 'invalid-secret'
    })
    );
    let signatureManager = new SignatureManager();

    const token = signatureManager.sign({
      employeeDocument: '55265344055',
      employeeRole: 'employee',
      isTemporary: false,
      storeUnit: 1
    });

    jest.doMock('../../constants', () => ({
      JWT_SECRET: 'invalid-secret-2'
    }));

    signatureManager = new SignatureManager();

    const result = signatureManager.checkIsValid(token);

    expect(result).rejects.toBeFalsy();
  });
});
