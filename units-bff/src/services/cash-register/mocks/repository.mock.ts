import { InternalError } from "../../../exceptions";

export const mockedRepository = {
  creationCases: {
    success: {
      create: jest.fn().mockResolvedValue({
        toJSON: jest.fn().mockReturnValue({
          id: 1,
          employee_document: '55265344055',
          clock_in: new Date(),
          clock_out: null,
          clock_lunch_in: null,
          clock_lunch_out: null
        })
      })
    },
    fail: {
      create: jest.fn().mockRejectedValue(new InternalError(null))
    },
    failWhenAlreadyExistsBySameDayAndSameDocument: {
      findOne: jest.fn().mockResolvedValue({
        toJSON: jest.fn().mockReturnValue({
          id: 1,
          employee_document: '55265344055',
          clock_in: new Date(),
          clock_out: null,
          clock_lunch_in: null,
          clock_lunch_out: null
        })
      })
    }
  },
  toggleCases: {
    success: {
      lastClockOut: {
        findByPk: jest.fn().mockResolvedValue({
          toJSON: jest.fn().mockReturnValue({
            id: 1,
            employee_document: '55265344055',
            clock_in: new Date(),
            clock_out: null,
            clock_lunch_in: new Date(),
            clock_lunch_out: new Date()
          }),
          update: jest.fn().mockResolvedValue(null)
        })
      },
      clock_lunch_in: {
        findByPk: jest.fn().mockResolvedValue({
          toJSON: jest.fn().mockReturnValue({
            id: 1,
            employee_document: '55265344055',
            clock_in: new Date(),
            clock_out: null,
            clock_lunch_in: null,
            clock_lunch_out: null
          }),
          update: jest.fn().mockResolvedValue(null)
        })
      },
      clock_lunch_out: {
        findByPk: jest.fn().mockResolvedValue({
          toJSON: jest.fn().mockReturnValue({
            id: 1,
            employee_document: '55265344055',
            clock_in: new Date(),
            clock_lunch_in: new Date(),
            clock_out: null,
            clock_lunch_out: null
          }),
          update: jest.fn().mockResolvedValue(null)
        })
      },
      clock_in: {
        findByPk: jest.fn().mockResolvedValue({
          toJSON: jest.fn().mockReturnValue({
            id: 1,
            employee_document: '55265344055',
            clock_in: null,
            clock_lunch_in: null,
            clock_out: null,
            clock_lunch_out: null
          }),
          update: jest.fn().mockResolvedValue(null)
        })
      }
    }
  }
};
