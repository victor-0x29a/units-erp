import type { Meta, StoryObj } from '@storybook/react';
import { fn } from '@storybook/test';
import { Button } from '../components/Button';

const meta = {
  title: 'Form/Button',
  component: Button,
  parameters: {
    layout: 'centered',
  },
  tags: ['!autodocs'],
  args: { onClick: fn() },
} satisfies Meta<typeof Button>;

export default meta;
type Story = StoryObj<typeof meta>;

export const Submit: Story = {
  args: {
    children: 'Submit',
    type: 'submit'
  },
};

export const Reset: Story = {
  args: {
    children: 'Reset',
    type: 'reset'
  },
};

export const Success: Story = {
  args: {
    children: 'Success',
    type: 'success'
  },
};

export const Disabled: Story = {
  args: {
    children: 'Disabled',
    disabled: true
  },
};

export const Loading: Story = {
  args: {
    children: 'Loading',
    isLoading: true
  },
};

export const CustomLoadingLabel: Story = {
  args: {
    children: 'Foo',
    isLoading: true,
    loadingLabel: 'Custom Loading Label'
  },
};
