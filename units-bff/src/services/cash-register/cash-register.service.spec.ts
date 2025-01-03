import { Model, ModelCtor } from "sequelize";
import { CashRegisterService } from "./cash-register.service";
import { mockedRepository } from "./mocks/repository.mock";
import { CashRegisterClock } from "../../types/cash-register-clock";
import { Conflict, InternalError, MissingDoc, RetroactiveAction } from "../../exceptions";


describe('CashRegisterService::Clock::Create', () => {
  test('should create a new clock register', async () => {
    const repository = mockedRepository.creationCases.success as unknown as ModelCtor<Model<CashRegisterClock, CashRegisterClock>>;

    const service = new CashRegisterService(repository);

    const anonymousFn = async (): Promise<Model<CashRegisterClock, CashRegisterClock>> => await service.createClockRegister('55265344055');

    expect(anonymousFn).not.toThrow();

    const model = await anonymousFn();

    expect(model.toJSON().employee_document).toBe('55265344055');
  });
  test('should broke when try to create a new clock register', async () => {
    const repository = mockedRepository.creationCases.fail as unknown as ModelCtor<Model<CashRegisterClock, CashRegisterClock>>;

    const service = new CashRegisterService(repository);

    const anonymousFn = async (): Promise<Model<CashRegisterClock, CashRegisterClock>> => await service.createClockRegister('55265344055');

    expect(anonymousFn).rejects.toBeInstanceOf(InternalError);
  });
  test('should broke when try to find a register', async () => {
    const repository = mockedRepository.creationCases.whenFindOneFails as unknown as ModelCtor<Model<CashRegisterClock, CashRegisterClock>>;

    const service = new CashRegisterService(repository);

    const anonymousFn = async (): Promise<Model<CashRegisterClock, CashRegisterClock>> => await service.createClockRegister('55265344055');

    expect(anonymousFn).rejects.toBeInstanceOf(InternalError);
  });
  test(('should not create when has already exist a register with the same document and the same day'), async () => {
    const repository = mockedRepository.creationCases.failWhenAlreadyExistsBySameDayAndSameDocument as unknown as ModelCtor<Model<CashRegisterClock, CashRegisterClock>>;

    const service = new CashRegisterService(repository);

    await expect(service.createClockRegister('55265344055')).rejects.toBeInstanceOf(Conflict);
  });
});

describe('CashRegisterService::Clock::Toggle', () => {
  test('should toggle a clock register on clock out', async () => {
    const repository = mockedRepository.toggleCases.success.lastClockOut as unknown as ModelCtor<Model<CashRegisterClock, CashRegisterClock>>;

    const service = new CashRegisterService(repository);

    const model = await repository.findByPk(1);

    const updateSpy = jest.spyOn(model, 'update');

    await expect(service.toggleClock(1)).resolves.not.toThrow();

    expect(updateSpy).toHaveBeenCalled();

    expect(updateSpy).toHaveBeenCalledWith({ clock_out: expect.any(Date) });
  });


  test('should toggle a clock register on lunch in', async () => {
    const repository = mockedRepository.toggleCases.success.clockLunchIn as unknown as ModelCtor<Model<CashRegisterClock, CashRegisterClock>>;

    const service = new CashRegisterService(repository);

    const model = await repository.findByPk(1);

    const updateSpy = jest.spyOn(model, 'update');

    await expect(service.toggleClock(1)).resolves.not.toThrow();

    expect(updateSpy).toHaveBeenCalled();

    expect(updateSpy).toHaveBeenCalledWith({ clock_lunch_in: expect.any(Date) });
  });

  test('should toggle a clock register on lunch out', async () => {
    const repository = mockedRepository.toggleCases.success.clockLunchOut as unknown as ModelCtor<Model<CashRegisterClock, CashRegisterClock>>;

    const service = new CashRegisterService(repository);

    const model = await repository.findByPk(1);

    const updateSpy = jest.spyOn(model, 'update');

    await expect(service.toggleClock(1)).resolves.not.toThrow();

    expect(updateSpy).toHaveBeenCalled();

    expect(updateSpy).toHaveBeenCalledWith({ clock_lunch_out: expect.any(Date) });
  });
  test('should toggle a clock register on the first time', async () => {
    const repository = mockedRepository.toggleCases.success.clockIn as unknown as ModelCtor<Model<CashRegisterClock, CashRegisterClock>>;

    const service = new CashRegisterService(repository);

    const model = await repository.findByPk(1);

    const updateSpy = jest.spyOn(model, 'update');

    await expect(service.toggleClock(1)).resolves.not.toThrow();

    expect(updateSpy).toHaveBeenCalled();

    expect(updateSpy).toHaveBeenCalledWith({ clock_in: expect.any(Date) });
  });
  test('should not toggle the clock register when has already clocked out', async () => {
    const repository = mockedRepository.toggleCases.fail.clockedOut as unknown as ModelCtor<Model<CashRegisterClock, CashRegisterClock>>;

    const service = new CashRegisterService(repository);

    await expect(service.toggleClock(1)).rejects.toBeInstanceOf(RetroactiveAction);
  });
  test('should not toggle to an unexistent register', async () => {
    const repository = mockedRepository.toggleCases.fail.notFound as unknown as ModelCtor<Model<CashRegisterClock, CashRegisterClock>>;

    const service = new CashRegisterService(repository);

    await expect(service.toggleClock(1)).rejects.toBeInstanceOf(MissingDoc);
  });
  test('should not toggle when have an error on .update', async () => {
    const repository = mockedRepository.toggleCases.fail.clockLunchInUpdateFail as unknown as ModelCtor<Model<CashRegisterClock, CashRegisterClock>>;

    const service = new CashRegisterService(repository);

    const model = await repository.findByPk(1);

    const updateSpy = jest.spyOn(model, 'update');

    await expect(service.toggleClock(1)).rejects.toBeInstanceOf(InternalError);

    expect(updateSpy).toHaveBeenCalled();

    expect(updateSpy).toHaveBeenCalledWith({ clock_lunch_in: expect.any(Date) });
  });
  test('should not toggle when have an error on ORM', async () => {
    const repository = mockedRepository.toggleCases.fail.ormInternalError as unknown as ModelCtor<Model<CashRegisterClock, CashRegisterClock>>;

    const service = new CashRegisterService(repository);

    await expect(service.toggleClock(1)).rejects.toBeInstanceOf(InternalError);
  });
});
