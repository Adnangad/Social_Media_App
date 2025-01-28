import React, { useState, useEffect } from "react";
import "../stylez/Signup.css";
import Select from "react-select";
import { Link, useNavigate } from "react-router-dom";

function Login() {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const url = "http://127.0.0.1:8000/login";
  const navigate = useNavigate();
  async function login(event) {
    event.preventDefault();

    const dat = {"email": email, "password": password};
    console.log(dat)
    try {
      const resp = await fetch(url, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(dat),
      });
      if (resp.status === 200) {
        const data = await resp.json();
        console.log(data);
        sessionStorage.setItem("token", data.token);
        sessionStorage.setItem("user", data.user);
        navigate("/home");
        alert("Sign-up successful!");
      } else {
        console.error("Error signing in:", resp.status);
        alert("Error signing in");
      }
    } catch (error) {
      console.error("Sign-in error:", error);
      alert("An error occurred during sign-in");
    }
  }

  return (
    <div className="sign_bod">
    <div className="background">
      <div className="form-container">
        <h1>Connectify</h1>
        <h3>Sign In</h3>
        <form onSubmit={login}>
          <div className="input-group">
            <label htmlFor="email">Email Address</label>
            <input
              type="email"
              id="email"
              placeholder="johndoe@gmail.com"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
            />
          </div>
          <div className="input-group">
            <label htmlFor="password">Password</label>
            <input
              type="password"
              id="password"
              placeholder="Password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
            />
          </div>
          <button type="submit" className="btn">
            Sign in
          </button>
        </form>
        <p className="footer-text">
          New to the system! <Link to="/">Sign up</Link>
        </p>
      </div>
    </div>
    </div>
  );
}

export default Login;
