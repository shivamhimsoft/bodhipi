import React from 'react';
import { createRoot } from 'react-dom/client';
import { createInertiaApp } from '@inertiajs/inertia-react';
import { InertiaProgress } from '@inertiajs/progress';
import { Inertia } from '@inertiajs/inertia';

// Import all page components
import Home from './pages/Home';
import Login from './pages/Login';
import Register from './pages/Register';
import Layout from './components/Layout';

// Configure Inertia
Inertia.on('navigate', (event) => {
  // This helps debug navigation issues
  console.log('Navigating to:', event.detail.page.url);
});

// Initialize progress indicator
InertiaProgress.init({
  color: '#4B5563',
  showSpinner: true,
});

// Component resolver function
const resolveComponent = (name) => {
  // Register all page components here
  const pages = {
    'Home': Home,
    'Login': Login,
    'Register': Register
    // Add more pages as more components are created
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
    
    // Initialize the Inertia app with proper visit options
    createInertiaApp({
      resolve: resolveComponent,
      setup({ el, App, props }) {
        createRoot(el).render(<App {...props} />);
      },
      page: pageData,
      // Add the following to ensure proper link handling
      visit: {
        preserveState: true,
        preserveScroll: true,
        replace: false,
        onBefore: () => true,
        onStart: () => console.log('Navigation started'),
        onFinish: () => console.log('Navigation finished'),
        onSuccess: () => console.log('Navigation succeeded'),
        onError: () => console.log('Navigation failed')
      }
    });
    
    // Configure Inertia global settings
    Inertia.on('success', (event) => {
      console.log('Page loaded successfully', event.detail.page.component);
    });
    
    console.log('Inertia app initialized successfully');
  } catch (error) {
    console.error('Error initializing Inertia app:', error);
  }
});