import React from 'react';
import { createRoot } from 'react-dom/client';
import { createInertiaApp } from '@inertiajs/inertia-react';

// Import components
import Home from './pages/Home';
import Layout from './components/Layout';

// Component mapping
const pages = {
  'Home': Home
};

createInertiaApp({
  // The page data comes from the server through Inertia
  resolve: name => {
    return pages[name];
  },
  setup({ el, App, props }) {
    createRoot(el).render(<App {...props} />);
  },
});