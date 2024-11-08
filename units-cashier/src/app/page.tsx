'use client';

import { useFormik } from 'formik';
import { Input, Link, Stack, Text } from '@chakra-ui/react';
import { Field, Button, Prose, Tooltip } from '@/components';
import { LoginSchema, LoginInitialValues } from '@/schemas/auth/login';
import Image from 'next/image';
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
        <main className={styles.container}>
            <div className={styles.side}>
                <Prose size={'lg'}>
                    <span>
                        <Image src={'https://img.freepik.com/fotos-gratis/retrato-de-um-mulher-negocio-trabalhar-laptop_1303-9733.jpg'} alt={'Logo'} width={600} height={600} />
                    </span>
                    <h1>Construindo a tecnologia</h1>
                    <p>
                    Venha conhecer o <Link  href='https://github.com/victor-0x29a/units-erp'>melhor ERP do mercado</Link> para o seu varejo.
                    Aumente a eficiência e impulsione suas vendas com nossa solução inovadora!
                    </p>
                </Prose>
            </div>
            <div className={styles.side}>
                <div className='image-container'>
                    <Image src="/logo.svg" alt='Units - ERP Logo' width={100} height={100}/>
                </div>
                <form onSubmit={formik.handleSubmit} className={styles.form}>
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
                    <Text fontSize={'small'} marginTop={'0.5'}>
                        Precisa de suporte? <Tooltip content='Esqueceu sua senha ou está enfrentando algum problema?' openDelay={200} closeDelay={100}>
                            <Link href='/help'>Clique aqui</Link>
                        </Tooltip>
                    </Text>
                </form>
            </div>
        </main>
    );
}
