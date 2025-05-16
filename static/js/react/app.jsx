import React from 'react';
import { createRoot } from 'react-dom/client';
import { createInertiaApp } from '@inertiajs/inertia-react';
import { InertiaProgress } from '@inertiajs/progress';

// Import components
import Home from './pages/Home';
import Layout from './components/Layout';

// Initialize progress indicator
InertiaProgress.init();

// Page component resolver
const resolveComponent = (name) => {
  const pages = {
    'Home': Home
  };
  
  return pages[name];
};

// Initialize Inertia
document.addEventListener('DOMContentLoaded', () => {
  const el = document.getElementById('app');
  
  if (!el) {
    console.error('Root element #app not found');
    return;
  }
  
  // Get page data from the data-page attribute
  const pageElement = el.dataset.page;
  const page = pageElement ? JSON.parse(decodeURIComponent(pageElement)) : null;
  
  if (!page) {
    console.error('Page data not found');
    return;
  }
  
  createInertiaApp({
    resolve: resolveComponent,
    setup({ el, App, props }) {
      createRoot(el).render(<App {...props} />);
    },
    page
  });
});