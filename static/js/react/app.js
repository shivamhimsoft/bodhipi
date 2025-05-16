import React from 'react';
import { createRoot } from 'react-dom/client';
import { createInertiaApp } from '@inertiajs/inertia-react';
import { InertiaProgress } from '@inertiajs/inertia';

InertiaProgress.init({
  color: '#4a6fdc',
  showSpinner: true,
});

createInertiaApp({
  resolve: name => require(`./pages/${name}`),
  setup({ el, App, props }) {
    const root = createRoot(el);
    root.render(<App {...props} />);
  },
});