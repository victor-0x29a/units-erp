import { CashRegisterClock } from "../../entity";
import type { CashRegisterClock as CashRegisterClockType } from "../../types/cash-register-clock";
import { InternalError, MissingDoc, RetroactiveAction } from "../../exceptions";
import { Model } from "sequelize";
import { getNow } from "../../utils";


class CashRegisterService {
  constructor (private cashRegisterClockModel: typeof CashRegisterClock) {}

  public async createClockRegister(employeeDocument: string): Promise<Model<CashRegisterClockType, CashRegisterClockType>> {
    return this.cashRegisterClockModel
      .create({ employee_document: employeeDocument, clock_in: getNow() })
      .catch((error: unknown) => Promise.reject(new InternalError(error)));
  }
  public async toggleClock(clockRegisterId: number) {
    return this.cashRegisterClockModel
      .findByPk(clockRegisterId)
      .then((register: Model<CashRegisterClockType, CashRegisterClockType> | null) => {
        if (!register) {
          return Promise.reject(new MissingDoc(["Register not found."]));
        }

        const registerData = register.toJSON();

        const hasAlreadyClockIn = registerData.clock_in !== null;
        const hasAlreadyClockLunchIn = registerData.clock_lunch_in !== null;
        const hasAlreadyClockLunchOut = registerData.clock_lunch_out !== null;
        const hasAlreadyClockOut = registerData.clock_out !== null;

        if (!hasAlreadyClockIn) {
          return register.update({ clock_in: getNow() })
            .catch((error: unknown) => Promise.reject(new InternalError(error)));
        }

        if (hasAlreadyClockOut) {
          return Promise.reject(new RetroactiveAction(["You can't clock out twice by day."]));
        }

        if (!hasAlreadyClockLunchIn && !hasAlreadyClockLunchOut) {
          return register.update({ clock_lunch_in: getNow() })
            .catch((error: unknown) => Promise.reject(new InternalError(error)));
        }

        if (hasAlreadyClockLunchIn && !hasAlreadyClockLunchOut) {
          return register.update({ clock_lunch_out: getNow() })
            .catch((error: unknown) => Promise.reject(new InternalError(error)));
        }

        return register.update({ clock_out: getNow() })
          .catch((error: unknown) => Promise.reject(new InternalError(error)));
      })
      .catch((error: unknown) => Promise.reject(new InternalError(error)));
  }
}

export { CashRegisterService };
