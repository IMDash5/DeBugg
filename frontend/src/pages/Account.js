import React from 'react';
import '../styles/Account.css';

export default function Account() {
  return (
    <div className="account-container">
      <div className="account-sidebar">
        <img
          src="/images/account_logo.png"
          alt="avatar"
          className="account-avatar"
        />
        <h2 className="account-name">Иван Иванов</h2>
        <p className="account-role">Common account</p>
        {/* Можно указывать тип подписки */}
      </div>

      <div className="account-info">
        <h3 className="account-section-title">Information</h3>
        <div className="account-info-row">
          <div>
            <p className="account-label">Email</p>
            <p>info@example.com</p>
          </div>
          <div>
            <p className="account-label">Phone</p>
            <p>+7(910)777-44-55</p>

          </div>
        </div>


        <div className="account-info-row">
          <div>
            <p className="account-label">Recent</p>
            <p>Lorem ipsum</p>
          </div>
          <div>
            <p className="account-label">Most Viewed</p>
            <p>Dolor sit amet</p>
          </div>
        </div>
      </div>
    </div>
  );
}
