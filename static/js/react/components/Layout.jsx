import React from 'react';
import { InertiaLink } from '@inertiajs/inertia-react';

const Layout = ({ children, auth }) => {
  return (
    <div className="min-vh-100 d-flex flex-column">
      <header>
        <nav className="navbar navbar-expand-lg navbar-dark bg-dark">
          <div className="container">
            <InertiaLink href="/" className="navbar-brand">
              <i className="fas fa-flask me-2"></i>Research Collaboration
            </InertiaLink>
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
                  <InertiaLink href="/" className="nav-link">Home</InertiaLink>
                </li>
                <li className="nav-item">
                  <InertiaLink href="/opportunities" className="nav-link">Opportunities</InertiaLink>
                </li>
                <li className="nav-item dropdown">
                  <a 
                    className="nav-link dropdown-toggle" 
                    href="#" 
                    id="navbarDropdown" 
                    role="button" 
                    data-bs-toggle="dropdown" 
                    aria-expanded="false"
                  >
                    Explore
                  </a>
                  <ul className="dropdown-menu" aria-labelledby="navbarDropdown">
                    <li>
                      <InertiaLink href="/search?category=profiles" className="dropdown-item">
                        Research Labs
                      </InertiaLink>
                    </li>
                    <li>
                      <InertiaLink href="/search?category=profiles" className="dropdown-item">
                        Industry Partners
                      </InertiaLink>
                    </li>
                    <li>
                      <InertiaLink href="/search?category=profiles" className="dropdown-item">
                        Vendors
                      </InertiaLink>
                    </li>
                    <li><hr className="dropdown-divider" /></li>
                    <li>
                      <InertiaLink href="/search?category=opportunities" className="dropdown-item">
                        Research Positions
                      </InertiaLink>
                    </li>
                  </ul>
                </li>
                {auth && auth.user && (auth.user.user_type === 'PI' || auth.user.user_type === 'Industry') && (
                  <li className="nav-item">
                    <InertiaLink href="/create_opportunity" className="nav-link">
                      Post Opportunity
                    </InertiaLink>
                  </li>
                )}
                {auth && auth.user && auth.user.user_type === 'Admin' && (
                  <li className="nav-item">
                    <InertiaLink href="/admin/dashboard" className="nav-link">
                      Admin Dashboard
                    </InertiaLink>
                  </li>
                )}
              </ul>
              
              <form className="d-flex me-4" action="/search" method="get">
                <input 
                  className="form-control me-2" 
                  type="search" 
                  placeholder="Search" 
                  aria-label="Search" 
                  name="query" 
                  required 
                />
                <input type="hidden" name="category" value="all" />
                <button className="btn btn-outline-light" type="submit">
                  <i className="fas fa-search"></i>
                </button>
              </form>
              
              <ul className="navbar-nav">
                {auth && auth.user ? (
                  <>
                    <li className="nav-item">
                      <InertiaLink href="/messages" className="nav-link">
                        <i className="fas fa-envelope"></i>
                        {auth.unread_count > 0 && (
                          <span className="badge bg-danger">{auth.unread_count}</span>
                        )}
                      </InertiaLink>
                    </li>
                    <li className="nav-item dropdown">
                      <a 
                        className="nav-link dropdown-toggle" 
                        href="#" 
                        id="userDropdown" 
                        role="button" 
                        data-bs-toggle="dropdown" 
                        aria-expanded="false"
                      >
                        {auth.user.email}
                      </a>
                      <ul className="dropdown-menu dropdown-menu-end" aria-labelledby="userDropdown">
                        <li>
                          <InertiaLink 
                            href={`/profile/${auth.user.id}`} 
                            className="dropdown-item"
                          >
                            My Profile
                          </InertiaLink>
                        </li>
                        <li>
                          <InertiaLink href="/edit_profile" className="dropdown-item">
                            Edit Profile
                          </InertiaLink>
                        </li>
                        <li><hr className="dropdown-divider" /></li>
                        <li>
                          <InertiaLink 
                            href="/logout" 
                            method="post" 
                            as="button" 
                            className="dropdown-item"
                          >
                            Logout
                          </InertiaLink>
                        </li>
                      </ul>
                    </li>
                  </>
                ) : (
                  <>
                    <li className="nav-item">
                      <InertiaLink href="/login" className="nav-link">Login</InertiaLink>
                    </li>
                    <li className="nav-item">
                      <InertiaLink href="/register" className="nav-link">Register</InertiaLink>
                    </li>
                  </>
                )}
              </ul>
            </div>
          </div>
        </nav>
      </header>

      <main className="flex-grow-1 py-4">
        <div className="container">
          {children}
        </div>
      </main>

      <footer className="bg-dark text-light py-4 mt-5">
        <div className="container">
          <div className="row">
            <div className="col-md-4">
              <h5>Research Collaboration Platform</h5>
              <p>Connecting researchers, students, industry partners, and vendors to foster innovation and collaboration.</p>
            </div>
            <div className="col-md-4">
              <h5>Quick Links</h5>
              <ul className="list-unstyled">
                <li><InertiaLink href="/" className="text-decoration-none text-light">Home</InertiaLink></li>
                <li><InertiaLink href="/opportunities" className="text-decoration-none text-light">Opportunities</InertiaLink></li>
                <li><InertiaLink href="/documentation" className="text-decoration-none text-light">Documentation</InertiaLink></li>
                <li><a href="#" className="text-decoration-none text-light">Contact</a></li>
              </ul>
            </div>
            <div className="col-md-4">
              <h5>Connect With Us</h5>
              <div className="d-flex gap-3 fs-4">
                <a href="#" className="text-light"><i className="fab fa-twitter"></i></a>
                <a href="#" className="text-light"><i className="fab fa-facebook"></i></a>
                <a href="#" className="text-light"><i className="fab fa-linkedin"></i></a>
                <a href="#" className="text-light"><i className="fab fa-instagram"></i></a>
              </div>
            </div>
          </div>
          <hr />
          <div className="text-center">
            <p className="mb-0">&copy; {new Date().getFullYear()} Research Collaboration Platform. All rights reserved.</p>
          </div>
        </div>
      </footer>
    </div>
  );
};

export default Layout;