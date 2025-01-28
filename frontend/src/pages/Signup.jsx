import React, { useState, useEffect } from "react";
import "../stylez/Signup.css";
import Select from "react-select";
import { Link, useNavigate } from "react-router-dom";

function SignUp() {
  const [username, setName] = useState("");
  const [dob, setDOB] = useState("");
  const [location, setLoc] = useState(null); // Should hold the selected option object
  const [countries, setCountries] = useState([]); // Correct initialization for an array of options
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [prof, setProf] = useState(null); // Use null for file objects
  const url = "http://127.0.0.1:8000/signup/";
  const navigate = useNavigate();

  const getImage = (event) => {
    setProf(event.target.files[0]);
  };

  useEffect(() => {
    // Fetch country data once on component mount
    fetch(
      "https://valid.layercode.workers.dev/list/countries?format=select&flags=true&value=code"
    )
      .then((response) => response.json())
      .then((data) => {
        const formattedCountries = data.countries.map((country) => ({
          value: country.value,
          label: country.label,
        }));
        setCountries(formattedCountries); // Set properly formatted options
      })
      .catch((error) => alert("Failed to fetch countries: " + error.message));
  }, []); // Dependency array ensures this runs only once

  async function sign_up(event) {
    event.preventDefault();

    if (!prof) {
      alert("Please upload an image");
      return;
    }

    const formData = new FormData();
    formData.append("profile", prof);
    formData.append("name", username);
    formData.append("dob", dob);
    formData.append("email", email);
    formData.append("password", password);
    formData.append("location", location?.value);

    try {
      const resp = await fetch(url, {
        method: "POST",
        body: formData,
      });
      if (resp.ok) {
        const data = await resp.json();
        console.log(data);
        sessionStorage.setItem("token", data.token);
        sessionStorage.setItem("user", data.user);
        navigate("/home");
        alert("Sign-up successful!");
      } else {
        console.error("Error signing up:", resp.status);
        alert("Error signing up");
      }
    } catch (error) {
      console.error("Sign-up error:", error);
      alert("An error occurred during sign-up");
    }
  }

  return (
    <div className="sign_bod">
    <div className="background">
      <div className="form-container">
        <h1>Connectify</h1>
        <h3>Create Your Account</h3>
        <form onSubmit={sign_up}>
          <div className="input-group">
            <label htmlFor="username">User name</label>
            <input
              type="text"
              id="username"
              placeholder="John"
              value={username}
              onChange={(e) => setName(e.target.value)}
            />
          </div>
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
          <div className="input-group">
            <label htmlFor="dob">Date of birth</label>
            <input
              type="date"
              id="dob"
              placeholder="DOB"
              value={dob}
              onChange={(e) => setDOB(e.target.value)}
            />
          </div>
          <div className="input-group">
            <label htmlFor="profile">Profile picture</label>
            <input type="file" id="profile" onChange={getImage}></input>
          </div>
          <div className="input-group">
            <label htmlFor="location">Location</label>
            <Select
              id="location"
              options={countries}
              value={location}
              onChange={(selectedOption) => setLoc(selectedOption)}
              placeholder="Select your country"
            />
          </div>
          <button type="submit" className="btn">
            Sign Up
          </button>
        </form>
        <p className="footer-text">
          I'm already a member! <Link to="/login">Sign In</Link>
        </p>
      </div>
    </div>
    </div>
  );
}

export default SignUp;
