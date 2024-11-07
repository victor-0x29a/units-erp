'use client';

import { useFormik } from 'formik';
import { Button } from '@/components/ui/button';
import { Field } from '@/components/ui/field';
import { Input, Stack } from '@chakra-ui/react';
import { LoginSchema, LoginInitialValues } from '@/schemas/auth/login';
import styles from './page.module.scss';

export default function Home() {
  const formik = useFormik({
    initialValues: LoginInitialValues,
    validationSchema: LoginSchema,
    onSubmit: () => {},
    validateOnBlur: false,
    validateOnChange: false
  });

  return (
    <main>
      <div className={styles.box}>
        <form onSubmit={formik.handleSubmit}>
            <Stack gap="5" maxW={'sm'}>
                <Field
                    label='Usuário'
                    invalid={Boolean(formik.errors.username)}
                    errorText={formik.errors.username}>
                    <Input
                        value={formik.values.username}
                        onChange={formik.handleChange}
                        onBlur={formik.handleBlur}
                        name='username'
                        type='text'
                    />
                </Field>
                <Field
                    label='Senha'
                    invalid={Boolean(formik.errors.password)}
                    errorText={formik.errors.password}>
                    <Input
                        value={formik.values.password}
                        onChange={formik.handleChange}
                        onBlur={formik.handleBlur}
                        name='password'
                        type='password'
                    />
                </Field>
                <Button
                    type='submit'
                    variant={'solid'}
                    colorPalette={'orange'}
                    width={'100%'}>
                    Entrar
                </Button>
            </Stack>
        </form>
      </div>
    </main>
  );
}
