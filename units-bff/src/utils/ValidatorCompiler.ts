export const ValidatorCompiler = ({ schema }) => {
  return (data) => {
    try {
      const result = schema.validateSync(data, {
        strict: false,
        abortEarly: false,
        stripUnknown: true,
        recursive: true,
      });
      return { value: result };
    } catch (error) {
      return { error };
    }
  };
};
