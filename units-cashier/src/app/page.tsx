"use client"

import { TextInput, Button } from "@/components";
import { useState } from "react";
import styles from "./page.module.scss";

export default function Home() {
  const [value, setValue] = useState<string>("");
  const callBack = (field: string) => (value: string) => setValue(value);
  return (
    <main>
      <div className="box">
        <form className={styles['login-form']}>
          <TextInput label="Usuário" onChange={callBack('user')} onBlur={() => { }} value={value} />
          <TextInput label="Senha" onChange={callBack('password')} onBlur={() => { }} value={value} />
          <Button label="Entrar" type="success" />
        </form>
      </div>
    </main>
  );
}
