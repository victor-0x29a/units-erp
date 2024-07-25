'use client';

import { useFormik } from 'formik';
import { Button, Column, TextInput } from '@/components';
import { LoginSchema, LoginInitialValues } from '@/schemas/auth/login';
import styles from './page.module.scss';
import Image from 'next/image';

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
          <Image src='/logo.png' alt='Logo' width={200} height={200} />
          <Column
            hasError={Boolean(formik.errors.username)}
            isTouched={formik.touched.username}
            error={formik.errors.username}
          >
            <TextInput
              label='Usuário'
              value={formik.values.username}
              onChange={formik.handleChange}
              onBlur={formik.handleBlur}
              name='username'
              type='text'
            />
          </Column>
          <Column
            hasError={Boolean(formik.errors.password)}
            isTouched={formik.touched.password}
            error={formik.errors.password}
          >
            <TextInput
              label='Senha'
              value={formik.values.password}
              onChange={formik.handleChange}
              onBlur={formik.handleBlur}
              name='password'
              type='password'
            />
          </Column>
          <Button type='submit'>Entrar</Button>
        </form>
      </div>
    </main>
  );
}
