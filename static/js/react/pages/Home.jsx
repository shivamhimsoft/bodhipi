import React from 'react';
import Layout from '../components/Layout';

const Home = ({ auth, opportunities, stats }) => {
  return (
    <Layout auth={auth}>
      {/* Hero Section */}
      <div className="py-5 mb-5 bg-dark text-white rounded-3">
        <div className="container">
          <div className="row align-items-center">
            <div className="col-lg-6">
              <h1 className="display-4 fw-bold mb-3">Research Collaboration Platform</h1>
              <p className="lead mb-4">
                Connecting students, researchers, industry partners, and vendors 
                in the research ecosystem to foster innovation and collaboration.
              </p>
              <div className="d-grid gap-2 d-md-flex justify-content-md-start">
                <a href="/opportunities" className="btn btn-primary btn-lg px-4 me-md-2">
                  Browse Opportunities
                </a>
                {!auth && (
                  <a href="/register" className="btn btn-outline-light btn-lg px-4">
                    Join Platform
                  </a>
                )}
              </div>
            </div>
            <div className="col-lg-6 d-none d-lg-block">
              <div className="text-center">
                <i className="fas fa-flask fa-10x text-primary opacity-75"></i>
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* Stats Section */}
      <div className="row mb-5">
        <div className="col-md-3 mb-4">
          <div className="card h-100">
            <div className="card-body text-center">
              <div className="display-4 mb-2 text-primary">
                <i className="fas fa-users"></i>
              </div>
              <h3 className="display-5 fw-bold">{stats?.users || 0}</h3>
              <p className="text-muted">Platform Users</p>
            </div>
          </div>
        </div>
        <div className="col-md-3 mb-4">
          <div className="card h-100">
            <div className="card-body text-center">
              <div className="display-4 mb-2 text-info">
                <i className="fas fa-flask"></i>
              </div>
              <h3 className="display-5 fw-bold">{stats?.labs || 0}</h3>
              <p className="text-muted">Research Labs</p>
            </div>
          </div>
        </div>
        <div className="col-md-3 mb-4">
          <div className="card h-100">
            <div className="card-body text-center">
              <div className="display-4 mb-2 text-success">
                <i className="fas fa-briefcase"></i>
              </div>
              <h3 className="display-5 fw-bold">{stats?.opportunities || 0}</h3>
              <p className="text-muted">Opportunities</p>
            </div>
          </div>
        </div>
        <div className="col-md-3 mb-4">
          <div className="card h-100">
            <div className="card-body text-center">
              <div className="display-4 mb-2 text-warning">
                <i className="fas fa-handshake"></i>
              </div>
              <h3 className="display-5 fw-bold">{stats?.collaborations || 0}</h3>
              <p className="text-muted">Collaborations</p>
            </div>
          </div>
        </div>
      </div>

      {/* Recent Opportunities */}
      <h2 className="mb-4">Recent Opportunities</h2>
      <div className="row">
        {opportunities && opportunities.length > 0 ? (
          opportunities.map(opportunity => (
            <div className="col-md-6 col-lg-4 mb-4" key={opportunity.id}>
              <div className="card h-100 opportunity-card">
                <div className="card-body">
                  <div className="d-flex justify-content-between align-items-start mb-2">
                    <span 
                      className={`badge ${opportunity.type === 'PhD' ? 'badge-phd' : 
                                         opportunity.type === 'Internship' ? 'badge-internship' : 
                                         opportunity.type === 'Job' ? 'badge-job' : 
                                         opportunity.type === 'PostDoc' ? 'badge-postdoc' : 
                                         'badge-project'}`}
                    >
                      {opportunity.type}
                    </span>
                    <small className="text-muted">Posted: {new Date(opportunity.created_at).toLocaleDateString()}</small>
                  </div>
                  <h5 className="card-title">{opportunity.title}</h5>
                  <p className="card-text">{opportunity.description.substring(0, 100)}...</p>
                  <div className="d-flex justify-content-between align-items-center">
                    <span><i className="fas fa-map-marker-alt me-1"></i> {opportunity.location}</span>
                    <span><i className="fas fa-calendar-alt me-1"></i> {opportunity.duration}</span>
                  </div>
                </div>
                <div className="card-footer bg-transparent d-grid">
                  <a href={`/opportunity/${opportunity.id}`} className="btn btn-outline-primary">
                    View Details
                  </a>
                </div>
              </div>
            </div>
          ))
        ) : (
          <div className="col-12">
            <div className="alert alert-info">
              No opportunities available at the moment.
            </div>
          </div>
        )}
      </div>
      {opportunities && opportunities.length > 0 && (
        <div className="text-center mt-4">
          <a href="/opportunities" className="btn btn-primary">
            View All Opportunities
          </a>
        </div>
      )}

      {/* Features Section */}
      <h2 className="mt-5 mb-4">Platform Features</h2>
      <div className="row">
        <div className="col-md-4 mb-4">
          <div className="card h-100">
            <div className="card-body text-center">
              <div className="display-5 mb-3 text-primary">
                <i className="fas fa-user-graduate"></i>
              </div>
              <h4>For Students</h4>
              <ul className="list-unstyled text-start mt-3">
                <li className="mb-2"><i className="fas fa-check-circle text-success me-2"></i> Find research opportunities</li>
                <li className="mb-2"><i className="fas fa-check-circle text-success me-2"></i> Connect with labs</li>
                <li className="mb-2"><i className="fas fa-check-circle text-success me-2"></i> Showcase your skills</li>
              </ul>
            </div>
          </div>
        </div>
        <div className="col-md-4 mb-4">
          <div className="card h-100">
            <div className="card-body text-center">
              <div className="display-5 mb-3 text-info">
                <i className="fas fa-microscope"></i>
              </div>
              <h4>For Researchers</h4>
              <ul className="list-unstyled text-start mt-3">
                <li className="mb-2"><i className="fas fa-check-circle text-success me-2"></i> Post research positions</li>
                <li className="mb-2"><i className="fas fa-check-circle text-success me-2"></i> Find talented students</li>
                <li className="mb-2"><i className="fas fa-check-circle text-success me-2"></i> Industry collaborations</li>
              </ul>
            </div>
          </div>
        </div>
        <div className="col-md-4 mb-4">
          <div className="card h-100">
            <div className="card-body text-center">
              <div className="display-5 mb-3 text-warning">
                <i className="fas fa-building"></i>
              </div>
              <h4>For Industry Partners</h4>
              <ul className="list-unstyled text-start mt-3">
                <li className="mb-2"><i className="fas fa-check-circle text-success me-2"></i> Academic partnerships</li>
                <li className="mb-2"><i className="fas fa-check-circle text-success me-2"></i> Research collaborations</li>
                <li className="mb-2"><i className="fas fa-check-circle text-success me-2"></i> Recruit researchers</li>
              </ul>
            </div>
          </div>
        </div>
      </div>

      {/* Call to Action */}
      <div className="mt-5 p-5 bg-primary text-white rounded-3">
        <div className="container">
          <div className="row align-items-center">
            <div className="col-lg-8">
              <h2 className="mb-3">Ready to join the research community?</h2>
              <p className="lead mb-0">
                Create your profile today and start connecting with research opportunities 
                and collaborators from around the world.
              </p>
            </div>
            <div className="col-lg-4 text-lg-end mt-3 mt-lg-0">
              {auth ? (
                <a href="/opportunities" className="btn btn-light btn-lg">Explore Opportunities</a>
              ) : (
                <a href="/register" className="btn btn-light btn-lg">Join Now</a>
              )}
            </div>
          </div>
        </div>
      </div>
    </Layout>
  );
};

export default Home;