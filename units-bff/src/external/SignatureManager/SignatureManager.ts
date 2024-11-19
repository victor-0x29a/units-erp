import jwt, { TokenExpiredError, JsonWebTokenError } from 'jsonwebtoken';
import moment from 'moment-timezone';
import { getByTimestamp, getNow } from "../../utils";
import { JWT_SECRET } from "../../constants";
import type { DecodedToken, ParsedDecodedToken, SignPayload } from "./types/SignatureManager";
import { ExpiredAuthorization, InvalidAuthorization, InternalError } from '../../exceptions';

class SignatureManager {
  public sign(payload: SignPayload): string {
    return jwt.sign({
      employee_document: payload.employeeDocument,
      employee_role: payload.employeeRole,
      is_temporary: payload.isTemporary,
      store_unit: payload.storeUnit
    }, JWT_SECRET, {
      expiresIn: '2h'
    });
  }
  public decode(token: string): ParsedDecodedToken {
    const decodedToken: DecodedToken = jwt.decode(token, {
      complete: true,
      json: true
    }).payload as unknown as DecodedToken;

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
      jwt.verify(token, JWT_SECRET, (error, _decoded) => {
        if (error) {
          if (error instanceof TokenExpiredError) {
            reject(new ExpiredAuthorization(["Token expired"], error));
          }
          if (error instanceof JsonWebTokenError) {
            return reject(new InvalidAuthorization(["Invalid token"], error));
          }

          return reject(new InternalError(error));
        }

        resolve(true);
      });
    });
  }
  public checkIsExpired(exp: number, isGeneratedBySignatureManager = false): boolean {
    const now = getNow();
    if (isGeneratedBySignatureManager) {
      return moment(exp * 1000).isBefore(now);
    }
    const expirationDatetime = getByTimestamp(exp);
    return moment(expirationDatetime).isBefore(now);
  }
}

export { SignatureManager };
