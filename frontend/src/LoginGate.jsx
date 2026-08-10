import React, { useState, useEffect } from 'react';

export default function LoginGate({ children }) {
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');

  useEffect(() => {
    if (localStorage.getItem('hamsterflix_auth') === 'true') {
      setIsAuthenticated(true);
    }
  }, []);

  const handleLogin = (e) => {
    e.preventDefault();
    if (email.toLowerCase().trim() === 'youriykaplan@gmail.com' && password === 'hasmterpower') {
      localStorage.setItem('hamsterflix_auth', 'true');
      setIsAuthenticated(true);
    } else {
      setError('Incorrect email or password. Please try again.');
    }
  };

  if (isAuthenticated) {
    return children;
  }

  return (
    <div className="min-h-screen bg-black flex flex-col items-center justify-center font-sans text-white relative">
      {/* Subtle background glow/overlay */}
      <div className="absolute inset-0 bg-[url('https://images.unsplash.com/photo-1574267432553-4b4628081524?q=80&w=2000&auto=format&fit=crop')] bg-cover bg-center opacity-20"></div>
      <div className="absolute inset-0 bg-gradient-to-t from-black via-black/60 to-black/80"></div>
      
      <div className="z-10 w-full max-w-md bg-black/75 p-12 rounded-md shadow-2xl border border-gray-800">
        <h1 className="text-4xl font-bold text-red-600 mb-8 tracking-wider text-center">HAMSTERFLIX</h1>
        
        <h2 className="text-3xl font-bold mb-6">Sign In</h2>
        
        {error && (
          <div className="bg-orange-500 text-white text-sm p-3 rounded mb-4">
            {error}
          </div>
        )}

        <form onSubmit={handleLogin} className="flex flex-col gap-4">
          <input
            type="email"
            placeholder="Email address"
            className="p-3 bg-gray-800 rounded focus:outline-none focus:ring-2 focus:ring-gray-500 text-white w-full"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            required
          />
          
          <input
            type="password"
            placeholder="Password"
            className="p-3 bg-gray-800 rounded focus:outline-none focus:ring-2 focus:ring-gray-500 text-white w-full"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            required
          />
          
          <button
            type="submit"
            className="bg-red-600 hover:bg-red-700 text-white font-bold py-3 px-4 rounded mt-4 transition-colors"
          >
            Sign In
          </button>
        </form>
        
        <div className="mt-10 text-gray-400 text-sm">
          <p>Protected by Neuralon Secure Gateway.</p>
        </div>
      </div>
    </div>
  );
}
