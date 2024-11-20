import { SignatureManager } from "../../external";
import { ExternalError, InvalidCredentials, Unprocessable } from "../../exceptions";

const signatureManager = new SignatureManager();

beforeEach(() => {
  jest.resetAllMocks();
  jest.resetModules();
});

describe("EmployeeService::Authentication all success cases", () => {
  test("should authenticate an employee", async () => {
    jest.doMock('../../core', () => ({
      privateDomains: {
        employeeDomain: {
          login: jest.fn().mockResolvedValue("Bearer token")
        }
      }
    }));

    const { EmployeeService } = await import("./employee.service");

    const employeeService = new EmployeeService(signatureManager);

    const token = await employeeService.login({
      username: "victor-0x29a",
      password: null,
      document: null
    });

    expect(token).toBe("Bearer token");
  });

  test("should authenticate an employee with password", async () => {
    jest.doMock('../../core', () => ({
      privateDomains: {
        employeeDomain: {
          login: jest.fn().mockResolvedValue("Bearer token")
        }
      }
    }));

    const { EmployeeService } = await import("./employee.service");

    const employeeService = new EmployeeService(signatureManager);

    const token = await employeeService.login({
      username: "victor-0x29a",
      password: "kkoo",
      document: null
    });

    expect(token).toBe("Bearer token");
  });
});

describe("EmployeeService::Authentication all error cases", () => {
  test("should reject when non existing employee", async () => {
    jest.doMock('../../core', () => ({
      privateDomains: {
        employeeDomain: {
          login: jest.fn().mockRejectedValue({
            "code": 1003,
            "message": "Employee not found.",
            "errors": [],
            "statusCode": 404
          })
        }
      }
    }));

    const { EmployeeService } = await import("./employee.service");

    const employeeService = new EmployeeService(signatureManager);

    const anonymousFnLogin = async () => await employeeService.login({
      username: "victor-0x29a",
      password: "foo",
      document: null
    });

    expect(anonymousFnLogin).rejects.toBeDefined();
    expect(anonymousFnLogin).rejects.toEqual(new InvalidCredentials());
  });
  test("should reject when wrong the password", async () => {
    jest.doMock('../../core', () => ({
      privateDomains: {
        employeeDomain: {
          login: jest.fn().mockRejectedValue({
            "code": 1070,
            "message": "Failed on process.",
            "errors": [],
            "statusCode": 422
          })
        }
      }
    }));

    const { EmployeeService } = await import("./employee.service");

    const employeeService = new EmployeeService(signatureManager);

    const anonymousFnLogin = async () => await employeeService.login({
      username: "victor-0x29a",
      password: "foo",
      document: null
    });

    expect(anonymousFnLogin).rejects.toBeDefined();
    expect(anonymousFnLogin).rejects.toEqual(new InvalidCredentials());
  });
  test("should reject when broke the external service", async () => {
    jest.doMock('../../core', () => ({
      privateDomains: {
        employeeDomain: {
          login: jest.fn().mockRejectedValue({
            "code": 500,
            "message": "Internal error.",
            "errors": [],
            "statusCode": 500
          })
        }
      }
    }));

    const { EmployeeService } = await import("./employee.service");

    const employeeService = new EmployeeService(signatureManager);

    const anonymousFnLogin = async () => await employeeService.login({
      username: "victor-0x29a",
      password: "foo",
      document: null
    });

    expect(anonymousFnLogin).rejects.toBeDefined();
    expect(anonymousFnLogin).rejects.toEqual(new ExternalError({
      "code": 500,
      "message": "Internal error.",
      "errors": [],
      "statusCode": 500
    }));
  });

});

describe("EmployeeService::Fill password all cases", () => {
  test("should fill the password", async () => {
    jest.doMock('../../core', () => ({
      privateDomains: {
        employeeDomain: {
          fillPassword: jest.fn().mockResolvedValue(undefined)
        }
      }
    }));

    const { EmployeeService } = await import("./employee.service");

    const token = signatureManager.sign({
      employeeDocument: "12345678901",
      employeeRole: "OPERATOR",
      isTemporary: true,
      storeUnit: 1
    });

    const employeeService = new EmployeeService(signatureManager);

    await expect(employeeService.fillPassword(token, {
      password: 'foo'
    })).resolves.toBeUndefined();
  });
  test('should reject when the token is temporary', async () => {
    jest.doMock('../../core', () => ({
      privateDomains: {
        employeeDomain: {
          fillPassword: jest.fn().mockResolvedValue(undefined)
        }
      }
    }));

    const { EmployeeService } = await import("./employee.service");

    const token = signatureManager.sign({
      employeeDocument: "12345678901",
      employeeRole: "OPERATOR",
      isTemporary: false,
      storeUnit: 1
    });

    const employeeService = new EmployeeService(signatureManager);

    await expect(employeeService.fillPassword(token, {
      password: 'foo'
    })).rejects.toEqual(new Unprocessable(["You can't change your password."]));
  });
  test('should reject when the external service broke', async () => {
    jest.doMock('../../core', () => ({
      privateDomains: {
        employeeDomain: {
          fillPassword: jest.fn().mockRejectedValue({
            "code": 500,
            "message": "Internal error.",
            "errors": [],
            "statusCode": 500
          })
        }
      }
    }));

    const { EmployeeService } = await import("./employee.service");

    const token = signatureManager.sign({
      employeeDocument: "12345678901",
      employeeRole: "OPERATOR",
      isTemporary: true,
      storeUnit: 1
    });

    const employeeService = new EmployeeService(signatureManager);

    await expect(employeeService.fillPassword(token, {
      password: 'foo'
    })).rejects.toEqual(new ExternalError({
      "code": 500,
      "message": "Internal error.",
      "errors": [],
      "statusCode": 500
    }));
  });
});
