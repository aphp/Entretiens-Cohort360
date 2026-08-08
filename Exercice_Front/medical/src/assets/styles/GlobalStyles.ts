// src/assets/styles/GlobalStyles.ts
import { createGlobalStyle } from 'styled-components';
import { Theme } from '@/config/theme';

interface GlobalStylesProps {
  theme: Theme;
}

const GlobalStyles = createGlobalStyle<GlobalStylesProps>`
  /* Import de polices */
  @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
  
  /* Reset */
  * {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
    -webkit-font-smoothing: antialiased;
    -moz-osx-font-smoothing: grayscale;
  }
  
  /* Base styles */
  html {
    font-size: 16px;
    scroll-behavior: smooth;
  }
  
  body {
    font-family: ${({ theme }) => theme.typography.fontFamily.sans};
    font-size: ${({ theme }) => theme.typography.fontSize.base};
    line-height: ${({ theme }) => theme.typography.lineHeight.normal};
    color: ${({ theme }) => theme.colors.text};
    background-color: ${({ theme }) => theme.colors.background};
    min-height: 100vh;
    overflow-x: hidden;
  }
  
  /* Typography */
  h1, h2, h3, h4, h5, h6 {
    font-weight: ${({ theme }) => theme.typography.fontWeight.semibold};
    line-height: ${({ theme }) => theme.typography.lineHeight.tight};
    margin-bottom: ${({ theme }) => theme.spacing[4]};
  }
  
  h1 {
    font-size: ${({ theme }) => theme.typography.fontSize['4xl']};
    color: ${({ theme }) => theme.colors.gray900};
  }
  
  h2 {
    font-size: ${({ theme }) => theme.typography.fontSize['3xl']};
    color: ${({ theme }) => theme.colors.gray800};
  }
  
  h3 {
    font-size: ${({ theme }) => theme.typography.fontSize['2xl']};
    color: ${({ theme }) => theme.colors.gray700};
  }
  
  p {
    margin-bottom: ${({ theme }) => theme.spacing[4]};
    color: ${({ theme }) => theme.colors.text};
  }
  
  /* Links */
  a {
    color: ${({ theme }) => theme.colors.primary};
    text-decoration: none;
    transition: color 0.2s ease;
    
    &:hover {
      color: ${({ theme }) => theme.colors.primaryDark};
      text-decoration: underline;
    }
  }
  
  /* Buttons */
  button {
    font-family: inherit;
    cursor: pointer;
    
    &:disabled {
      cursor: not-allowed;
      opacity: 0.6;
    }
  }
  
  /* Lists */
  ul, ol {
    margin-left: ${({ theme }) => theme.spacing[6]};
    margin-bottom: ${({ theme }) => theme.spacing[4]};
  }
  
  /* Forms */
  input,
  textarea,
  select {
    font-family: inherit;
    font-size: inherit;
    color: inherit;
    background-color: transparent;
    
    &:focus {
      outline: 2px solid ${({ theme }) => theme.colors.primary};
      outline-offset: 2px;
    }
  }
  
  /* Images */
  img {
    max-width: 100%;
    height: auto;
  }
  
  /* Accessibility - focus visible */
  :focus-visible {
    outline: 2px solid ${({ theme }) => theme.colors.primary};
    outline-offset: 2px;
  }
  
  /* Scrollbar styling */
  ::-webkit-scrollbar {
    width: 12px;
    height: 12px;
  }
  
  ::-webkit-scrollbar-track {
    background: ${({ theme }) => theme.colors.gray100};
    border-radius: ${({ theme }) => theme.borders.radius.full};
  }
  
  ::-webkit-scrollbar-thumb {
    background: ${({ theme }) => theme.colors.gray400};
    border-radius: ${({ theme }) => theme.borders.radius.full};
    border: 3px solid ${({ theme }) => theme.colors.gray100};
    
    &:hover {
      background: ${({ theme }) => theme.colors.gray500};
    }
  }
  
  /* Selection */
  ::selection {
    background-color: ${({ theme }) => theme.colors.primaryLight};
    color: ${({ theme }) => theme.colors.white};
  }
  
  /* Utility classes */
  .visually-hidden {
    position: absolute;
    width: 1px;
    height: 1px;
    padding: 0;
    margin: -1px;
    overflow: hidden;
    clip: rect(0, 0, 0, 0);
    white-space: nowrap;
    border: 0;
  }
  
  .text-truncate {
    overflow: hidden;
    text-overflow: ellipsis;
    white-space: nowrap;
  }
  
  /* Container utility */
  .container {
    width: 100%;
    max-width: 1200px;
    margin: 0 auto;
    padding: 0 ${({ theme }) => theme.spacing[4]};
    
    @media (min-width: ${({ theme }) => theme.breakpoints.lg}) {
      padding: 0 ${({ theme }) => theme.spacing[8]};
    }
  }
  
  /* Grid utilities */
  .grid {
    display: grid;
    gap: ${({ theme }) => theme.spacing[4]};
  }
  
  /* Flex utilities */
  .flex {
    display: flex;
  }
  
  .flex-center {
    display: flex;
    align-items: center;
    justify-content: center;
  }
  
  .flex-between {
    display: flex;
    align-items: center;
    justify-content: space-between;
  }
  
  /* Spacing utilities */
  .m-0 { margin: 0 !important; }
  .m-1 { margin: ${({ theme }) => theme.spacing[1]} !important; }
  .m-2 { margin: ${({ theme }) => theme.spacing[2]} !important; }
  .m-3 { margin: ${({ theme }) => theme.spacing[3]} !important; }
  .m-4 { margin: ${({ theme }) => theme.spacing[4]} !important; }
  .m-6 { margin: ${({ theme }) => theme.spacing[6]} !important; }
  
  .p-0 { padding: 0 !important; }
  .p-1 { padding: ${({ theme }) => theme.spacing[1]} !important; }
  .p-2 { padding: ${({ theme }) => theme.spacing[2]} !important; }
  .p-3 { padding: ${({ theme }) => theme.spacing[3]} !important; }
  .p-4 { padding: ${({ theme }) => theme.spacing[4]} !important; }
  .p-6 { padding: ${({ theme }) => theme.spacing[6]} !important; }
  
  /* Text utilities */
  .text-center { text-align: center; }
  .text-left { text-align: left; }
  .text-right { text-align: right; }
  
  /* Responsive utilities */
  @media (max-width: ${({ theme }) => theme.breakpoints.sm}) {
    .hide-sm { display: none !important; }
  }
  
  @media (max-width: ${({ theme }) => theme.breakpoints.md}) {
    .hide-md { display: none !important; }
  }
  
  @media (max-width: ${({ theme }) => theme.breakpoints.lg}) {
    .hide-lg { display: none !important; }
  }
  
  /* Dark mode */
  @media (prefers-color-scheme: dark) {
    body:not(.light-mode) {
      color: ${({ theme }) => theme.colors.textInverted};
      background-color: ${({ theme }) => theme.colors.backgroundDark};
    }
    
    body:not(.light-mode) h1 {
      color: ${({ theme }) => theme.colors.white};
    }
    
    body:not(.light-mode) a {
      color: ${({ theme }) => theme.colors.secondaryLight};
    }
  }
  
  /* Reduced motion */
  @media (prefers-reduced-motion: reduce) {
    *,
    *::before,
    *::after {
      animation-duration: 0.01ms !important;
      animation-iteration-count: 1 !important;
      transition-duration: 0.01ms !important;
      scroll-behavior: auto !important;
    }
  }
`;

export default GlobalStyles;