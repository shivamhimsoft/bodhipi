import React, { useState } from 'react';
import { Inertia } from '@inertiajs/inertia';
import Layout from '../components/Layout';

const Login = ({ errors = {}, title = 'Login - Research Collaboration Platform', csrfToken = '' }) => {
  const [values, setValues] = useState({
    email: '',
    password: '',
    remember_me: false
  });

  const handleChange = (e) => {
    const key = e.target.name;
    const value = e.target.type === 'checkbox' ? e.target.checked : e.target.value;
    
    setValues(values => ({
      ...values,
      [key]: value,
    }));
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    Inertia.post('/login', values);
  };

  return (
    <Layout title={title}>
      <div className="container py-5">
        <div className="row justify-content-center">
          <div className="col-md-6">
            <div className="card bg-dark">
              <div className="card-header">
                <h3 className="mb-0">Login</h3>
              </div>
              <div className="card-body">
                <form onSubmit={handleSubmit}>
                  <input type="hidden" name="csrf_token" value={csrfToken} />
                  
                  <div className="mb-3">
                    <label htmlFor="email" className="form-label">Email Address</label>
                    <input 
                      type="email" 
                      className={`form-control ${errors.email ? 'is-invalid' : ''}`}
                      id="email" 
                      name="email"
                      value={values.email}
                      onChange={handleChange}
                      required
                    />
                    {errors.email && <div className="invalid-feedback">{errors.email}</div>}
                  </div>
                  
                  <div className="mb-3">
                    <label htmlFor="password" className="form-label">Password</label>
                    <input 
                      type="password" 
                      className={`form-control ${errors.password ? 'is-invalid' : ''}`}
                      id="password" 
                      name="password"
                      value={values.password}
                      onChange={handleChange}
                      required
                    />
                    {errors.password && <div className="invalid-feedback">{errors.password}</div>}
                  </div>
                  
                  <div className="mb-3 form-check">
                    <input 
                      type="checkbox" 
                      className="form-check-input" 
                      id="remember_me" 
                      name="remember_me"
                      checked={values.remember_me}
                      onChange={handleChange}
                    />
                    <label className="form-check-label" htmlFor="remember_me">Remember Me</label>
                  </div>
                  
                  <div className="d-grid">
                    <button type="submit" className="btn btn-primary">Sign In</button>
                  </div>
                </form>
                
                <div className="mt-3 text-center">
                  <p>Don't have an account? <a href="/register" className="link-info">Register here</a></p>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </Layout>
  );
};

export default Login;