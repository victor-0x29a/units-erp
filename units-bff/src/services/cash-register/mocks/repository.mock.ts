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
      }),
      findOne: jest.fn().mockResolvedValue(null)
    },
    fail: {
      create: jest.fn().mockRejectedValue(new InternalError(null)),
      findOne: jest.fn().mockResolvedValue(null)
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
      clockLunchIn: {
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
      clockLunchOut: {
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
      clockIn: {
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
    },
    fail: {
      clockedOut: {
        findByPk: jest.fn().mockResolvedValue({
          toJSON: jest.fn().mockReturnValue({
            id: 1,
            employee_document: '55265344055',
            clock_in: new Date(),
            clock_out: new Date(),
            clock_lunch_in: new Date(),
            clock_lunch_out: new Date()
          })
        }),
      },
      notFound: {
        findByPk: jest.fn().mockResolvedValue(null)
      },
      clockLunchInUpdateFail: {
        findByPk: jest.fn().mockResolvedValue({
          toJSON: jest.fn().mockReturnValue({
            id: 1,
            employee_document: '55265344055',
            clock_in: new Date(),
            clock_out: null,
            clock_lunch_in: null,
            clock_lunch_out: null
          }),
          update: jest.fn().mockRejectedValue(new Error())
        })
      },
      ormInternalError: {
        findByPk: jest.fn().mockRejectedValue(new Error('ORM ERROR'))
      }
    }
  }
};
