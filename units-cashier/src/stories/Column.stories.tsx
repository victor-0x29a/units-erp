import React from 'react'; // Ensure React is imported for JSX support
import type { Meta, StoryObj } from '@storybook/react';
import { Column, TextInput } from '../components';

const meta: Meta<typeof Column> = {
  title: 'Form/Column',
  component: Column,
  parameters: {
    layout: 'centered',
  },
  tags: ['!autodocs'],
};

export default meta;
type Story = StoryObj<typeof meta>;

export const WithoutError: Story = {
  args: {
    children: (
        <>
            <TextInput label='Foo label' onBlur={() => {}} onChange={() => {}} value='foo value' type='text'/>
        </>
    )
  },
};

export const WithError: Story = {
  args: {
    children: (
        <>
            <TextInput label='Foo label' onBlur={() => {}} onChange={() => {}} value='foo value' type='text'/>
        </>
    ),
    hasError: true,
    isTouched: true,
    isDisabled: false,
    error: 'This is an error message'
  },
};