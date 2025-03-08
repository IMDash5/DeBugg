import React from 'react';
import '../styles/Footer.css';

const Footer = () => {
  return (
    <div className="footer">
      <p>&#169; {new Date().getFullYear()} <strong>DeBugg<sup>TM</sup></strong>. Все права защищены. Использование материалов только с разрешения владельцев.</p>
    </div>
  );
};

export default Footer;
