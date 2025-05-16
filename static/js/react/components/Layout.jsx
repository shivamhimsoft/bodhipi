import React from 'react';
import { Link } from '@inertiajs/inertia-react';

const Layout = ({ children, title = 'Research Collaboration Platform' }) => {
  return (
    <div className="d-flex flex-column min-vh-100">
      <header>
        <nav className="navbar navbar-expand-lg navbar-dark bg-dark">
          <div className="container">
            <Link className="navbar-brand" href="/">
              Research Platform
            </Link>
            <button
              className="navbar-toggler"
              type="button"
              data-bs-toggle="collapse"
              data-bs-target="#navbarNav"
              aria-controls="navbarNav"
              aria-expanded="false"
              aria-label="Toggle navigation"
            >
              <span className="navbar-toggler-icon"></span>
            </button>
            <div className="collapse navbar-collapse" id="navbarNav">
              <ul className="navbar-nav me-auto">
                <li className="nav-item">
                  <Link className="nav-link" href="/opportunities">
                    Opportunities
                  </Link>
                </li>
                <li className="nav-item">
                  <Link className="nav-link" href="/documentation">
                    Documentation
                  </Link>
                </li>
                <li className="nav-item">
                  <Link className="nav-link" href="/search">
                    Search
                  </Link>
                </li>
              </ul>
              <ul className="navbar-nav">
                <li className="nav-item">
                  <Link className="nav-link" href="/login">
                    Login
                  </Link>
                </li>
                <li className="nav-item">
                  <Link className="nav-link" href="/register">
                    Register
                  </Link>
                </li>
              </ul>
            </div>
          </div>
        </nav>
      </header>

      <main className="flex-grow-1 py-4">
        <div className="container">
          <h1 className="mb-4">{title}</h1>
          {children}
        </div>
      </main>

      <footer className="bg-dark text-light py-4 mt-auto">
        <div className="container">
          <div className="row">
            <div className="col-md-6">
              <h5>Research Collaboration Platform</h5>
              <p>Connecting researchers, students, and industry partners.</p>
            </div>
            <div className="col-md-3">
              <h6>Resources</h6>
              <ul className="list-unstyled">
                <li><Link className="text-light" href="/documentation">Documentation</Link></li>
                <li><Link className="text-light" href="/search">Search</Link></li>
              </ul>
            </div>
            <div className="col-md-3">
              <h6>Legal</h6>
              <ul className="list-unstyled">
                <li><Link className="text-light" href="/terms">Terms of Service</Link></li>
                <li><Link className="text-light" href="/privacy">Privacy Policy</Link></li>
              </ul>
            </div>
          </div>
          <hr className="mt-3 mb-3" />
          <div className="text-center">
            <p className="mb-0">&copy; {new Date().getFullYear()} Research Collaboration Platform. All rights reserved.</p>
          </div>
        </div>
      </footer>
    </div>
  );
};

export default Layout;