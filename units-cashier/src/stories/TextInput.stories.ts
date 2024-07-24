import type { Meta, StoryObj } from '@storybook/react';
import { fn } from '@storybook/test';
import { TextInput } from '../components/TextInput';

const meta = {
  title: 'Form/TextInput',
  component: TextInput,
  parameters: {
    layout: 'centered',
  },
  tags: ['!autodocs'],
  args: { onBlur: fn(), onChange: fn() },
} satisfies Meta<typeof TextInput>;

export default meta;
type Story = StoryObj<typeof meta>;

export const Text: Story = {
  args: {
    label: 'User',
    value: 'John Doe'
  },
};

export const Password: Story = {
  args: {
    label: 'Password',
    value: 'password',
  },
};
