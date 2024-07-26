import { mockedAxios } from "./__mocks__/axios.mock";
import { BackendModule } from "./backend.module";

const mockedPath = "foo";

describe("BackendModule", () => {
  it("should be defined", () => {
    expect(new BackendModule(mockedAxios, mockedPath)).toBeDefined();
  });

  it("should call get", async () => {
    const module = new BackendModule(mockedAxios, mockedPath);

    const getSpy = jest.spyOn(module, "get");

    const response = await module.get();

    expect(getSpy).toHaveBeenCalledTimes(1);

    expect(response.statusCode).toEqual(200);

    getSpy.mockRestore();
  });

  it("should call post", async () => {
    const module = new BackendModule(mockedAxios, mockedPath, {
      foo: "bar",
    });

    const postSpy = jest.spyOn(module, "post");

    const response = await module.post();

    const postMock = mockedAxios.create().post;

    expect(postMock).toHaveBeenCalledWith(
      expect.any(String),
      { foo: "bar" },
      expect.any(Object)
    );

    expect(postSpy).toHaveBeenCalledTimes(1);

    expect(response.statusCode).toEqual(200);

    postSpy.mockRestore();
  });

  it("should call put", async () => {
    const module = new BackendModule(mockedAxios, mockedPath, {
      foo: "bar",
    });

    const putSpy = jest.spyOn(module, "put");

    const response = await module.put();

    const putMock = mockedAxios.create().put;

    expect(putMock).toHaveBeenCalledWith(
      expect.any(String),
      { foo: "bar" },
      expect.any(Object)
    );

    expect(putSpy).toHaveBeenCalledTimes(1);

    expect(response.statusCode).toEqual(200);

    putSpy.mockRestore();
  });

  it("should call patch", async () => {
    const module = new BackendModule(mockedAxios, mockedPath, {
      foo: "bar",
    });

    const patchSpy = jest.spyOn(module, "patch");

    const response = await module.patch();

    const patchMock = mockedAxios.create().patch;

    expect(patchMock).toHaveBeenCalledWith(
      expect.any(String),
      { foo: "bar" },
      expect.any(Object)
    );

    expect(patchSpy).toHaveBeenCalledTimes(1);

    expect(response.statusCode).toEqual(200);

    patchSpy.mockRestore();
  });

  it("should call delete", async () => {
    const module = new BackendModule(mockedAxios, mockedPath);

    const deleteSpy = jest.spyOn(module, "delete");

    const response = await module.delete();

    const deleteMock = mockedAxios.create().delete;

    expect(deleteMock).toHaveBeenCalledWith(
      expect.any(String),
      expect.any(Object)
    );

    expect(deleteSpy).toHaveBeenCalledTimes(1);

    expect(response.statusCode).toEqual(200);

    deleteSpy.mockRestore();
  });
});

describe("BackendModule with params", () => {
  test("should transform params object to query string", async () => {
    const module = new BackendModule(mockedAxios, mockedPath, undefined, {
      foo2: "bar",
      baz: "qux",
    });

    const getSpy = jest.spyOn(module, "get");

    const response = await module.get();

    const getMock = mockedAxios.create().get;

    expect(getMock).toHaveBeenCalledWith(
      expect.stringMatching(/foo\/foo2\/bar\/baz\/qux/),
      expect.any(Object)
    );

    expect(getSpy).toHaveBeenCalledTimes(1);

    expect(response.statusCode).toEqual(200);

    getSpy.mockRestore();
  });
  test("should transform query object to query string", async () => {
    const module = new BackendModule(
      mockedAxios,
      mockedPath,
      undefined,
      undefined,
      {
        foo2: "bar",
        baz: "qux",
      }
    );

    const getSpy = jest.spyOn(module, "get");

    const response = await module.get();

    const getMock = mockedAxios.create().get;

    expect(getMock).toHaveBeenCalledWith(
      expect.stringMatching(/foo\?foo2=bar&baz=qux/),
      expect.any(Object)
    );

    expect(getSpy).toHaveBeenCalledTimes(1);

    expect(response.statusCode).toEqual(200);

    getSpy.mockRestore();
  });
});
