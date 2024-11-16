import jwt from 'jsonwebtoken';
import { JWT_SECRET } from "../constants";
import type { DecodedToken, ParsedDecodedToken } from "./types/SignatureManager";

class SignatureManager {
  public decode(token: string): ParsedDecodedToken {
    const decodedToken: DecodedToken = jwt.decode(token, {
      complete: true,
      json: true
    }) as unknown as DecodedToken;

    return {
      employeeDocument: decodedToken.employee_document,
      employeeRole: decodedToken.employee_role,
      isTemporary: decodedToken.is_temporary,
      storeUnit: decodedToken.store_unit,
      iat: decodedToken.iat,
      exp: decodedToken.exp
    };
  }
  public async checkIsValid(token: string): Promise<boolean> {
    return new Promise((resolve, reject) => {
      return jwt.verify(token, JWT_SECRET, (error) => {
        if (error) {
          return reject(error);
        }

        resolve(true);
      });
    });
  }
}

export { SignatureManager };
