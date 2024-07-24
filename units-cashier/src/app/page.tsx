'use client';

import { useFormik } from 'formik';
import { Button } from '@/components';
import { LoginSchema, LoginInitialValues } from '@/schemas/auth/login';
import styles from './page.module.scss';

export default function Home() {
  const formik = useFormik({
    initialValues: LoginInitialValues,
    validationSchema: LoginSchema,
    onSubmit: () => {}
  });

  return (
    <main>
      <div className="box">
        <form className={styles['login-form']} onSubmit={formik.handleSubmit}>
          <Button type="success">Log-in</Button>
        </form>
      </div>
    </main>
  );
}
