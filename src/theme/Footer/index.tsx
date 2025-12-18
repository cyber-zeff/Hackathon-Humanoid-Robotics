import React, {type ReactNode} from 'react';
import Footer from '@theme-original/Footer';
import type FooterType from '@theme/Footer';
import type {WrapperProps} from '@docusaurus/types';
import Chatbot from '../Chatbot'; // Import the Chatbot

type Props = WrapperProps<typeof FooterType>;

export default function FooterWrapper(props: Props): ReactNode {
  return (
    <>
      <Footer {...props} />
      <Chatbot />
    </>
  );
}
