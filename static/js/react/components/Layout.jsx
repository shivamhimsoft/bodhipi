import React from 'react';
import { usePage } from '@inertiajs/inertia-react';
import { Link } from '@inertiajs/inertia-react';

export default function Layout({ children, title = 'Research Collaboration Platform' }) {
  const { auth, flash } = usePage().props;
  
  return (
    <div className="d-flex flex-column min-vh-100">
      {/* Header/Navbar */}
      <nav className="navbar navbar-expand-lg navbar-dark bg-dark mb-4">
        <div className="container">
          <Link className="navbar-brand" href="/">Research Collaboration</Link>
          <button className="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav">
            <span className="navbar-toggler-icon"></span>
          </button>
          <div className="collapse navbar-collapse" id="navbarNav">
            <ul className="navbar-nav me-auto">
              <li className="nav-item">
                <Link className="nav-link" href="/">Home</Link>
              </li>
              <li className="nav-item">
                <Link className="nav-link" href="/opportunities">Opportunities</Link>
              </li>
              <li className="nav-item">
                <Link className="nav-link" href="/search">Search</Link>
              </li>
              <li className="nav-item">
                <Link className="nav-link" href="/documentation">Documentation</Link>
              </li>
            </ul>
            <ul className="navbar-nav">
              {auth && auth.user ? (
                <>
                  <li className="nav-item dropdown">
                    <a className="nav-link dropdown-toggle" href="#" id="navbarDropdown" role="button" data-bs-toggle="dropdown">
                      <i className="fas fa-user-circle me-1"></i> 
                      {auth.user.email}
                      {auth.unread_count > 0 && 
                        <span className="badge bg-danger ms-1">{auth.unread_count}</span>
                      }
                    </a>
                    <ul className="dropdown-menu dropdown-menu-end">
                      <li><Link className="dropdown-item" href={`/profile/${auth.user.id}`}>My Profile</Link></li>
                      <li><Link className="dropdown-item" href="/profile/edit">Edit Profile</Link></li>
                      <li><Link className="dropdown-item" href="/messages">Messages</Link></li>
                      <li><hr className="dropdown-divider" /></li>
                      <li><Link className="dropdown-item" href="/logout" method="post">Logout</Link></li>
                    </ul>
                  </li>
                </>
              ) : (
                <>
                  <li className="nav-item">
                    <Link className="nav-link" href="/login">Login</Link>
                  </li>
                  <li className="nav-item">
                    <Link className="nav-link" href="/register">Register</Link>
                  </li>
                </>
              )}
            </ul>
          </div>
        </div>
      </nav>

      {/* Flash Messages */}
      {flash && flash.length > 0 && (
        <div className="container mb-4">
          {flash.map((message, i) => (
            <div key={i} className={`alert alert-${message.type || 'info'} alert-dismissible fade show`} role="alert">
              {message.message}
              <button type="button" className="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
            </div>
          ))}
        </div>
      )}

      {/* Page Title */}
      <div className="container mb-4">
        <h1>{title}</h1>
      </div>
      
      {/* Main Content */}
      <main className="container flex-grow-1 mb-4">
        {children}
      </main>
      
      {/* Footer */}
      <footer className="footer bg-dark text-white py-4 mt-auto">
        <div className="container">
          <div className="row">
            <div className="col-md-6">
              <h5>Research Collaboration Platform</h5>
              <p>Connecting students, researchers, industry partners, and vendors.</p>
            </div>
            <div className="col-md-3">
              <h5>Quick Links</h5>
              <ul className="list-unstyled">
                <li><Link className="text-white" href="/documentation">Documentation</Link></li>
                <li><Link className="text-white" href="/terms">Terms of Service</Link></li>
                <li><Link className="text-white" href="/privacy">Privacy Policy</Link></li>
              </ul>
            </div>
            <div className="col-md-3">
              <h5>Contact</h5>
              <ul className="list-unstyled">
                <li><i className="fas fa-envelope me-2"></i> support@research-collab.com</li>
                <li><i className="fas fa-phone me-2"></i> +1 (123) 456-7890</li>
              </ul>
            </div>
          </div>
          <div className="row mt-3">
            <div className="col text-center">
              <p className="mb-0">&copy; {new Date().getFullYear()} Research Collaboration Platform. All rights reserved.</p>
            </div>
          </div>
        </div>
      </footer>
    </div>
  );
}