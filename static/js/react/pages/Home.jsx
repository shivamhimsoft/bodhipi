import React from 'react';
import { Link } from '@inertiajs/inertia-react';
import Layout from '../components/Layout';

const Home = ({ opportunities = [], profiles = [], stats = {}, title = 'Research Collaboration Platform' }) => {
  // Ensure stats has default values to prevent errors
  const safeStats = {
    users: stats?.users || 0,
    labs: stats?.labs || 0,
    opportunities: stats?.opportunities || 0,
    collaborations: stats?.collaborations || 0,
    ...stats
  };
  
  return (
    <Layout title={title}>
      {/* Hero section */}
      <section className="hero-section text-center mb-5">
        <div className="container py-5">
          <h2 className="display-4 fw-bold mb-4">Connecting Research Communities</h2>
          <p className="lead mb-4">
            Find research opportunities, connect with peers, and collaborate on groundbreaking projects.
          </p>
          <div className="d-grid gap-2 d-sm-flex justify-content-sm-center">
            <Link href="/register" className="btn btn-primary btn-lg px-4 gap-3">
              Join Today
            </Link>
            <Link href="/documentation" className="btn btn-outline-secondary btn-lg px-4">
              Learn More
            </Link>
          </div>
        </div>
      </section>

      {/* Platform stats */}
      <section className="mb-5">
        <div className="row text-center">
          <div className="col-md-3">
            <div className="card bg-dark border-primary mb-3">
              <div className="card-body">
                <h2 className="display-6 fw-bold text-primary">{safeStats.users}</h2>
                <p className="card-text">Users</p>
              </div>
            </div>
          </div>
          <div className="col-md-3">
            <div className="card bg-dark border-success mb-3">
              <div className="card-body">
                <h2 className="display-6 fw-bold text-success">{safeStats.labs}</h2>
                <p className="card-text">Research Labs</p>
              </div>
            </div>
          </div>
          <div className="col-md-3">
            <div className="card bg-dark border-info mb-3">
              <div className="card-body">
                <h2 className="display-6 fw-bold text-info">{safeStats.opportunities}</h2>
                <p className="card-text">Opportunities</p>
              </div>
            </div>
          </div>
          <div className="col-md-3">
            <div className="card bg-dark border-warning mb-3">
              <div className="card-body">
                <h2 className="display-6 fw-bold text-warning">{safeStats.collaborations}</h2>
                <p className="card-text">Collaborations</p>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* Latest opportunities */}
      <section className="mb-5">
        <h3 className="mb-4 border-bottom pb-2">Latest Opportunities</h3>
        <div className="row">
          {opportunities && opportunities.length > 0 ? (
            opportunities.map((opportunity) => (
              <div key={opportunity.id} className="col-md-4 mb-4">
                <div className="card h-100 opportunity-card">
                  <div className="card-header">
                    <span className="badge bg-primary me-2">{opportunity.type}</span>
                    <span className="badge bg-secondary">{opportunity.domain}</span>
                  </div>
                  <div className="card-body">
                    <h5 className="card-title">{opportunity.title}</h5>
                    <p className="card-text text-truncate">{opportunity.description}</p>
                    <div className="d-flex justify-content-between align-items-center mt-3">
                      <small className="text-muted">Location: {opportunity.location}</small>
                      <small className="text-muted">
                        Deadline: {new Date(opportunity.deadline).toLocaleDateString()}
                      </small>
                    </div>
                  </div>
                  <div className="card-footer bg-transparent">
                    <InertiaLink
                      href={`/opportunities/${opportunity.id}`}
                      className="btn btn-sm btn-outline-primary"
                    >
                      View Details
                    </InertiaLink>
                  </div>
                </div>
              </div>
            ))
          ) : (
            <div className="col-12">
              <div className="alert alert-info">No opportunities available at the moment.</div>
            </div>
          )}
        </div>
        <div className="text-center mt-3">
          <InertiaLink href="/opportunities" className="btn btn-outline-primary">
            Browse All Opportunities
          </InertiaLink>
        </div>
      </section>

      {/* Featured profiles */}
      <section className="mb-5">
        <h3 className="mb-4 border-bottom pb-2">Featured Profiles</h3>
        <div className="row">
          {profiles && profiles.length > 0 ? (
            profiles.map((profile) => (
              <div key={profile.id} className="col-md-3 mb-4">
                <div className="card h-100 profile-card">
                  <div className="card-body text-center">
                    <div className="mb-3">
                      <span className="badge bg-info mb-2">{profile.user_type}</span>
                      <h5 className="card-title mb-0">{profile.name || 'Unnamed Profile'}</h5>
                      <p className="text-muted small">{profile.affiliation || 'No affiliation'}</p>
                    </div>
                    <div className="progress mb-3" style={{ height: '5px' }}>
                      <div
                        className="progress-bar bg-success"
                        role="progressbar"
                        style={{ width: `${profile.completeness || 0}%` }}
                        aria-valuenow={profile.completeness || 0}
                        aria-valuemin="0"
                        aria-valuemax="100"
                      ></div>
                    </div>
                    <p className="small mb-0">
                      Profile Completion: {profile.completeness || 0}%
                    </p>
                  </div>
                  <div className="card-footer bg-transparent">
                    <InertiaLink
                      href={`/profile/${profile.user_id}`}
                      className="btn btn-sm btn-outline-info w-100"
                    >
                      View Profile
                    </InertiaLink>
                  </div>
                </div>
              </div>
            ))
          ) : (
            <div className="col-12">
              <div className="alert alert-info">No featured profiles available.</div>
            </div>
          )}
        </div>
      </section>

      {/* Platform features */}
      <section className="mb-5">
        <h3 className="mb-4 border-bottom pb-2">Platform Features</h3>
        <div className="row g-4">
          <div className="col-md-4">
            <div className="d-flex align-items-start">
              <div className="flex-shrink-0 me-3">
                <div className="icon-square bg-primary text-white p-2 rounded">
                  <i className="bi bi-search"></i>
                </div>
              </div>
              <div>
                <h4>Find Opportunities</h4>
                <p>
                  Discover research positions, internships, and collaborations across various domains and institutions.
                </p>
              </div>
            </div>
          </div>
          <div className="col-md-4">
            <div className="d-flex align-items-start">
              <div className="flex-shrink-0 me-3">
                <div className="icon-square bg-success text-white p-2 rounded">
                  <i className="bi bi-people"></i>
                </div>
              </div>
              <div>
                <h4>Connect with Researchers</h4>
                <p>
                  Build your network with principal investigators, fellow students, and industry partners.
                </p>
              </div>
            </div>
          </div>
          <div className="col-md-4">
            <div className="d-flex align-items-start">
              <div className="flex-shrink-0 me-3">
                <div className="icon-square bg-warning text-white p-2 rounded">
                  <i className="bi bi-chat"></i>
                </div>
              </div>
              <div>
                <h4>Direct Messaging</h4>
                <p>
                  Communicate directly with potential collaborators through our secure messaging system.
                </p>
              </div>
            </div>
          </div>
        </div>
      </section>
    </Layout>
  );
};

export default Home;