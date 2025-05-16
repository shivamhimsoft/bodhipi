import React from 'react';
import { createRoot } from 'react-dom/client';
import { createInertiaApp } from '@inertiajs/inertia-react';
import { InertiaProgress } from '@inertiajs/progress';

// Import all page components
import Home from './pages/Home';
import Layout from './components/Layout';

// Initialize progress indicator
InertiaProgress.init({
  color: '#4B5563',
  showSpinner: true,
});

// Component resolver function
const resolveComponent = (name) => {
  const pages = {
    'Home': Home
    // Add more pages as needed
  };
  
  const Component = pages[name];
  if (!Component) {
    console.error(`Component ${name} not found in the pages object`);
    return null;
  }
  
  return Component;
};

// Create and mount the Inertia app
document.addEventListener('DOMContentLoaded', () => {
  const el = document.getElementById('app');
  
  if (!el) {
    console.error('Root element #app not found');
    return;
  }
  
  try {
    // Get page data from the global window object
    const pageData = window.pageData || {
      component: 'Home',
      props: { 
        title: 'Research Collaboration Platform',
        opportunities: [],
        profiles: [],
        stats: {
          users: 0,
          labs: 0,
          opportunities: 0,
          collaborations: 0
        }
      },
      url: window.location.pathname
    };
    
    // Initialize the Inertia app
    createInertiaApp({
      resolve: resolveComponent,
      setup({ el, App, props }) {
        createRoot(el).render(<App {...props} />);
      },
      page: pageData
    });
    
    console.log('Inertia app initialized successfully');
  } catch (error) {
    console.error('Error initializing Inertia app:', error);
  }
});