import type { Preview } from "@storybook/react";
import "../src/app/globals.scss"

const preview: Preview = {
  parameters: {
    // backgrounds: {
    //   default: 'black',
    //   values: [
    //     {
    //       name: 'black',
    //       value: '#000000',
    //     },
    //   ],
    // },
    controls: {
      matchers: {
        color: /(background|color)$/i,
        date: /Date$/i,
      },
    },
  },
};

export default preview;
