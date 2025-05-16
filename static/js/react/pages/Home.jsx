import React from 'react';
import Layout from '../components/Layout';
import { Link } from '@inertiajs/inertia-react';

export default function Home({ opportunities, profiles, stats }) {
  return (
    <Layout title="Welcome to Research Collaboration Platform">
      {/* Hero Section */}
      <section className="py-5 text-center bg-dark text-white rounded mb-5">
        <div className="container">
          <h1 className="display-4 fw-bold">Research Collaboration Platform</h1>
          <p className="lead mb-4">
            Connecting students, researchers, industry partners, and vendors for impactful collaborations
          </p>
          <div className="d-grid gap-2 d-sm-flex justify-content-sm-center">
            <Link href="/register" className="btn btn-primary btn-lg px-4 gap-3">
              Join Now
            </Link>
            <Link href="/opportunities" className="btn btn-outline-light btn-lg px-4">
              Browse Opportunities
            </Link>
          </div>
        </div>
      </section>

      {/* Stats Section */}
      <section className="mb-5">
        <div className="container">
          <div className="row text-center">
            <div className="col-md-3">
              <div className="card h-100 bg-primary text-white">
                <div className="card-body">
                  <i className="fas fa-users fa-3x mb-3"></i>
                  <h3 className="card-title">{stats.users}</h3>
                  <p className="card-text">Active Users</p>
                </div>
              </div>
            </div>
            <div className="col-md-3">
              <div className="card h-100 bg-info text-white">
                <div className="card-body">
                  <i className="fas fa-flask fa-3x mb-3"></i>
                  <h3 className="card-title">{stats.labs}</h3>
                  <p className="card-text">Research Labs</p>
                </div>
              </div>
            </div>
            <div className="col-md-3">
              <div className="card h-100 bg-success text-white">
                <div className="card-body">
                  <i className="fas fa-briefcase fa-3x mb-3"></i>
                  <h3 className="card-title">{stats.opportunities}</h3>
                  <p className="card-text">Opportunities</p>
                </div>
              </div>
            </div>
            <div className="col-md-3">
              <div className="card h-100 bg-warning text-dark">
                <div className="card-body">
                  <i className="fas fa-handshake fa-3x mb-3"></i>
                  <h3 className="card-title">{stats.collaborations}</h3>
                  <p className="card-text">Collaborations</p>
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* Featured Opportunities */}
      <section className="mb-5">
        <div className="container">
          <h2 className="mb-4">Featured Opportunities</h2>
          <div className="row">
            {opportunities && opportunities.length > 0 ? (
              opportunities.map((opportunity) => (
                <div key={opportunity.id} className="col-md-4 mb-4">
                  <div className="card h-100 shadow-sm">
                    <div className="card-header bg-dark text-white">
                      <span className="badge bg-primary me-2">{opportunity.type}</span>
                    </div>
                    <div className="card-body">
                      <h5 className="card-title">{opportunity.title}</h5>
                      <p className="card-text">
                        {opportunity.description?.substring(0, 150)}
                        {opportunity.description?.length > 150 ? '...' : ''}
                      </p>
                      <div className="d-flex justify-content-between align-items-center">
                        <small className="text-muted">
                          <i className="fas fa-map-marker-alt me-1"></i>
                          {opportunity.location}
                        </small>
                        <small className="text-muted">
                          <i className="fas fa-clock me-1"></i>
                          {opportunity.duration}
                        </small>
                      </div>
                    </div>
                    <div className="card-footer bg-white border-0">
                      <Link href={`/opportunity/${opportunity.id}`} className="btn btn-sm btn-outline-primary">
                        View Details
                      </Link>
                    </div>
                  </div>
                </div>
              ))
            ) : (
              <div className="col">
                <div className="alert alert-info" role="alert">
                  No opportunities available at the moment.
                </div>
              </div>
            )}
          </div>
          <div className="text-center mt-3">
            <Link href="/opportunities" className="btn btn-primary">
              View All Opportunities
            </Link>
          </div>
        </div>
      </section>

      {/* Featured Profiles */}
      <section className="mb-5">
        <div className="container">
          <h2 className="mb-4">Featured Profiles</h2>
          <div className="row">
            {profiles && profiles.length > 0 ? (
              profiles.map((profile) => (
                <div key={profile.id} className="col-md-3 mb-4">
                  <div className="card h-100 shadow-sm">
                    <div className="card-header bg-dark text-white">
                      <span className="badge bg-info me-2">{profile.profile_type}</span>
                    </div>
                    <div className="card-body">
                      <h5 className="card-title">{profile.name || 'Unnamed Profile'}</h5>
                      {profile.affiliation && (
                        <p className="card-text">
                          <i className="fas fa-university me-1"></i> {profile.affiliation}
                        </p>
                      )}
                      {profile.department && (
                        <p className="card-text">
                          <i className="fas fa-building me-1"></i> {profile.department}
                        </p>
                      )}
                      {profile.research_interests && (
                        <p className="card-text">
                          <small className="text-muted">
                            {profile.research_interests.substring(0, 100)}
                            {profile.research_interests.length > 100 ? '...' : ''}
                          </small>
                        </p>
                      )}
                      {profile.current_focus && (
                        <p className="card-text">
                          <small className="text-muted">
                            {profile.current_focus.substring(0, 100)}
                            {profile.current_focus.length > 100 ? '...' : ''}
                          </small>
                        </p>
                      )}
                      <div className="progress mt-2" style={{ height: '5px' }}>
                        <div
                          className="progress-bar bg-success"
                          role="progressbar"
                          style={{ width: `${profile.profile_completeness}%` }}
                          aria-valuenow={profile.profile_completeness}
                          aria-valuemin="0"
                          aria-valuemax="100"
                        ></div>
                      </div>
                      <small className="text-muted">Profile: {profile.profile_completeness}% complete</small>
                    </div>
                    <div className="card-footer bg-white border-0">
                      <Link href={`/profile/${profile.user_id}`} className="btn btn-sm btn-outline-info">
                        View Profile
                      </Link>
                    </div>
                  </div>
                </div>
              ))
            ) : (
              <div className="col">
                <div className="alert alert-info" role="alert">
                  No profiles available at the moment.
                </div>
              </div>
            )}
          </div>
        </div>
      </section>

      {/* How It Works */}
      <section className="mb-5 bg-light p-4 rounded">
        <div className="container">
          <h2 className="text-center mb-4">How It Works</h2>
          <div className="row">
            <div className="col-md-4 text-center mb-3">
              <div className="p-3">
                <div className="mb-3">
                  <span className="fa-stack fa-2x">
                    <i className="fas fa-circle fa-stack-2x text-primary"></i>
                    <i className="fas fa-user-plus fa-stack-1x fa-inverse"></i>
                  </span>
                </div>
                <h4>Create Your Profile</h4>
                <p>Register and create a detailed profile based on your role in the research ecosystem.</p>
              </div>
            </div>
            <div className="col-md-4 text-center mb-3">
              <div className="p-3">
                <div className="mb-3">
                  <span className="fa-stack fa-2x">
                    <i className="fas fa-circle fa-stack-2x text-primary"></i>
                    <i className="fas fa-search fa-stack-1x fa-inverse"></i>
                  </span>
                </div>
                <h4>Find Opportunities</h4>
                <p>Browse or post research opportunities, from internships to full collaborations.</p>
              </div>
            </div>
            <div className="col-md-4 text-center mb-3">
              <div className="p-3">
                <div className="mb-3">
                  <span className="fa-stack fa-2x">
                    <i className="fas fa-circle fa-stack-2x text-primary"></i>
                    <i className="fas fa-comments fa-stack-1x fa-inverse"></i>
                  </span>
                </div>
                <h4>Connect & Collaborate</h4>
                <p>Communicate with potential partners and build impactful research relationships.</p>
              </div>
            </div>
          </div>
          <div className="text-center mt-3">
            <Link href="/documentation" className="btn btn-primary">
              Learn More
            </Link>
          </div>
        </div>
      </section>
    </Layout>
  );
}