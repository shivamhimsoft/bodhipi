import React, { useState } from 'react';
import { Inertia } from '@inertiajs/inertia';
import Layout from '../components/Layout';

const Register = ({ errors = {}, title = 'Register - Research Collaboration Platform', csrfToken = '' }) => {
  const [values, setValues] = useState({
    email: '',
    user_type: 'Student',
    password: '',
    password2: '',
    agree_terms: false
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
    Inertia.post('/register', values);
  };

  return (
    <Layout title={title}>
      <div className="container py-5">
        <div className="row justify-content-center">
          <div className="col-md-8">
            <div className="card bg-dark">
              <div className="card-header">
                <h3 className="mb-0">Register</h3>
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
                    <label htmlFor="user_type" className="form-label">User Type</label>
                    <select 
                      className={`form-select ${errors.user_type ? 'is-invalid' : ''}`}
                      id="user_type" 
                      name="user_type"
                      value={values.user_type}
                      onChange={handleChange}
                      required
                    >
                      <option value="Student">Student</option>
                      <option value="PI">Principal Investigator/Lab Director</option>
                      <option value="Industry">Industry/Company</option>
                      <option value="Vendor">Vendor/Service Provider</option>
                    </select>
                    {errors.user_type && <div className="invalid-feedback">{errors.user_type}</div>}
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
                    <div className="form-text">Password must be at least 8 characters long.</div>
                  </div>
                  
                  <div className="mb-3">
                    <label htmlFor="password2" className="form-label">Confirm Password</label>
                    <input 
                      type="password" 
                      className={`form-control ${errors.password2 ? 'is-invalid' : ''}`}
                      id="password2" 
                      name="password2"
                      value={values.password2}
                      onChange={handleChange}
                      required
                    />
                    {errors.password2 && <div className="invalid-feedback">{errors.password2}</div>}
                  </div>
                  
                  <div className="mb-3 form-check">
                    <input 
                      type="checkbox" 
                      className={`form-check-input ${errors.agree_terms ? 'is-invalid' : ''}`}
                      id="agree_terms" 
                      name="agree_terms"
                      checked={values.agree_terms}
                      onChange={handleChange}
                      required
                    />
                    <label className="form-check-label" htmlFor="agree_terms">
                      I agree to the Terms and Conditions
                    </label>
                    {errors.agree_terms && <div className="invalid-feedback">{errors.agree_terms}</div>}
                  </div>
                  
                  <div className="d-grid">
                    <button type="submit" className="btn btn-primary">Register</button>
                  </div>
                </form>
                
                <div className="mt-3 text-center">
                  <p>Already have an account? <a href="/login" className="link-info">Login here</a></p>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </Layout>
  );
};

export default Register;