import React from 'react';
import { BrowserRouter as Router, Routes, Route, Link, useParams, useNavigate } from 'react-router-dom';
import { Search, Bell, Info, Play, ChevronDown, Plus, ArrowLeft, ChevronLeft, ChevronRight } from 'lucide-react';

const FEATURED_MOVIE = {
  title: "Hamster's Great Escape",
  description: "When the wheel stops turning, the real adventure begins. Follow one brave hamster's journey beyond the cage.",
  heroImage: "/posters/poster_1.png"
};

// const CATEGORIES = [
//   {
//     title: "Wheel Spinners (Trending)",
//     movies: [
//       { id: 27, title: "Hamster Dance", img: "/posters/poster_27.png" },
//       { id: 38, title: "Shadows in the Cage", img: "/posters/poster_38.png" },
//       { id: 25, title: "Squeaky Clean", img: "/posters/poster_25.png" },
//       { id: 5, title: "Cheek Pouches", img: "/posters/poster_5.png" },
//       { id: 35, title: "Laser Eyes", img: "/posters/poster_35.png" },
//       { id: 12, title: "Sleep All Day", img: "/posters/poster_12.png" },
//       { id: 16, title: "Cage Break", img: "/posters/poster_16.png" },
//       { id: 2, title: "The Maze Runner", img: "/posters/poster_2.png" },
//       { id: 21, title: "Beyond the Wheel", img: "/posters/poster_21.png" },
//       { id: 18, title: "The Burrow", img: "/posters/poster_18.png" },
//       { id: 41, title: "The Hand", img: "/posters/poster_41.png" },
//       { id: 15, title: "Fuzz Ball", img: "/posters/poster_15.png" },
//     ]
//   },
//   {
//     title: "Squeak-Inducing Thrills",
//     movies: [
//       { id: 38, title: "Shadows in the Cage", img: "/posters/poster_38.png" },
//       { id: 39, title: "Lost in the Tubes", img: "/posters/poster_39.png" },
//       { id: 40, title: "Midnight Squeak", img: "/posters/poster_40.png" },
//       { id: 41, title: "The Hand", img: "/posters/poster_41.png" },
//       { id: 37, title: "The Cat Next Door", img: "/posters/poster_37.png" },
//       { id: 15, title: "Fuzz Ball", img: "/posters/poster_15.png" },
//       { id: 21, title: "Beyond the Wheel", img: "/posters/poster_21.png" },
//       { id: 8, title: "Bite Sized", img: "/posters/poster_8.png" },
//       { id: 2, title: "The Maze Runner", img: "/posters/poster_2.png" },
//       { id: 19, title: "Life in the Tubes", img: "/posters/poster_19.png" },
//       { id: 36, title: "Planet Fluff", img: "/posters/poster_36.png" },
//       { id: 14, title: "Midnight Runner", img: "/posters/poster_14.png" },
//     ]
//   },
//   {
//     title: "Cheeky Comedies",
//     movies: [
//       { id: 27, title: "Hamster Dance", img: "/posters/poster_27.png" },
//       { id: 29, title: "Wheel Fail", img: "/posters/poster_29.png" },
//       { id: 25, title: "Squeaky Clean", img: "/posters/poster_25.png" },
//       { id: 26, title: "Drop the Seed", img: "/posters/poster_26.png" },
//       { id: 30, title: "Bite Me", img: "/posters/poster_30.png" },
//       { id: 28, title: "Stuck in the Tube", img: "/posters/poster_28.png" },
//       { id: 10, title: "The Great Cage", img: "/posters/poster_10.png" },
//       { id: 12, title: "Sleep All Day", img: "/posters/poster_12.png" },
//       { id: 39, title: "Lost in the Tubes", img: "/posters/poster_39.png" },
//       { id: 20, title: "Seed Gatherers", img: "/posters/poster_20.png" },
//       { id: 4, title: "Tube City", img: "/posters/poster_4.png" },
//       { id: 13, title: "The Nut Job", img: "/posters/poster_13.png" },
//     ]
//   },
//   {
//     title: "Cage-Free Sci-Fi",
//     movies: [
//       { id: 36, title: "Planet Fluff", img: "/posters/poster_36.png" },
//       { id: 33, title: "Alien Seeds", img: "/posters/poster_33.png" },
//       { id: 34, title: "Tube Portals", img: "/posters/poster_34.png" },
//       { id: 35, title: "Laser Eyes", img: "/posters/poster_35.png" },
//       { id: 32, title: "The Galactic Cage", img: "/posters/poster_32.png" },
//       { id: 31, title: "Space Hamster", img: "/posters/poster_31.png" },
//       { id: 6, title: "Wheel of Time", img: "/posters/poster_6.png" },
//       { id: 16, title: "Cage Break", img: "/posters/poster_16.png" },
//       { id: 23, title: "The Escape Artist", img: "/posters/poster_23.png" },
//       { id: 11, title: "Wood Shavings", img: "/posters/poster_11.png" },
//       { id: 18, title: "The Burrow", img: "/posters/poster_18.png" },
//       { id: 20, title: "Seed Gatherers", img: "/posters/poster_20.png" },
//     ]
//   },
//   {
//     title: "Critically Acclaimed Fluff",
//     movies: [
//       { id: 4, title: "Tube City", img: "/posters/poster_4.png" },
//       { id: 15, title: "Fuzz Ball", img: "/posters/poster_15.png" },
//       { id: 13, title: "The Nut Job", img: "/posters/poster_13.png" },
//       { id: 5, title: "Cheek Pouches", img: "/posters/poster_5.png" },
//       { id: 16, title: "Cage Break", img: "/posters/poster_16.png" },
//       { id: 17, title: "Squeak", img: "/posters/poster_17.png" },
//       { id: 2, title: "The Maze Runner", img: "/posters/poster_2.png" },
//       { id: 6, title: "Wheel of Time", img: "/posters/poster_6.png" },
//       { id: 18, title: "The Burrow", img: "/posters/poster_18.png" },
//       { id: 14, title: "Midnight Runner", img: "/posters/poster_14.png" },
//       { id: 1, title: "Sunflower Seeds", img: "/posters/poster_1.png" },
//       { id: 3, title: "Midnight Snack", img: "/posters/poster_3.png" },
//     ]
//   },
//   {
//     title: "Real Rodent Stories (Docs)",
//     movies: [
//       { id: 24, title: "Cheeks of Steel", img: "/posters/poster_24.png" },
//       { id: 23, title: "The Escape Artist", img: "/posters/poster_23.png" },
//       { id: 19, title: "Life in the Tubes", img: "/posters/poster_19.png" },
//       { id: 20, title: "Seed Gatherers", img: "/posters/poster_20.png" },
//       { id: 22, title: "Nocturnal Habits", img: "/posters/poster_22.png" },
//       { id: 21, title: "Beyond the Wheel", img: "/posters/poster_21.png" },
//       { id: 30, title: "Bite Me", img: "/posters/poster_30.png" },
//       { id: 28, title: "Stuck in the Tube", img: "/posters/poster_28.png" },
//       { id: 18, title: "The Burrow", img: "/posters/poster_18.png" },
//       { id: 7, title: "Furry Fury", img: "/posters/poster_7.png" },
//       { id: 26, title: "Drop the Seed", img: "/posters/poster_26.png" },
//       { id: 16, title: "Cage Break", img: "/posters/poster_16.png" },
//     ]
//   },
//   {
//     title: "High-Speed Pursuits",
//     movies: [
//       { id: 9, title: "Rodent Racer", img: "/posters/poster_9.png" },
//       { id: 10, title: "The Great Cage", img: "/posters/poster_10.png" },
//       { id: 7, title: "Furry Fury", img: "/posters/poster_7.png" },
//       { id: 12, title: "Sleep All Day", img: "/posters/poster_12.png" },
//       { id: 8, title: "Bite Sized", img: "/posters/poster_8.png" },
//       { id: 11, title: "Wood Shavings", img: "/posters/poster_11.png" },
//       { id: 33, title: "Alien Seeds", img: "/posters/poster_33.png" },
//       { id: 17, title: "Squeak", img: "/posters/poster_17.png" },
//       { id: 14, title: "Midnight Runner", img: "/posters/poster_14.png" },
//       { id: 31, title: "Space Hamster", img: "/posters/poster_31.png" },
//       { id: 18, title: "The Burrow", img: "/posters/poster_18.png" },
//       { id: 23, title: "The Escape Artist", img: "/posters/poster_23.png" },
//     ]
//   },
// ];

// const ALL_MOVIES = CATEGORIES.flatMap(c => c.movies);

function Navbar({ searchQuery, onSearchChange }) {
  const [isScrolled, setIsScrolled] = React.useState(false);
  const [isSearchExpanded, setIsSearchExpanded] = React.useState(false);
  const searchInputRef = React.useRef(null);

  React.useEffect(() => {
    const handleScroll = () => {
      setIsScrolled(window.scrollY > 0);
    };
    window.addEventListener('scroll', handleScroll);
    return () => window.removeEventListener('scroll', handleScroll);
  }, []);

  const handleSearchClick = () => {
    if (!onSearchChange) return;
    setIsSearchExpanded(true);
    setTimeout(() => searchInputRef.current?.focus(), 100);
  };

  const handleSearchBlur = () => {
    if (!searchQuery) {
      setIsSearchExpanded(false);
    }
  };

  return (
    <nav className={`fixed w-full z-50 transition-colors duration-300 ${isScrolled ? 'bg-netflix-black' : 'bg-gradient-to-b from-black/80 to-transparent'}`}>
      <div className="px-4 md:px-12 py-4 flex items-center justify-between">
        <div className="flex items-center gap-4 md:gap-8">
          <Link to="/" className="text-netflix-red text-2xl md:text-3xl font-bold tracking-wider">HAMSTERFLIX</Link>
          <div className="hidden md:flex gap-4 text-sm font-medium text-netflix-light">
            <Link to="/" className="font-bold text-white">Home</Link>
            <span className="cursor-not-allowed opacity-50" title="TV Shows (Coming Soon)">TV Shows</span>
            <span className="cursor-not-allowed opacity-50" title="Movies (Coming Soon)">Movies</span>
            <span className="cursor-not-allowed opacity-50" title="New & Popular (Coming Soon)">New & Popular</span>
            <span className="cursor-not-allowed opacity-50" title="My List (Coming Soon)">My List</span>
          </div>
        </div>
        <div className="flex items-center gap-6 text-white">
          
          <div className="flex items-center">
            {onSearchChange ? (
              <div className={`flex items-center transition-all duration-300 ${isSearchExpanded ? 'border border-white bg-black/60 px-2 py-1' : ''}`}>
                <Search className="w-5 h-5 cursor-pointer hover:text-gray-300" onClick={handleSearchClick} />
                <input 
                  ref={searchInputRef}
                  type="text" 
                  placeholder="Titles, people, genres"
                  value={searchQuery || ''}
                  onChange={(e) => onSearchChange(e.target.value)}
                  onBlur={handleSearchBlur}
                  className={`bg-transparent text-sm text-white placeholder-gray-400 focus:outline-none transition-all duration-300 ${isSearchExpanded ? 'w-48 md:w-64 ml-2 opacity-100' : 'w-0 opacity-0'}`}
                />
              </div>
            ) : (
              <Search className="w-5 h-5 cursor-pointer opacity-50 hover:opacity-100 transition-opacity" title="Search (Coming Soon)" />
            )}
          </div>

          <Bell className="w-5 h-5 cursor-pointer opacity-50 hover:opacity-100 transition-opacity" title="Notifications (Coming Soon)" />
          <div className="flex items-center gap-2 cursor-pointer group relative">
            <div className="w-8 h-8 bg-blue-500 rounded text-xs flex items-center justify-center font-bold">H</div>
            <ChevronDown className="w-4 h-4 group-hover:rotate-180 transition-transform" />
            
            {/* Dropdown Menu */}
            <div className="absolute top-full right-0 mt-4 w-48 bg-black/90 border border-gray-800 rounded shadow-xl opacity-0 invisible group-hover:opacity-100 group-hover:visible transition-all">
              <div className="py-2">
                <button 
                  onClick={() => {
                    localStorage.removeItem('hamsterflix_auth');
                    window.location.reload();
                  }}
                  className="w-full text-left px-4 py-2 text-sm text-gray-300 hover:text-white hover:bg-gray-800 transition-colors"
                >
                  Sign out of Hamsterflix
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>
    </nav>
  );
}

function Hero({ featured }) {
  const heroMovie = featured || FEATURED_MOVIE;
  return (
    <div className="relative h-[80vh] w-full">
      <div className="absolute inset-0">
        <img src={heroMovie.heroImage} alt="Hero Background" className="w-full h-full object-cover" />
        <div className="absolute inset-0 bg-gradient-to-t from-netflix-black via-transparent to-black/50"></div>
        <div className="absolute inset-0 bg-gradient-to-r from-netflix-black/80 via-netflix-black/40 to-transparent"></div>
      </div>
      
      <div className="absolute inset-0 flex flex-col justify-center px-4 md:px-12 pt-20">
        <div className="max-w-2xl">
          <h1 className="text-5xl md:text-7xl font-bold text-white mb-4 drop-shadow-lg font-black tracking-tighter">
            {(heroMovie.title || "").toUpperCase()}
          </h1>
          <p className="text-lg md:text-xl text-white mb-8 drop-shadow-md font-medium text-shadow-sm max-w-xl">
            {heroMovie.description}
          </p>
          <div className="flex gap-4">
            <button className="flex items-center gap-2 bg-white text-black px-6 md:px-8 py-2 md:py-3 rounded hover:bg-white/80 transition-colors font-bold text-lg">
              <Play className="w-6 h-6 fill-current" /> Play
            </button>
            <button className="flex items-center gap-2 bg-gray-500/70 text-white px-6 md:px-8 py-2 md:py-3 rounded hover:bg-gray-500/50 transition-colors font-bold text-lg backdrop-blur-sm">
              <Info className="w-6 h-6" /> More Info
            </button>
          </div>
        </div>
      </div>
    </div>
  );
}

function Row({ title, movies }) {
  const rowRef = React.useRef(null);
  const [showLeftArrow, setShowLeftArrow] = React.useState(false);

  const handleScroll = (direction) => {
    if (rowRef.current) {
      const { scrollLeft, clientWidth } = rowRef.current;
      const scrollTo = direction === 'left' ? scrollLeft - clientWidth : scrollLeft + clientWidth;
      rowRef.current.scrollTo({ left: scrollTo, behavior: 'smooth' });
    }
  };

  const handleScrollEvent = () => {
    if (rowRef.current) {
      setShowLeftArrow(rowRef.current.scrollLeft > 0);
    }
  };

  return (
    <div className="px-4 md:px-12 py-4 relative group z-10">
      <h2 className="text-white text-xl md:text-2xl font-bold mb-4">{title}</h2>
      <div className="relative">
        {showLeftArrow && (
          <button 
            onClick={() => handleScroll('left')}
            className="absolute left-0 top-0 bottom-8 w-12 bg-black/50 hover:bg-black/70 z-30 flex items-center justify-center opacity-0 group-hover:opacity-100 transition-all rounded-l-md"
          >
            <ChevronLeft className="w-8 h-8 text-white transition-transform hover:scale-125" />
          </button>
        )}
        <div 
          ref={rowRef} 
          onScroll={handleScrollEvent}
          className="flex gap-4 overflow-x-auto hide-scrollbar pb-8 pt-4 -mt-4 px-2 -mx-2"
        >
          {movies.map(movie => (
            <Link key={movie.id} to={`/movie/${movie.id}`} className="relative flex-none w-[140px] md:w-[200px] h-[210px] md:h-[300px] transition-all duration-300 hover:scale-110 hover:z-20 origin-center cursor-pointer rounded-md overflow-hidden shadow-lg border border-transparent hover:border-gray-500">
              <img src={movie.img || movie.poster_filename || '/posters_real/poster_real_1.png'} alt={movie.title} className="w-full h-full object-cover" />
              <div className="absolute inset-0 bg-gradient-to-t from-black/90 via-black/20 to-transparent opacity-0 hover:opacity-100 transition-opacity duration-300 flex flex-col justify-end p-4">
                <p className="text-white font-bold text-sm md:text-base drop-shadow-md text-center">{movie.title}</p>
              </div>
            </Link>
          ))}
        </div>
        <button 
          onClick={() => handleScroll('right')}
          className="absolute right-0 top-0 bottom-8 w-12 bg-black/50 hover:bg-black/70 z-30 flex items-center justify-center opacity-0 group-hover:opacity-100 transition-all rounded-r-md"
        >
          <ChevronRight className="w-8 h-8 text-white transition-transform hover:scale-125" />
        </button>
      </div>
    </div>
  );
}

function Home() {
    const [categories, setCategories] = React.useState([]);
    const [allMovies, setAllMovies] = React.useState([]);
    const [featured, setFeatured] = React.useState(FEATURED_MOVIE);
    const [searchQuery, setSearchQuery] = React.useState("");

    React.useEffect(() => {
      fetch('/api/movies')
        .then(res => res.json())
        .then(data => {
          if (data && data.length > 0) {
             setAllMovies(data);
           
             const trending = [];
             const thrills = [];
             const comedies = [];
             const scifi = [];
             const action = [];
             const docs = [];

             data.forEach((movie, i) => {
               const genres = (movie.genres || '').toLowerCase();
               const mood = (movie.mood || '').toLowerCase();
               if (genres.includes("comedy") || mood.includes("funny") || mood.includes("silly")) {
                 comedies.push(movie);
               } else if (genres.includes("sci-fi") || genres.includes("fantasy")) {
                 scifi.push(movie);
               } else if (genres.includes("thriller") || genres.includes("horror") || mood.includes("intense")) {
                 thrills.push(movie);
               } else if (genres.includes("documentary") || genres.includes("family")) {
                 docs.push(movie);
               } else if (genres.includes("action") || genres.includes("adventure") || mood.includes("fast-paced")) {
                 action.push(movie);
               } else {
                 trending.push(movie); // catch-all
               }
             
               // Just force some balance if trending is too empty
               if (i % 7 === 0) trending.push(movie);
             });

             const chunked = [
               { title: "Wheel Spinners (Trending)", movies: [...new Set(trending)] },
               { title: "Squeak-Inducing Thrills", movies: thrills },
               { title: "Cheeky Comedies", movies: comedies },
               { title: "Cage-Free Sci-Fi", movies: scifi },
               { title: "High-Speed Pursuits", movies: action },
               { title: "Critically Acclaimed Fluff", movies: docs }
             ].filter(c => c.movies.length > 0);

             setCategories(chunked);
           
             // Set the first movie as the featured one
             if (data.length > 0) {
               setFeatured({
                 title: data[0].title,
                 description: data[0].synopsis,
                 heroImage: data[0].img
               });
             }
          }
        })
        .catch(e => console.error("Failed to fetch movies", e));
    }, []);

    const searchResults = React.useMemo(() => {
      if (!searchQuery.trim()) return [];
      const lowerQuery = searchQuery.toLowerCase();
      return allMovies.filter(m => {
        const titleMatch = m.title && m.title.toLowerCase().includes(lowerQuery);
        const synMatch = m.synopsis && m.synopsis.toLowerCase().includes(lowerQuery);
        const genreMatch = m.genres && m.genres.toLowerCase().includes(lowerQuery);
        
        let castMatch = false;
        if (m.cast && typeof m.cast === 'string') {
           try {
             const parsedCast = JSON.parse(m.cast);
             castMatch = parsedCast.some(c => 
               (c.name && c.name.toLowerCase().includes(lowerQuery)) ||
               (c.real_actor && c.real_actor.toLowerCase().includes(lowerQuery)) ||
               (c.character && c.character.toLowerCase().includes(lowerQuery))
             );
           } catch(e) {}
        }
        
        return titleMatch || synMatch || genreMatch || castMatch;
      });
    }, [searchQuery, allMovies]);

    return (
      <>
        <Navbar searchQuery={searchQuery} onSearchChange={setSearchQuery} />
        {searchQuery.trim() ? (
          <div className="pt-32 px-4 md:px-12 pb-20 min-h-screen">
            <h2 className="text-2xl font-bold text-gray-400 mb-8">
              Search results for "{searchQuery}"
            </h2>
            {searchResults.length > 0 ? (
              <div className="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 lg:grid-cols-5 gap-4 gap-y-10">
                {searchResults.map((movie, idx) => (
                  <Link key={idx} to={`/browse/${movie.uid}`} className="group relative aspect-[2/3] bg-gray-900 rounded-md overflow-hidden cursor-pointer">
                    <img src={movie.img || movie.poster_filename || '/posters_real/poster_real_1.png'} alt={movie.title} className="w-full h-full object-cover group-hover:scale-105 transition-transform duration-300" />
                    <div className="absolute inset-0 bg-black/60 opacity-0 group-hover:opacity-100 transition-opacity flex flex-col justify-end p-4">
                      <div className="text-white font-bold text-sm md:text-md leading-tight mb-1">{movie.title}</div>
                      <div className="flex items-center gap-2 mt-2">
                        <Play className="w-6 h-6 fill-white" />
                        <Plus className="w-6 h-6 border-2 border-gray-400 rounded-full p-1 hover:border-white" />
                      </div>
                    </div>
                  </Link>
                ))}
              </div>
            ) : (
              <div className="text-center mt-20">
                <p className="text-gray-400 text-lg">No matches found for "{searchQuery}".</p>
                <p className="text-gray-500 mt-2">Try checking for typos or using different keywords.</p>
              </div>
            )}
          </div>
        ) : (
          <>
            <Hero featured={featured} />
            <div className="-mt-32 relative z-20 pb-20">
              {categories.map((cat, idx) => (
                <Row key={idx} title={cat.title} movies={cat.movies} />
              ))}
            </div>
          </>
        )}
      </>
    );
  }

const EXTRACTED_DATA = {
  "1": {
    "cast": [
      {
        "name": "Pumpkin",
        "character": "The Tunnel Navigator",
        "img": "/posters/poster_14.png"
      },
      {
        "name": "Barnaby",
        "character": "The Biter",
        "img": "/posters/poster_22.png"
      },
      {
        "name": "Sir Fluffs",
        "character": "The Lookout",
        "img": "/posters/poster_20.png"
      },
      {
        "name": "Nugget",
        "character": "The Seed Hoarder",
        "img": "/posters/poster_20.png"
      },
      {
        "name": "Pip",
        "character": "The Wheel Runner",
        "img": "/posters/poster_24.png"
      },
      {
        "name": "Paws",
        "character": "The Cage Climber",
        "img": "/posters/poster_13.png"
      },
      {
        "name": "Furball",
        "character": "The Wheel Runner",
        "img": "/posters/poster_36.png"
      },
      {
        "name": "Mocha",
        "character": "The Treat Thief",
        "img": "/posters/poster_15.png"
      },
      {
        "name": "Pompom",
        "character": "The Escape Artist",
        "img": "/posters/poster_30.png"
      },
      {
        "name": "Dusty",
        "character": "The Biter",
        "img": "/posters/poster_14.png"
      },
      {
        "name": "Cheeks",
        "character": "The Seed Hoarder",
        "img": "/posters/poster_33.png"
      }
    ],
    "director": "Steven Spielberg",
    "synopsis": "In a world where the wheel never stops turning, one hamster must face the ultimate challenge. Experience 'Sunflower Seeds' like never before in this epic drama tale of survival, seeds, and late-night running.",
    "genres": [
      "Drama",
      "Animation"
    ],
    "mood": [
      "Intense",
      "Furry"
    ],
    "trailer_concept": "[0:00-0:10] A moody, cinematic opening. Sunlight filters through the cage bars, casting long shadows. A intense atmosphere.\n\n[0:10-0:20] The hamster sits motionless on the wheel, contemplating the meaning of the spinning cycle. Emotional string music swells.\n\n[0:20-0:30] A tear-jerking climax as the hamster finally reaches the top of the ramp. Fade to white with the title: 'Sunflower Seeds'."
  },
  "2": {
    "cast": [
      {
        "name": "Peanut",
        "character": "The Escape Artist",
        "img": "/posters/poster_15.png"
      },
      {
        "name": "Cashew",
        "character": "The Mastermind",
        "img": "/posters/poster_16.png"
      },
      {
        "name": "Buster",
        "character": "The Sidekick",
        "img": "/posters/poster_8.png"
      },
      {
        "name": "Buttercup",
        "character": "The Seed Hoarder",
        "img": "/posters/poster_39.png"
      },
      {
        "name": "Snickers",
        "character": "The Villain",
        "img": "/posters/poster_30.png"
      },
      {
        "name": "Whiskers",
        "character": "The Squeaker",
        "img": "/posters/poster_38.png"
      },
      {
        "name": "Nibbles",
        "character": "The Tunnel Navigator",
        "img": "/posters/poster_41.png"
      },
      {
        "name": "Cheeks",
        "character": "The Cage Climber",
        "img": "/posters/poster_49.png"
      },
      {
        "name": "Pompom",
        "character": "The Hero",
        "img": "/posters/poster_31.png"
      },
      {
        "name": "Bean",
        "character": "The Mastermind",
        "img": "/posters/poster_22.png"
      },
      {
        "name": "Muffin",
        "character": "The Villain",
        "img": "/posters/poster_34.png"
      },
      {
        "name": "Biscuit",
        "character": "The Hero",
        "img": "/posters/poster_19.png"
      },
      {
        "name": "Barnaby",
        "character": "The Treat Thief",
        "img": "/posters/poster_20.png"
      }
    ],
    "director": "Steven Spielberg",
    "synopsis": "In a world where the wheel never stops turning, one hamster must face the ultimate challenge. Experience 'The Maze Runner' like never before in this epic drama tale of survival, seeds, and late-night running.",
    "genres": [
      "Drama",
      "Animation"
    ],
    "mood": [
      "Heartwarming",
      "Fast-Paced"
    ],
    "trailer_concept": "[0:00-0:10] A moody, cinematic opening. Sunlight filters through the cage bars, casting long shadows. A heartwarming atmosphere.\n\n[0:10-0:20] The hamster sits motionless on the wheel, contemplating the meaning of the spinning cycle. Emotional string music swells.\n\n[0:20-0:30] A tear-jerking climax as the hamster finally reaches the top of the ramp. Fade to white with the title: 'The Maze Runner'."
  },
  "3": {
    "cast": [
      {
        "name": "Snickers",
        "character": "The Squeaker",
        "img": "/posters/poster_8.png"
      },
      {
        "name": "Muffin",
        "character": "The Mastermind",
        "img": "/posters/poster_21.png"
      },
      {
        "name": "Marshmallow",
        "character": "The Squeaker",
        "img": "/posters/poster_10.png"
      },
      {
        "name": "Chestnut",
        "character": "The Cage Climber",
        "img": "/posters/poster_49.png"
      },
      {
        "name": "Furball",
        "character": "The Squeaker",
        "img": "/posters/poster_36.png"
      },
      {
        "name": "Pip",
        "character": "The Mastermind",
        "img": "/posters/poster_2.png"
      },
      {
        "name": "Biscuit",
        "character": "The Escape Artist",
        "img": "/posters/poster_49.png"
      },
      {
        "name": "Nugget",
        "character": "The Villain",
        "img": "/posters/poster_31.png"
      }
    ],
    "director": "Wes Anderson",
    "synopsis": "In a world where the wheel never stops turning, one hamster must face the ultimate challenge. Experience 'Midnight Snack' like never before in this epic drama tale of survival, seeds, and late-night running.",
    "genres": [
      "Drama",
      "Family"
    ],
    "mood": [
      "Exciting",
      "Exciting"
    ],
    "trailer_concept": "[0:00-0:10] A moody, cinematic opening. Sunlight filters through the cage bars, casting long shadows. A exciting atmosphere.\n\n[0:10-0:20] The hamster sits motionless on the wheel, contemplating the meaning of the spinning cycle. Emotional string music swells.\n\n[0:20-0:30] A tear-jerking climax as the hamster finally reaches the top of the ramp. Fade to white with the title: 'Midnight Snack'."
  },
  "4": {
    "cast": [
      {
        "name": "Biscuit",
        "character": "The Squeaker",
        "img": "/posters/poster_2.png"
      },
      {
        "name": "Pumpkin",
        "character": "The Cage Climber",
        "img": "/posters/poster_34.png"
      },
      {
        "name": "Muffin",
        "character": "The Treat Thief",
        "img": "/posters/poster_28.png"
      },
      {
        "name": "Peanut",
        "character": "The Squeaker",
        "img": "/posters/poster_1.png"
      },
      {
        "name": "Nugget",
        "character": "The Sleeper",
        "img": "/posters/poster_9.png"
      },
      {
        "name": "Sir Fluffs",
        "character": "The Wheel Runner",
        "img": "/posters/poster_12.png"
      },
      {
        "name": "Buttercup",
        "character": "The Squeaker",
        "img": "/posters/poster_27.png"
      },
      {
        "name": "Pompom",
        "character": "The Lookout",
        "img": "/posters/poster_29.png"
      },
      {
        "name": "Cheeks",
        "character": "The Treat Thief",
        "img": "/posters/poster_18.png"
      },
      {
        "name": "Buster",
        "character": "The Villain",
        "img": "/posters/poster_19.png"
      },
      {
        "name": "Paws",
        "character": "The Tunnel Navigator",
        "img": "/posters/poster_13.png"
      },
      {
        "name": "Whiskers",
        "character": "The Sidekick",
        "img": "/posters/poster_3.png"
      }
    ],
    "director": "Steven Spielberg",
    "synopsis": "In a world where the wheel never stops turning, one hamster must face the ultimate challenge. Experience 'Tube City' like never before in this epic drama tale of survival, seeds, and late-night running.",
    "genres": [
      "Drama",
      "Animation"
    ],
    "mood": [
      "Furry",
      "Heartwarming"
    ],
    "trailer_concept": "[0:00-0:10] A moody, cinematic opening. Sunlight filters through the cage bars, casting long shadows. A furry atmosphere.\n\n[0:10-0:20] The hamster sits motionless on the wheel, contemplating the meaning of the spinning cycle. Emotional string music swells.\n\n[0:20-0:30] A tear-jerking climax as the hamster finally reaches the top of the ramp. Fade to white with the title: 'Tube City'."
  },
  "5": {
    "cast": [
      {
        "name": "Hazel",
        "character": "The Lookout",
        "img": "/posters/poster_32.png"
      },
      {
        "name": "Teddy",
        "character": "The Seed Hoarder",
        "img": "/posters/poster_18.png"
      },
      {
        "name": "Pip",
        "character": "The Villain",
        "img": "/posters/poster_26.png"
      },
      {
        "name": "Muffin",
        "character": "The Biter",
        "img": "/posters/poster_17.png"
      },
      {
        "name": "Chubby",
        "character": "The Hero",
        "img": "/posters/poster_17.png"
      },
      {
        "name": "Bean",
        "character": "The Squeaker",
        "img": "/posters/poster_32.png"
      },
      {
        "name": "Barnaby",
        "character": "The Sleeper",
        "img": "/posters/poster_38.png"
      },
      {
        "name": "Marshmallow",
        "character": "The Wise Elder",
        "img": "/posters/poster_23.png"
      },
      {
        "name": "Biscuit",
        "character": "The Wheel Runner",
        "img": "/posters/poster_26.png"
      },
      {
        "name": "Sir Fluffs",
        "character": "The Wise Elder",
        "img": "/posters/poster_13.png"
      },
      {
        "name": "Snickers",
        "character": "The Seed Hoarder",
        "img": "/posters/poster_8.png"
      },
      {
        "name": "Nugget",
        "character": "The Wheel Runner",
        "img": "/posters/poster_40.png"
      },
      {
        "name": "Cashew",
        "character": "The Sleeper",
        "img": "/posters/poster_33.png"
      },
      {
        "name": "Squeaks",
        "character": "The Seed Hoarder",
        "img": "/posters/poster_9.png"
      }
    ],
    "director": "Wes Anderson",
    "synopsis": "In a world where the wheel never stops turning, one hamster must face the ultimate challenge. Experience 'Cheek Pouches' like never before in this epic drama tale of survival, seeds, and late-night running.",
    "genres": [
      "Drama",
      "Family"
    ],
    "mood": [
      "Squeaky",
      "Fast-Paced"
    ],
    "trailer_concept": "[0:00-0:10] A moody, cinematic opening. Sunlight filters through the cage bars, casting long shadows. A squeaky atmosphere.\n\n[0:10-0:20] The hamster sits motionless on the wheel, contemplating the meaning of the spinning cycle. Emotional string music swells.\n\n[0:20-0:30] A tear-jerking climax as the hamster finally reaches the top of the ramp. Fade to white with the title: 'Cheek Pouches'."
  },
  "6": {
    "cast": [
      {
        "name": "Mocha",
        "character": "The Villain",
        "img": "/posters/poster_7.png"
      },
      {
        "name": "Pompom",
        "character": "The Mastermind",
        "img": "/posters/poster_16.png"
      },
      {
        "name": "Chubby",
        "character": "The Wise Elder",
        "img": "/posters/poster_39.png"
      },
      {
        "name": "Nibbles",
        "character": "The Squeaker",
        "img": "/posters/poster_6.png"
      },
      {
        "name": "Muffin",
        "character": "The Seed Hoarder",
        "img": "/posters/poster_16.png"
      },
      {
        "name": "Coco",
        "character": "The Seed Hoarder",
        "img": "/posters/poster_10.png"
      },
      {
        "name": "Oreo",
        "character": "The Hero",
        "img": "/posters/poster_49.png"
      },
      {
        "name": "Whiskers",
        "character": "The Cage Climber",
        "img": "/posters/poster_22.png"
      },
      {
        "name": "Snickers",
        "character": "The Hero",
        "img": "/posters/poster_26.png"
      },
      {
        "name": "Pip",
        "character": "The Hero",
        "img": "/posters/poster_33.png"
      },
      {
        "name": "Pumpkin",
        "character": "The Squeaker",
        "img": "/posters/poster_16.png"
      },
      {
        "name": "Marshmallow",
        "character": "The Sidekick",
        "img": "/posters/poster_29.png"
      },
      {
        "name": "Paws",
        "character": "The Lookout",
        "img": "/posters/poster_30.png"
      }
    ],
    "director": "Christopher Nolan",
    "synopsis": "In a world where the wheel never stops turning, one hamster must face the ultimate challenge. Experience 'Wheel of Time' like never before in this epic drama tale of survival, seeds, and late-night running.",
    "genres": [
      "Drama",
      "Animation"
    ],
    "mood": [
      "Squeaky",
      "Intense"
    ],
    "trailer_concept": "[0:00-0:10] A moody, cinematic opening. Sunlight filters through the cage bars, casting long shadows. A squeaky atmosphere.\n\n[0:10-0:20] The hamster sits motionless on the wheel, contemplating the meaning of the spinning cycle. Emotional string music swells.\n\n[0:20-0:30] A tear-jerking climax as the hamster finally reaches the top of the ramp. Fade to white with the title: 'Wheel of Time'."
  },
  "7": {
    "cast": [
      {
        "name": "Muffin",
        "character": "The Sleeper",
        "img": "/posters/poster_32.png"
      },
      {
        "name": "Teddy",
        "character": "The Treat Thief",
        "img": "/posters/poster_19.png"
      },
      {
        "name": "Pumpkin",
        "character": "The Escape Artist",
        "img": "/posters/poster_24.png"
      },
      {
        "name": "Biscuit",
        "character": "The Cage Climber",
        "img": "/posters/poster_10.png"
      },
      {
        "name": "Buster",
        "character": "The Mastermind",
        "img": "/posters/poster_2.png"
      },
      {
        "name": "Paws",
        "character": "The Escape Artist",
        "img": "/posters/poster_28.png"
      },
      {
        "name": "Chubby",
        "character": "The Wheel Runner",
        "img": "/posters/poster_31.png"
      },
      {
        "name": "Nugget",
        "character": "The Seed Hoarder",
        "img": "/posters/poster_1.png"
      },
      {
        "name": "Oreo",
        "character": "The Treat Thief",
        "img": "/posters/poster_29.png"
      },
      {
        "name": "Bean",
        "character": "The Biter",
        "img": "/posters/poster_32.png"
      },
      {
        "name": "Barnaby",
        "character": "The Hero",
        "img": "/posters/poster_9.png"
      },
      {
        "name": "Hazel",
        "character": "The Wise Elder",
        "img": "/posters/poster_22.png"
      }
    ],
    "director": "Christopher Nolan",
    "synopsis": "In a world where the wheel never stops turning, one hamster must face the ultimate challenge. Experience 'Furry Fury' like never before in this epic action tale of survival, seeds, and late-night running.",
    "genres": [
      "Action",
      "Adventure"
    ],
    "mood": [
      "Exciting",
      "Exciting"
    ],
    "trailer_concept": "[0:00-0:10] Heartbeat sound effect. Pitch black. Suddenly, the cage door clicks open. The exciting tension is palpable.\n\n[0:10-0:20] Fast cuts: A shadow of a house cat. The hamster stuffing cheeks with seeds. A frantic dash through the plastic tunnels.\n\n[0:20-0:30] An explosive slow-motion dive off the second level of the cage. Heavy bass drop. 'Furry Fury' slams onto the screen."
  },
  "8": {
    "cast": [
      {
        "name": "Pompom",
        "character": "The Sidekick",
        "img": "/posters/poster_29.png"
      },
      {
        "name": "Pumpkin",
        "character": "The Hero",
        "img": "/posters/poster_36.png"
      },
      {
        "name": "Barnaby",
        "character": "The Sleeper",
        "img": "/posters/poster_2.png"
      },
      {
        "name": "Marshmallow",
        "character": "The Hero",
        "img": "/posters/poster_35.png"
      },
      {
        "name": "Hazel",
        "character": "The Villain",
        "img": "/posters/poster_13.png"
      },
      {
        "name": "Coco",
        "character": "The Cage Climber",
        "img": "/posters/poster_10.png"
      },
      {
        "name": "Bean",
        "character": "The Squeaker",
        "img": "/posters/poster_24.png"
      },
      {
        "name": "Buttercup",
        "character": "The Villain",
        "img": "/posters/poster_4.png"
      },
      {
        "name": "Dusty",
        "character": "The Biter",
        "img": "/posters/poster_16.png"
      },
      {
        "name": "Buster",
        "character": "The Wise Elder",
        "img": "/posters/poster_25.png"
      },
      {
        "name": "Chubby",
        "character": "The Lookout",
        "img": "/posters/poster_29.png"
      },
      {
        "name": "Furball",
        "character": "The Wheel Runner",
        "img": "/posters/poster_40.png"
      },
      {
        "name": "Whiskers",
        "character": "The Villain",
        "img": "/posters/poster_35.png"
      },
      {
        "name": "Paws",
        "character": "The Treat Thief",
        "img": "/posters/poster_6.png"
      }
    ],
    "director": "Greta Gerwig",
    "synopsis": "In a world where the wheel never stops turning, one hamster must face the ultimate challenge. Experience 'Bite Sized' like never before in this epic action tale of survival, seeds, and late-night running.",
    "genres": [
      "Action",
      "Adventure"
    ],
    "mood": [
      "Fast-Paced",
      "Intense"
    ],
    "trailer_concept": "[0:00-0:10] Heartbeat sound effect. Pitch black. Suddenly, the cage door clicks open. The fast-paced tension is palpable.\n\n[0:10-0:20] Fast cuts: A shadow of a house cat. The hamster stuffing cheeks with seeds. A frantic dash through the plastic tunnels.\n\n[0:20-0:30] An explosive slow-motion dive off the second level of the cage. Heavy bass drop. 'Bite Sized' slams onto the screen."
  },
  "9": {
    "cast": [
      {
        "name": "Buttercup",
        "character": "The Treat Thief",
        "img": "/posters/poster_30.png"
      },
      {
        "name": "Biscuit",
        "character": "The Lookout",
        "img": "/posters/poster_35.png"
      },
      {
        "name": "Paws",
        "character": "The Wise Elder",
        "img": "/posters/poster_31.png"
      },
      {
        "name": "Buster",
        "character": "The Sleeper",
        "img": "/posters/poster_38.png"
      },
      {
        "name": "Marshmallow",
        "character": "The Wheel Runner",
        "img": "/posters/poster_26.png"
      },
      {
        "name": "Pumpkin",
        "character": "The Squeaker",
        "img": "/posters/poster_21.png"
      },
      {
        "name": "Oreo",
        "character": "The Sidekick",
        "img": "/posters/poster_3.png"
      },
      {
        "name": "Whiskers",
        "character": "The Sidekick",
        "img": "/posters/poster_3.png"
      }
    ],
    "director": "Wes Anderson",
    "synopsis": "In a world where the wheel never stops turning, one hamster must face the ultimate challenge. Experience 'Rodent Racer' like never before in this epic action tale of survival, seeds, and late-night running.",
    "genres": [
      "Action",
      "Animation"
    ],
    "mood": [
      "Exciting",
      "Squeaky"
    ],
    "trailer_concept": "[0:00-0:10] Heartbeat sound effect. Pitch black. Suddenly, the cage door clicks open. The exciting tension is palpable.\n\n[0:10-0:20] Fast cuts: A shadow of a house cat. The hamster stuffing cheeks with seeds. A frantic dash through the plastic tunnels.\n\n[0:20-0:30] An explosive slow-motion dive off the second level of the cage. Heavy bass drop. 'Rodent Racer' slams onto the screen."
  },
  "10": {
    "cast": [
      {
        "name": "Chestnut",
        "character": "The Biter",
        "img": "/posters/poster_39.png"
      },
      {
        "name": "Bean",
        "character": "The Hero",
        "img": "/posters/poster_49.png"
      },
      {
        "name": "Coco",
        "character": "The Cage Climber",
        "img": "/posters/poster_12.png"
      },
      {
        "name": "Furball",
        "character": "The Treat Thief",
        "img": "/posters/poster_15.png"
      },
      {
        "name": "Dusty",
        "character": "The Mastermind",
        "img": "/posters/poster_28.png"
      },
      {
        "name": "Hazel",
        "character": "The Squeaker",
        "img": "/posters/poster_11.png"
      },
      {
        "name": "Nibbles",
        "character": "The Wheel Runner",
        "img": "/posters/poster_41.png"
      },
      {
        "name": "Cheeks",
        "character": "The Tunnel Navigator",
        "img": "/posters/poster_33.png"
      },
      {
        "name": "Buttercup",
        "character": "The Wise Elder",
        "img": "/posters/poster_2.png"
      },
      {
        "name": "Oreo",
        "character": "The Hero",
        "img": "/posters/poster_32.png"
      },
      {
        "name": "Squeaks",
        "character": "The Sidekick",
        "img": "/posters/poster_33.png"
      },
      {
        "name": "Nugget",
        "character": "The Mastermind",
        "img": "/posters/poster_26.png"
      },
      {
        "name": "Waffles",
        "character": "The Wise Elder",
        "img": "/posters/poster_28.png"
      }
    ],
    "director": "Greta Gerwig",
    "synopsis": "In a world where the wheel never stops turning, one hamster must face the ultimate challenge. Experience 'The Great Cage' like never before in this epic action tale of survival, seeds, and late-night running.",
    "genres": [
      "Action",
      "Animation"
    ],
    "mood": [
      "Fast-Paced",
      "Intense"
    ],
    "trailer_concept": "[0:00-0:10] Heartbeat sound effect. Pitch black. Suddenly, the cage door clicks open. The fast-paced tension is palpable.\n\n[0:10-0:20] Fast cuts: A shadow of a house cat. The hamster stuffing cheeks with seeds. A frantic dash through the plastic tunnels.\n\n[0:20-0:30] An explosive slow-motion dive off the second level of the cage. Heavy bass drop. 'The Great Cage' slams onto the screen."
  },
  "11": {
    "cast": [
      {
        "name": "Buster",
        "character": "The Escape Artist",
        "img": "/posters/poster_5.png"
      },
      {
        "name": "Barnaby",
        "character": "The Lookout",
        "img": "/posters/poster_38.png"
      },
      {
        "name": "Buttercup",
        "character": "The Sidekick",
        "img": "/posters/poster_27.png"
      },
      {
        "name": "Nibbles",
        "character": "The Treat Thief",
        "img": "/posters/poster_38.png"
      },
      {
        "name": "Coco",
        "character": "The Hero",
        "img": "/posters/poster_12.png"
      },
      {
        "name": "Dusty",
        "character": "The Mastermind",
        "img": "/posters/poster_40.png"
      },
      {
        "name": "Squeaks",
        "character": "The Wheel Runner",
        "img": "/posters/poster_33.png"
      },
      {
        "name": "Nugget",
        "character": "The Hero",
        "img": "/posters/poster_26.png"
      },
      {
        "name": "Snickers",
        "character": "The Cage Climber",
        "img": "/posters/poster_8.png"
      },
      {
        "name": "Cheeks",
        "character": "The Mastermind",
        "img": "/posters/poster_12.png"
      },
      {
        "name": "Bean",
        "character": "The Squeaker",
        "img": "/posters/poster_12.png"
      },
      {
        "name": "Mocha",
        "character": "The Sleeper",
        "img": "/posters/poster_28.png"
      },
      {
        "name": "Hazel",
        "character": "The Squeaker",
        "img": "/posters/poster_2.png"
      }
    ],
    "director": "Steven Spielberg",
    "synopsis": "In a world where the wheel never stops turning, one hamster must face the ultimate challenge. Experience 'Wood Shavings' like never before in this epic action tale of survival, seeds, and late-night running.",
    "genres": [
      "Action",
      "Family"
    ],
    "mood": [
      "Heartwarming",
      "Furry"
    ],
    "trailer_concept": "[0:00-0:10] Heartbeat sound effect. Pitch black. Suddenly, the cage door clicks open. The heartwarming tension is palpable.\n\n[0:10-0:20] Fast cuts: A shadow of a house cat. The hamster stuffing cheeks with seeds. A frantic dash through the plastic tunnels.\n\n[0:20-0:30] An explosive slow-motion dive off the second level of the cage. Heavy bass drop. 'Wood Shavings' slams onto the screen."
  },
  "12": {
    "cast": [
      {
        "name": "Snickers",
        "character": "The Cage Climber",
        "img": "/posters/poster_5.png"
      },
      {
        "name": "Bean",
        "character": "The Squeaker",
        "img": "/posters/poster_26.png"
      },
      {
        "name": "Buttercup",
        "character": "The Hero",
        "img": "/posters/poster_33.png"
      },
      {
        "name": "Coco",
        "character": "The Villain",
        "img": "/posters/poster_24.png"
      },
      {
        "name": "Oreo",
        "character": "The Wheel Runner",
        "img": "/posters/poster_39.png"
      },
      {
        "name": "Biscuit",
        "character": "The Sidekick",
        "img": "/posters/poster_22.png"
      },
      {
        "name": "Squeaks",
        "character": "The Escape Artist",
        "img": "/posters/poster_23.png"
      },
      {
        "name": "Furball",
        "character": "The Sleeper",
        "img": "/posters/poster_8.png"
      },
      {
        "name": "Pompom",
        "character": "The Biter",
        "img": "/posters/poster_36.png"
      },
      {
        "name": "Cheeks",
        "character": "The Sleeper",
        "img": "/posters/poster_4.png"
      },
      {
        "name": "Nugget",
        "character": "The Biter",
        "img": "/posters/poster_16.png"
      },
      {
        "name": "Cashew",
        "character": "The Seed Hoarder",
        "img": "/posters/poster_4.png"
      },
      {
        "name": "Dusty",
        "character": "The Cage Climber",
        "img": "/posters/poster_39.png"
      },
      {
        "name": "Teddy",
        "character": "The Escape Artist",
        "img": "/posters/poster_25.png"
      }
    ],
    "director": "Christopher Nolan",
    "synopsis": "In a world where the wheel never stops turning, one hamster must face the ultimate challenge. Experience 'Sleep All Day' like never before in this epic action tale of survival, seeds, and late-night running.",
    "genres": [
      "Action",
      "Family"
    ],
    "mood": [
      "Squeaky",
      "Intense"
    ],
    "trailer_concept": "[0:00-0:10] Heartbeat sound effect. Pitch black. Suddenly, the cage door clicks open. The squeaky tension is palpable.\n\n[0:10-0:20] Fast cuts: A shadow of a house cat. The hamster stuffing cheeks with seeds. A frantic dash through the plastic tunnels.\n\n[0:20-0:30] An explosive slow-motion dive off the second level of the cage. Heavy bass drop. 'Sleep All Day' slams onto the screen."
  },
  "13": {
    "cast": [
      {
        "name": "Whiskers",
        "character": "The Tunnel Navigator",
        "img": "/posters/poster_38.png"
      },
      {
        "name": "Cashew",
        "character": "The Squeaker",
        "img": "/posters/poster_49.png"
      },
      {
        "name": "Coco",
        "character": "The Tunnel Navigator",
        "img": "/posters/poster_19.png"
      },
      {
        "name": "Biscuit",
        "character": "The Biter",
        "img": "/posters/poster_17.png"
      },
      {
        "name": "Bean",
        "character": "The Treat Thief",
        "img": "/posters/poster_28.png"
      },
      {
        "name": "Dusty",
        "character": "The Hero",
        "img": "/posters/poster_24.png"
      },
      {
        "name": "Nugget",
        "character": "The Squeaker",
        "img": "/posters/poster_19.png"
      },
      {
        "name": "Barnaby",
        "character": "The Sidekick",
        "img": "/posters/poster_38.png"
      },
      {
        "name": "Squeaks",
        "character": "The Biter",
        "img": "/posters/poster_15.png"
      },
      {
        "name": "Pumpkin",
        "character": "The Biter",
        "img": "/posters/poster_43.png"
      },
      {
        "name": "Paws",
        "character": "The Cage Climber",
        "img": "/posters/poster_20.png"
      },
      {
        "name": "Sir Fluffs",
        "character": "The Sidekick",
        "img": "/posters/poster_16.png"
      },
      {
        "name": "Snickers",
        "character": "The Sleeper",
        "img": "/posters/poster_25.png"
      },
      {
        "name": "Chubby",
        "character": "The Cage Climber",
        "img": "/posters/poster_22.png"
      }
    ],
    "director": "Greta Gerwig",
    "synopsis": "In a world where the wheel never stops turning, one hamster must face the ultimate challenge. Experience 'The Nut Job' like never before in this epic drama tale of survival, seeds, and late-night running.",
    "genres": [
      "Drama",
      "Family"
    ],
    "mood": [
      "Intense",
      "Intense"
    ],
    "trailer_concept": "[0:00-0:10] A moody, cinematic opening. Sunlight filters through the cage bars, casting long shadows. A intense atmosphere.\n\n[0:10-0:20] The hamster sits motionless on the wheel, contemplating the meaning of the spinning cycle. Emotional string music swells.\n\n[0:20-0:30] A tear-jerking climax as the hamster finally reaches the top of the ramp. Fade to white with the title: 'The Nut Job'."
  },
  "14": {
    "cast": [
      {
        "name": "Cashew",
        "character": "The Mastermind",
        "img": "/posters/poster_6.png"
      },
      {
        "name": "Whiskers",
        "character": "The Wheel Runner",
        "img": "/posters/poster_51.png"
      },
      {
        "name": "Sir Fluffs",
        "character": "The Escape Artist",
        "img": "/posters/poster_39.png"
      },
      {
        "name": "Biscuit",
        "character": "The Biter",
        "img": "/posters/poster_51.png"
      },
      {
        "name": "Cheeks",
        "character": "The Tunnel Navigator",
        "img": "/posters/poster_9.png"
      },
      {
        "name": "Pip",
        "character": "The Squeaker",
        "img": "/posters/poster_8.png"
      },
      {
        "name": "Furball",
        "character": "The Sidekick",
        "img": "/posters/poster_36.png"
      },
      {
        "name": "Mocha",
        "character": "The Cage Climber",
        "img": "/posters/poster_19.png"
      }
    ],
    "director": "Greta Gerwig",
    "synopsis": "In a world where the wheel never stops turning, one hamster must face the ultimate challenge. Experience 'Midnight Runner' like never before in this epic drama tale of survival, seeds, and late-night running.",
    "genres": [
      "Drama",
      "Animation"
    ],
    "mood": [
      "Heartwarming",
      "Heartwarming"
    ],
    "trailer_concept": "[0:00-0:10] A moody, cinematic opening. Sunlight filters through the cage bars, casting long shadows. A heartwarming atmosphere.\n\n[0:10-0:20] The hamster sits motionless on the wheel, contemplating the meaning of the spinning cycle. Emotional string music swells.\n\n[0:20-0:30] A tear-jerking climax as the hamster finally reaches the top of the ramp. Fade to white with the title: 'Midnight Runner'."
  },
  "15": {
    "cast": [
      {
        "name": "Mocha",
        "character": "The Wheel Runner",
        "img": "/posters/poster_20.png"
      },
      {
        "name": "Buttercup",
        "character": "The Hero",
        "img": "/posters/poster_1.png"
      },
      {
        "name": "Bean",
        "character": "The Sleeper",
        "img": "/posters/poster_22.png"
      },
      {
        "name": "Peanut",
        "character": "The Villain",
        "img": "/posters/poster_23.png"
      },
      {
        "name": "Furball",
        "character": "The Sleeper",
        "img": "/posters/poster_27.png"
      },
      {
        "name": "Chubby",
        "character": "The Seed Hoarder",
        "img": "/posters/poster_4.png"
      },
      {
        "name": "Sir Fluffs",
        "character": "The Hero",
        "img": "/posters/poster_34.png"
      },
      {
        "name": "Cheeks",
        "character": "The Hero",
        "img": "/posters/poster_35.png"
      },
      {
        "name": "Muffin",
        "character": "The Biter",
        "img": "/posters/poster_16.png"
      },
      {
        "name": "Teddy",
        "character": "The Wise Elder",
        "img": "/posters/poster_21.png"
      },
      {
        "name": "Buster",
        "character": "The Biter",
        "img": "/posters/poster_25.png"
      },
      {
        "name": "Pumpkin",
        "character": "The Mastermind",
        "img": "/posters/poster_6.png"
      },
      {
        "name": "Nugget",
        "character": "The Escape Artist",
        "img": "/posters/poster_6.png"
      },
      {
        "name": "Oreo",
        "character": "The Biter",
        "img": "/posters/poster_26.png"
      }
    ],
    "director": "Christopher Nolan",
    "synopsis": "In a world where the wheel never stops turning, one hamster must face the ultimate challenge. Experience 'Fuzz Ball' like never before in this epic drama tale of survival, seeds, and late-night running.",
    "genres": [
      "Drama",
      "Animation"
    ],
    "mood": [
      "Heartwarming",
      "Furry"
    ],
    "trailer_concept": "[0:00-0:10] A moody, cinematic opening. Sunlight filters through the cage bars, casting long shadows. A heartwarming atmosphere.\n\n[0:10-0:20] The hamster sits motionless on the wheel, contemplating the meaning of the spinning cycle. Emotional string music swells.\n\n[0:20-0:30] A tear-jerking climax as the hamster finally reaches the top of the ramp. Fade to white with the title: 'Fuzz Ball'."
  },
  "16": {
    "cast": [
      {
        "name": "Oreo",
        "character": "The Cage Climber",
        "img": "/posters/poster_34.png"
      },
      {
        "name": "Squeaks",
        "character": "The Lookout",
        "img": "/posters/poster_11.png"
      },
      {
        "name": "Furball",
        "character": "The Wheel Runner",
        "img": "/posters/poster_28.png"
      },
      {
        "name": "Pumpkin",
        "character": "The Lookout",
        "img": "/posters/poster_33.png"
      },
      {
        "name": "Dusty",
        "character": "The Treat Thief",
        "img": "/posters/poster_18.png"
      },
      {
        "name": "Nugget",
        "character": "The Squeaker",
        "img": "/posters/poster_26.png"
      },
      {
        "name": "Sir Fluffs",
        "character": "The Hero",
        "img": "/posters/poster_23.png"
      },
      {
        "name": "Pompom",
        "character": "The Seed Hoarder",
        "img": "/posters/poster_5.png"
      },
      {
        "name": "Hazel",
        "character": "The Tunnel Navigator",
        "img": "/posters/poster_15.png"
      },
      {
        "name": "Teddy",
        "character": "The Hero",
        "img": "/posters/poster_51.png"
      },
      {
        "name": "Barnaby",
        "character": "The Wheel Runner",
        "img": "/posters/poster_35.png"
      },
      {
        "name": "Muffin",
        "character": "The Squeaker",
        "img": "/posters/poster_30.png"
      },
      {
        "name": "Nibbles",
        "character": "The Treat Thief",
        "img": "/posters/poster_38.png"
      }
    ],
    "director": "Wes Anderson",
    "synopsis": "In a world where the wheel never stops turning, one hamster must face the ultimate challenge. Experience 'Cage Break' like never before in this epic drama tale of survival, seeds, and late-night running.",
    "genres": [
      "Drama",
      "Adventure"
    ],
    "mood": [
      "Heartwarming",
      "Heartwarming"
    ],
    "trailer_concept": "[0:00-0:10] A moody, cinematic opening. Sunlight filters through the cage bars, casting long shadows. A heartwarming atmosphere.\n\n[0:10-0:20] The hamster sits motionless on the wheel, contemplating the meaning of the spinning cycle. Emotional string music swells.\n\n[0:20-0:30] A tear-jerking climax as the hamster finally reaches the top of the ramp. Fade to white with the title: 'Cage Break'."
  },
  "17": {
    "cast": [
      {
        "name": "Waffles",
        "character": "The Sidekick",
        "img": "/posters/poster_23.png"
      },
      {
        "name": "Muffin",
        "character": "The Sleeper",
        "img": "/posters/poster_35.png"
      },
      {
        "name": "Pumpkin",
        "character": "The Sleeper",
        "img": "/posters/poster_30.png"
      },
      {
        "name": "Snickers",
        "character": "The Wheel Runner",
        "img": "/posters/poster_37.png"
      },
      {
        "name": "Chubby",
        "character": "The Wheel Runner",
        "img": "/posters/poster_12.png"
      },
      {
        "name": "Dusty",
        "character": "The Cage Climber",
        "img": "/posters/poster_22.png"
      },
      {
        "name": "Barnaby",
        "character": "The Sidekick",
        "img": "/posters/poster_39.png"
      },
      {
        "name": "Buttercup",
        "character": "The Seed Hoarder",
        "img": "/posters/poster_41.png"
      },
      {
        "name": "Sir Fluffs",
        "character": "The Treat Thief",
        "img": "/posters/poster_30.png"
      },
      {
        "name": "Mocha",
        "character": "The Biter",
        "img": "/posters/poster_27.png"
      },
      {
        "name": "Coco",
        "character": "The Villain",
        "img": "/posters/poster_19.png"
      }
    ],
    "director": "Greta Gerwig",
    "synopsis": "In a world where the wheel never stops turning, one hamster must face the ultimate challenge. Experience 'Squeak' like never before in this epic drama tale of survival, seeds, and late-night running.",
    "genres": [
      "Drama",
      "Family"
    ],
    "mood": [
      "Furry",
      "Exciting"
    ],
    "trailer_concept": "[0:00-0:10] A moody, cinematic opening. Sunlight filters through the cage bars, casting long shadows. A furry atmosphere.\n\n[0:10-0:20] The hamster sits motionless on the wheel, contemplating the meaning of the spinning cycle. Emotional string music swells.\n\n[0:20-0:30] A tear-jerking climax as the hamster finally reaches the top of the ramp. Fade to white with the title: 'Squeak'."
  },
  "18": {
    "cast": [
      {
        "name": "Sir Fluffs",
        "character": "The Hero",
        "img": "/posters/poster_51.png"
      },
      {
        "name": "Pumpkin",
        "character": "The Mastermind",
        "img": "/posters/poster_17.png"
      },
      {
        "name": "Nibbles",
        "character": "The Lookout",
        "img": "/posters/poster_12.png"
      },
      {
        "name": "Oreo",
        "character": "The Villain",
        "img": "/posters/poster_4.png"
      },
      {
        "name": "Mocha",
        "character": "The Lookout",
        "img": "/posters/poster_32.png"
      },
      {
        "name": "Squeaks",
        "character": "The Seed Hoarder",
        "img": "/posters/poster_10.png"
      },
      {
        "name": "Whiskers",
        "character": "The Treat Thief",
        "img": "/posters/poster_19.png"
      },
      {
        "name": "Buttercup",
        "character": "The Sleeper",
        "img": "/posters/poster_34.png"
      },
      {
        "name": "Peanut",
        "character": "The Squeaker",
        "img": "/posters/poster_8.png"
      },
      {
        "name": "Teddy",
        "character": "The Sidekick",
        "img": "/posters/poster_35.png"
      }
    ],
    "director": "Greta Gerwig",
    "synopsis": "In a world where the wheel never stops turning, one hamster must face the ultimate challenge. Experience 'The Burrow' like never before in this epic drama tale of survival, seeds, and late-night running.",
    "genres": [
      "Drama",
      "Family"
    ],
    "mood": [
      "Furry",
      "Fast-Paced"
    ],
    "trailer_concept": "[0:00-0:10] A moody, cinematic opening. Sunlight filters through the cage bars, casting long shadows. A furry atmosphere.\n\n[0:10-0:20] The hamster sits motionless on the wheel, contemplating the meaning of the spinning cycle. Emotional string music swells.\n\n[0:20-0:30] A tear-jerking climax as the hamster finally reaches the top of the ramp. Fade to white with the title: 'The Burrow'."
  },
  "19": {
    "cast": [
      {
        "name": "Dusty",
        "character": "The Sidekick",
        "img": "/posters/poster_32.png"
      },
      {
        "name": "Pompom",
        "character": "The Squeaker",
        "img": "/posters/poster_7.png"
      },
      {
        "name": "Mocha",
        "character": "The Treat Thief",
        "img": "/posters/poster_22.png"
      },
      {
        "name": "Whiskers",
        "character": "The Mastermind",
        "img": "/posters/poster_2.png"
      },
      {
        "name": "Bean",
        "character": "The Cage Climber",
        "img": "/posters/poster_21.png"
      },
      {
        "name": "Coco",
        "character": "The Wheel Runner",
        "img": "/posters/poster_32.png"
      },
      {
        "name": "Squeaks",
        "character": "The Tunnel Navigator",
        "img": "/posters/poster_26.png"
      },
      {
        "name": "Oreo",
        "character": "The Sleeper",
        "img": "/posters/poster_16.png"
      },
      {
        "name": "Pumpkin",
        "character": "The Treat Thief",
        "img": "/posters/poster_6.png"
      },
      {
        "name": "Hazel",
        "character": "The Wheel Runner",
        "img": "/posters/poster_22.png"
      },
      {
        "name": "Chestnut",
        "character": "The Mastermind",
        "img": "/posters/poster_22.png"
      },
      {
        "name": "Snickers",
        "character": "The Lookout",
        "img": "/posters/poster_38.png"
      },
      {
        "name": "Biscuit",
        "character": "The Lookout",
        "img": "/posters/poster_40.png"
      }
    ],
    "director": "Christopher Nolan",
    "synopsis": "In a world where the wheel never stops turning, one hamster must face the ultimate challenge. Experience 'Life in the Tubes' like never before in this epic documentary tale of survival, seeds, and late-night running.",
    "genres": [
      "Documentary",
      "Animation"
    ],
    "mood": [
      "Squeaky",
      "Squeaky"
    ],
    "trailer_concept": "[0:00-0:10] Sweeping orchestral score. Macro shots of wood shavings and a pristine food bowl. 'Explore the unseen world...'\n\n[0:10-0:20] Slow, majestic footage of the hamster grooming its whiskers. A deep, squeaky voiceover explains the stakes of the nocturnal life.\n\n[0:20-0:30] A profound look into the dark, glittering eyes of the rodent. 'Discover Life in the Tubes. Streaming this Fall.'"
  },
  "20": {
    "cast": [
      {
        "name": "Biscuit",
        "character": "The Mastermind",
        "img": "/posters/poster_34.png"
      },
      {
        "name": "Coco",
        "character": "The Tunnel Navigator",
        "img": "/posters/poster_49.png"
      },
      {
        "name": "Teddy",
        "character": "The Sleeper",
        "img": "/posters/poster_39.png"
      },
      {
        "name": "Buster",
        "character": "The Wheel Runner",
        "img": "/posters/poster_28.png"
      },
      {
        "name": "Buttercup",
        "character": "The Hero",
        "img": "/posters/poster_25.png"
      },
      {
        "name": "Marshmallow",
        "character": "The Wise Elder",
        "img": "/posters/poster_41.png"
      },
      {
        "name": "Cheeks",
        "character": "The Sidekick",
        "img": "/posters/poster_2.png"
      },
      {
        "name": "Oreo",
        "character": "The Hero",
        "img": "/posters/poster_26.png"
      }
    ],
    "director": "Christopher Nolan",
    "synopsis": "In a world where the wheel never stops turning, one hamster must face the ultimate challenge. Experience 'Seed Gatherers' like never before in this epic documentary tale of survival, seeds, and late-night running.",
    "genres": [
      "Documentary",
      "Adventure"
    ],
    "mood": [
      "Furry",
      "Furry"
    ],
    "trailer_concept": "[0:00-0:10] Sweeping orchestral score. Macro shots of wood shavings and a pristine food bowl. 'Explore the unseen world...'\n\n[0:10-0:20] Slow, majestic footage of the hamster grooming its whiskers. A deep, furry voiceover explains the stakes of the nocturnal life.\n\n[0:20-0:30] A profound look into the dark, glittering eyes of the rodent. 'Discover Seed Gatherers. Streaming this Fall.'"
  },
  "21": {
    "cast": [
      {
        "name": "Sir Fluffs",
        "character": "The Escape Artist",
        "img": "/posters/poster_43.png"
      },
      {
        "name": "Bean",
        "character": "The Sleeper",
        "img": "/posters/poster_13.png"
      },
      {
        "name": "Cheeks",
        "character": "The Wheel Runner",
        "img": "/posters/poster_12.png"
      },
      {
        "name": "Marshmallow",
        "character": "The Wheel Runner",
        "img": "/posters/poster_6.png"
      },
      {
        "name": "Squeaks",
        "character": "The Tunnel Navigator",
        "img": "/posters/poster_16.png"
      },
      {
        "name": "Dusty",
        "character": "The Wise Elder",
        "img": "/posters/poster_41.png"
      },
      {
        "name": "Pip",
        "character": "The Seed Hoarder",
        "img": "/posters/poster_29.png"
      },
      {
        "name": "Chubby",
        "character": "The Cage Climber",
        "img": "/posters/poster_24.png"
      }
    ],
    "director": "Greta Gerwig",
    "synopsis": "In a world where the wheel never stops turning, one hamster must face the ultimate challenge. Experience 'Beyond the Wheel' like never before in this epic documentary tale of survival, seeds, and late-night running.",
    "genres": [
      "Documentary",
      "Animation"
    ],
    "mood": [
      "Fast-Paced",
      "Squeaky"
    ],
    "trailer_concept": "[0:00-0:10] Sweeping orchestral score. Macro shots of wood shavings and a pristine food bowl. 'Explore the unseen world...'\n\n[0:10-0:20] Slow, majestic footage of the hamster grooming its whiskers. A deep, fast-paced voiceover explains the stakes of the nocturnal life.\n\n[0:20-0:30] A profound look into the dark, glittering eyes of the rodent. 'Discover Beyond the Wheel. Streaming this Fall.'"
  },
  "22": {
    "cast": [
      {
        "name": "Oreo",
        "character": "The Seed Hoarder",
        "img": "/posters/poster_40.png"
      },
      {
        "name": "Snickers",
        "character": "The Wheel Runner",
        "img": "/posters/poster_16.png"
      },
      {
        "name": "Marshmallow",
        "character": "The Tunnel Navigator",
        "img": "/posters/poster_24.png"
      },
      {
        "name": "Teddy",
        "character": "The Cage Climber",
        "img": "/posters/poster_5.png"
      },
      {
        "name": "Dusty",
        "character": "The Wise Elder",
        "img": "/posters/poster_7.png"
      },
      {
        "name": "Biscuit",
        "character": "The Sidekick",
        "img": "/posters/poster_5.png"
      },
      {
        "name": "Chubby",
        "character": "The Wise Elder",
        "img": "/posters/poster_29.png"
      },
      {
        "name": "Chestnut",
        "character": "The Cage Climber",
        "img": "/posters/poster_4.png"
      },
      {
        "name": "Furball",
        "character": "The Cage Climber",
        "img": "/posters/poster_9.png"
      }
    ],
    "director": "Greta Gerwig",
    "synopsis": "In a world where the wheel never stops turning, one hamster must face the ultimate challenge. Experience 'Nocturnal Habits' like never before in this epic documentary tale of survival, seeds, and late-night running.",
    "genres": [
      "Documentary",
      "Family"
    ],
    "mood": [
      "Furry",
      "Fast-Paced"
    ],
    "trailer_concept": "[0:00-0:10] Sweeping orchestral score. Macro shots of wood shavings and a pristine food bowl. 'Explore the unseen world...'\n\n[0:10-0:20] Slow, majestic footage of the hamster grooming its whiskers. A deep, furry voiceover explains the stakes of the nocturnal life.\n\n[0:20-0:30] A profound look into the dark, glittering eyes of the rodent. 'Discover Nocturnal Habits. Streaming this Fall.'"
  },
  "23": {
    "cast": [
      {
        "name": "Marshmallow",
        "character": "The Treat Thief",
        "img": "/posters/poster_20.png"
      },
      {
        "name": "Coco",
        "character": "The Hero",
        "img": "/posters/poster_25.png"
      },
      {
        "name": "Cheeks",
        "character": "The Wheel Runner",
        "img": "/posters/poster_25.png"
      },
      {
        "name": "Buttercup",
        "character": "The Tunnel Navigator",
        "img": "/posters/poster_51.png"
      },
      {
        "name": "Muffin",
        "character": "The Sidekick",
        "img": "/posters/poster_29.png"
      },
      {
        "name": "Hazel",
        "character": "The Cage Climber",
        "img": "/posters/poster_24.png"
      },
      {
        "name": "Bean",
        "character": "The Escape Artist",
        "img": "/posters/poster_28.png"
      },
      {
        "name": "Furball",
        "character": "The Treat Thief",
        "img": "/posters/poster_1.png"
      },
      {
        "name": "Nugget",
        "character": "The Cage Climber",
        "img": "/posters/poster_7.png"
      }
    ],
    "director": "Steven Spielberg",
    "synopsis": "In a world where the wheel never stops turning, one hamster must face the ultimate challenge. Experience 'The Escape Artist' like never before in this epic documentary tale of survival, seeds, and late-night running.",
    "genres": [
      "Documentary",
      "Family"
    ],
    "mood": [
      "Furry",
      "Heartwarming"
    ],
    "trailer_concept": "[0:00-0:10] Sweeping orchestral score. Macro shots of wood shavings and a pristine food bowl. 'Explore the unseen world...'\n\n[0:10-0:20] Slow, majestic footage of the hamster grooming its whiskers. A deep, furry voiceover explains the stakes of the nocturnal life.\n\n[0:20-0:30] A profound look into the dark, glittering eyes of the rodent. 'Discover The Escape Artist. Streaming this Fall.'"
  },
  "24": {
    "cast": [
      {
        "name": "Furball",
        "character": "The Sleeper",
        "img": "/posters/poster_29.png"
      },
      {
        "name": "Teddy",
        "character": "The Villain",
        "img": "/posters/poster_14.png"
      },
      {
        "name": "Hazel",
        "character": "The Escape Artist",
        "img": "/posters/poster_9.png"
      },
      {
        "name": "Cheeks",
        "character": "The Villain",
        "img": "/posters/poster_31.png"
      },
      {
        "name": "Sir Fluffs",
        "character": "The Biter",
        "img": "/posters/poster_3.png"
      },
      {
        "name": "Bean",
        "character": "The Seed Hoarder",
        "img": "/posters/poster_6.png"
      },
      {
        "name": "Nibbles",
        "character": "The Villain",
        "img": "/posters/poster_41.png"
      },
      {
        "name": "Chestnut",
        "character": "The Lookout",
        "img": "/posters/poster_10.png"
      },
      {
        "name": "Peanut",
        "character": "The Treat Thief",
        "img": "/posters/poster_33.png"
      },
      {
        "name": "Snickers",
        "character": "The Wheel Runner",
        "img": "/posters/poster_28.png"
      },
      {
        "name": "Squeaks",
        "character": "The Sidekick",
        "img": "/posters/poster_39.png"
      },
      {
        "name": "Barnaby",
        "character": "The Villain",
        "img": "/posters/poster_34.png"
      },
      {
        "name": "Oreo",
        "character": "The Hero",
        "img": "/posters/poster_27.png"
      }
    ],
    "director": "Wes Anderson",
    "synopsis": "In a world where the wheel never stops turning, one hamster must face the ultimate challenge. Experience 'Cheeks of Steel' like never before in this epic documentary tale of survival, seeds, and late-night running.",
    "genres": [
      "Documentary",
      "Animation"
    ],
    "mood": [
      "Exciting",
      "Squeaky"
    ],
    "trailer_concept": "[0:00-0:10] Sweeping orchestral score. Macro shots of wood shavings and a pristine food bowl. 'Explore the unseen world...'\n\n[0:10-0:20] Slow, majestic footage of the hamster grooming its whiskers. A deep, exciting voiceover explains the stakes of the nocturnal life.\n\n[0:20-0:30] A profound look into the dark, glittering eyes of the rodent. 'Discover Cheeks of Steel. Streaming this Fall.'"
  },
  "25": {
    "cast": [
      {
        "name": "Nugget",
        "character": "The Hero",
        "img": "/posters/poster_29.png"
      },
      {
        "name": "Sir Fluffs",
        "character": "The Sidekick",
        "img": "/posters/poster_16.png"
      },
      {
        "name": "Paws",
        "character": "The Tunnel Navigator",
        "img": "/posters/poster_4.png"
      },
      {
        "name": "Chubby",
        "character": "The Seed Hoarder",
        "img": "/posters/poster_17.png"
      },
      {
        "name": "Cashew",
        "character": "The Lookout",
        "img": "/posters/poster_33.png"
      },
      {
        "name": "Muffin",
        "character": "The Sidekick",
        "img": "/posters/poster_34.png"
      },
      {
        "name": "Snickers",
        "character": "The Squeaker",
        "img": "/posters/poster_34.png"
      },
      {
        "name": "Furball",
        "character": "The Tunnel Navigator",
        "img": "/posters/poster_51.png"
      },
      {
        "name": "Biscuit",
        "character": "The Sleeper",
        "img": "/posters/poster_36.png"
      }
    ],
    "director": "Wes Anderson",
    "synopsis": "In a world where the wheel never stops turning, one hamster must face the ultimate challenge. Experience 'Squeaky Clean' like never before in this epic comedy tale of survival, seeds, and late-night running.",
    "genres": [
      "Comedy",
      "Animation"
    ],
    "mood": [
      "Intense",
      "Fast-Paced"
    ],
    "trailer_concept": "[0:00-0:10] Upbeat, quirky music. A chubby hamster tries to fit an impossibly large carrot into its cheek and falls over.\n\n[0:10-0:20] The narrator says, 'This summer... getting out of the cage is just the beginning.' Montage of hilarious slip-ups and wheel fails.\n\n[0:20-0:30] The hamsters form a towering pyramid to reach the latch. It collapses in a squeaky mess. Title card: 'Squeaky Clean'."
  },
  "26": {
    "cast": [
      {
        "name": "Dusty",
        "character": "The Lookout",
        "img": "/posters/poster_13.png"
      },
      {
        "name": "Sir Fluffs",
        "character": "The Escape Artist",
        "img": "/posters/poster_49.png"
      },
      {
        "name": "Mocha",
        "character": "The Sleeper",
        "img": "/posters/poster_31.png"
      },
      {
        "name": "Hazel",
        "character": "The Sidekick",
        "img": "/posters/poster_40.png"
      },
      {
        "name": "Nibbles",
        "character": "The Lookout",
        "img": "/posters/poster_35.png"
      },
      {
        "name": "Marshmallow",
        "character": "The Lookout",
        "img": "/posters/poster_19.png"
      },
      {
        "name": "Oreo",
        "character": "The Wheel Runner",
        "img": "/posters/poster_27.png"
      },
      {
        "name": "Paws",
        "character": "The Lookout",
        "img": "/posters/poster_17.png"
      },
      {
        "name": "Coco",
        "character": "The Hero",
        "img": "/posters/poster_36.png"
      },
      {
        "name": "Furball",
        "character": "The Biter",
        "img": "/posters/poster_49.png"
      },
      {
        "name": "Pompom",
        "character": "The Treat Thief",
        "img": "/posters/poster_39.png"
      }
    ],
    "director": "Steven Spielberg",
    "synopsis": "In a world where the wheel never stops turning, one hamster must face the ultimate challenge. Experience 'Drop the Seed' like never before in this epic comedy tale of survival, seeds, and late-night running.",
    "genres": [
      "Comedy",
      "Animation"
    ],
    "mood": [
      "Fast-Paced",
      "Intense"
    ],
    "trailer_concept": "[0:00-0:10] Upbeat, quirky music. A chubby hamster tries to fit an impossibly large carrot into its cheek and falls over.\n\n[0:10-0:20] The narrator says, 'This summer... getting out of the cage is just the beginning.' Montage of hilarious slip-ups and wheel fails.\n\n[0:20-0:30] The hamsters form a towering pyramid to reach the latch. It collapses in a squeaky mess. Title card: 'Drop the Seed'."
  },
  "27": {
    "cast": [
      {
        "name": "Cheeks",
        "character": "The Hero",
        "img": "/posters/poster_4.png"
      },
      {
        "name": "Snickers",
        "character": "The Hero",
        "img": "/posters/poster_33.png"
      },
      {
        "name": "Teddy",
        "character": "The Cage Climber",
        "img": "/posters/poster_28.png"
      },
      {
        "name": "Waffles",
        "character": "The Seed Hoarder",
        "img": "/posters/poster_31.png"
      },
      {
        "name": "Peanut",
        "character": "The Wise Elder",
        "img": "/posters/poster_17.png"
      },
      {
        "name": "Paws",
        "character": "The Biter",
        "img": "/posters/poster_33.png"
      },
      {
        "name": "Mocha",
        "character": "The Hero",
        "img": "/posters/poster_8.png"
      },
      {
        "name": "Coco",
        "character": "The Sidekick",
        "img": "/posters/poster_13.png"
      },
      {
        "name": "Marshmallow",
        "character": "The Squeaker",
        "img": "/posters/poster_40.png"
      },
      {
        "name": "Pumpkin",
        "character": "The Wheel Runner",
        "img": "/posters/poster_27.png"
      },
      {
        "name": "Sir Fluffs",
        "character": "The Sleeper",
        "img": "/posters/poster_14.png"
      }
    ],
    "director": "Steven Spielberg",
    "synopsis": "In a world where the wheel never stops turning, one hamster must face the ultimate challenge. Experience 'Hamster Dance' like never before in this epic comedy tale of survival, seeds, and late-night running.",
    "genres": [
      "Comedy",
      "Adventure"
    ],
    "mood": [
      "Squeaky",
      "Furry"
    ],
    "trailer_concept": "[0:00-0:10] Upbeat, quirky music. A chubby hamster tries to fit an impossibly large carrot into its cheek and falls over.\n\n[0:10-0:20] The narrator says, 'This summer... getting out of the cage is just the beginning.' Montage of hilarious slip-ups and wheel fails.\n\n[0:20-0:30] The hamsters form a towering pyramid to reach the latch. It collapses in a squeaky mess. Title card: 'Hamster Dance'."
  },
  "28": {
    "cast": [
      {
        "name": "Snickers",
        "character": "The Squeaker",
        "img": "/posters/poster_13.png"
      },
      {
        "name": "Barnaby",
        "character": "The Sidekick",
        "img": "/posters/poster_22.png"
      },
      {
        "name": "Dusty",
        "character": "The Wise Elder",
        "img": "/posters/poster_43.png"
      },
      {
        "name": "Teddy",
        "character": "The Lookout",
        "img": "/posters/poster_40.png"
      },
      {
        "name": "Pompom",
        "character": "The Treat Thief",
        "img": "/posters/poster_30.png"
      },
      {
        "name": "Waffles",
        "character": "The Tunnel Navigator",
        "img": "/posters/poster_19.png"
      },
      {
        "name": "Marshmallow",
        "character": "The Cage Climber",
        "img": "/posters/poster_28.png"
      },
      {
        "name": "Coco",
        "character": "The Lookout",
        "img": "/posters/poster_51.png"
      },
      {
        "name": "Buttercup",
        "character": "The Escape Artist",
        "img": "/posters/poster_7.png"
      },
      {
        "name": "Mocha",
        "character": "The Escape Artist",
        "img": "/posters/poster_10.png"
      },
      {
        "name": "Hazel",
        "character": "The Treat Thief",
        "img": "/posters/poster_18.png"
      }
    ],
    "director": "Greta Gerwig",
    "synopsis": "In a world where the wheel never stops turning, one hamster must face the ultimate challenge. Experience 'Stuck in the Tube' like never before in this epic comedy tale of survival, seeds, and late-night running.",
    "genres": [
      "Comedy",
      "Animation"
    ],
    "mood": [
      "Furry",
      "Fast-Paced"
    ],
    "trailer_concept": "[0:00-0:10] Upbeat, quirky music. A chubby hamster tries to fit an impossibly large carrot into its cheek and falls over.\n\n[0:10-0:20] The narrator says, 'This summer... getting out of the cage is just the beginning.' Montage of hilarious slip-ups and wheel fails.\n\n[0:20-0:30] The hamsters form a towering pyramid to reach the latch. It collapses in a squeaky mess. Title card: 'Stuck in the Tube'."
  },
  "29": {
    "cast": [
      {
        "name": "Dusty",
        "character": "The Villain",
        "img": "/posters/poster_21.png"
      },
      {
        "name": "Cashew",
        "character": "The Biter",
        "img": "/posters/poster_27.png"
      },
      {
        "name": "Buster",
        "character": "The Wise Elder",
        "img": "/posters/poster_16.png"
      },
      {
        "name": "Sir Fluffs",
        "character": "The Tunnel Navigator",
        "img": "/posters/poster_26.png"
      },
      {
        "name": "Pompom",
        "character": "The Wise Elder",
        "img": "/posters/poster_39.png"
      },
      {
        "name": "Teddy",
        "character": "The Wheel Runner",
        "img": "/posters/poster_40.png"
      },
      {
        "name": "Squeaks",
        "character": "The Sidekick",
        "img": "/posters/poster_23.png"
      },
      {
        "name": "Chubby",
        "character": "The Hero",
        "img": "/posters/poster_16.png"
      },
      {
        "name": "Barnaby",
        "character": "The Wise Elder",
        "img": "/posters/poster_11.png"
      },
      {
        "name": "Furball",
        "character": "The Wise Elder",
        "img": "/posters/poster_21.png"
      }
    ],
    "director": "Greta Gerwig",
    "synopsis": "In a world where the wheel never stops turning, one hamster must face the ultimate challenge. Experience 'Wheel Fail' like never before in this epic comedy tale of survival, seeds, and late-night running.",
    "genres": [
      "Comedy",
      "Animation"
    ],
    "mood": [
      "Fast-Paced",
      "Fast-Paced"
    ],
    "trailer_concept": "[0:00-0:10] Upbeat, quirky music. A chubby hamster tries to fit an impossibly large carrot into its cheek and falls over.\n\n[0:10-0:20] The narrator says, 'This summer... getting out of the cage is just the beginning.' Montage of hilarious slip-ups and wheel fails.\n\n[0:20-0:30] The hamsters form a towering pyramid to reach the latch. It collapses in a squeaky mess. Title card: 'Wheel Fail'."
  },
  "30": {
    "cast": [
      {
        "name": "Dusty",
        "character": "The Mastermind",
        "img": "/posters/poster_14.png"
      },
      {
        "name": "Barnaby",
        "character": "The Biter",
        "img": "/posters/poster_33.png"
      },
      {
        "name": "Peanut",
        "character": "The Cage Climber",
        "img": "/posters/poster_20.png"
      },
      {
        "name": "Furball",
        "character": "The Mastermind",
        "img": "/posters/poster_16.png"
      },
      {
        "name": "Pip",
        "character": "The Villain",
        "img": "/posters/poster_40.png"
      },
      {
        "name": "Cheeks",
        "character": "The Mastermind",
        "img": "/posters/poster_5.png"
      },
      {
        "name": "Coco",
        "character": "The Villain",
        "img": "/posters/poster_41.png"
      },
      {
        "name": "Sir Fluffs",
        "character": "The Seed Hoarder",
        "img": "/posters/poster_12.png"
      },
      {
        "name": "Whiskers",
        "character": "The Lookout",
        "img": "/posters/poster_22.png"
      },
      {
        "name": "Marshmallow",
        "character": "The Seed Hoarder",
        "img": "/posters/poster_29.png"
      },
      {
        "name": "Biscuit",
        "character": "The Squeaker",
        "img": "/posters/poster_10.png"
      },
      {
        "name": "Chubby",
        "character": "The Tunnel Navigator",
        "img": "/posters/poster_8.png"
      }
    ],
    "director": "Greta Gerwig",
    "synopsis": "In a world where the wheel never stops turning, one hamster must face the ultimate challenge. Experience 'Bite Me' like never before in this epic comedy tale of survival, seeds, and late-night running.",
    "genres": [
      "Comedy",
      "Family"
    ],
    "mood": [
      "Fast-Paced",
      "Fast-Paced"
    ],
    "trailer_concept": "[0:00-0:10] Upbeat, quirky music. A chubby hamster tries to fit an impossibly large carrot into its cheek and falls over.\n\n[0:10-0:20] The narrator says, 'This summer... getting out of the cage is just the beginning.' Montage of hilarious slip-ups and wheel fails.\n\n[0:20-0:30] The hamsters form a towering pyramid to reach the latch. It collapses in a squeaky mess. Title card: 'Bite Me'."
  },
  "31": {
    "cast": [
      {
        "name": "Biscuit",
        "character": "The Sleeper",
        "img": "/posters/poster_26.png"
      },
      {
        "name": "Cashew",
        "character": "The Villain",
        "img": "/posters/poster_18.png"
      },
      {
        "name": "Peanut",
        "character": "The Seed Hoarder",
        "img": "/posters/poster_37.png"
      },
      {
        "name": "Dusty",
        "character": "The Biter",
        "img": "/posters/poster_21.png"
      },
      {
        "name": "Mocha",
        "character": "The Seed Hoarder",
        "img": "/posters/poster_10.png"
      },
      {
        "name": "Chubby",
        "character": "The Biter",
        "img": "/posters/poster_51.png"
      },
      {
        "name": "Marshmallow",
        "character": "The Mastermind",
        "img": "/posters/poster_9.png"
      },
      {
        "name": "Paws",
        "character": "The Wise Elder",
        "img": "/posters/poster_1.png"
      },
      {
        "name": "Pompom",
        "character": "The Wise Elder",
        "img": "/posters/poster_23.png"
      },
      {
        "name": "Sir Fluffs",
        "character": "The Tunnel Navigator",
        "img": "/posters/poster_21.png"
      },
      {
        "name": "Nugget",
        "character": "The Lookout",
        "img": "/posters/poster_13.png"
      }
    ],
    "director": "Greta Gerwig",
    "synopsis": "In a world where the wheel never stops turning, one hamster must face the ultimate challenge. Experience 'Space Hamster' like never before in this epic sci-fi tale of survival, seeds, and late-night running.",
    "genres": [
      "Sci-Fi",
      "Adventure"
    ],
    "mood": [
      "Exciting",
      "Exciting"
    ],
    "trailer_concept": "[0:00-0:10] Wide panning shot of a neon-lit, futuristic cage. A glowing water bottle drips in slow motion. 'Space Hamster' appears on screen.\n\n[0:10-0:20] Close-up of our majestic hamster hero looking out of a plastic tube into the vast unknown, exciting synth music building.\n\n[0:20-0:30] Rapid montage: running on a hyper-drive wheel, dodging laser pointers, and a final epic leap into the bedding. Fade to black."
  },
  "32": {
    "cast": [
      {
        "name": "Paws",
        "character": "The Villain",
        "img": "/posters/poster_49.png"
      },
      {
        "name": "Pompom",
        "character": "The Wise Elder",
        "img": "/posters/poster_34.png"
      },
      {
        "name": "Squeaks",
        "character": "The Lookout",
        "img": "/posters/poster_4.png"
      },
      {
        "name": "Biscuit",
        "character": "The Hero",
        "img": "/posters/poster_18.png"
      },
      {
        "name": "Chestnut",
        "character": "The Hero",
        "img": "/posters/poster_30.png"
      },
      {
        "name": "Barnaby",
        "character": "The Hero",
        "img": "/posters/poster_22.png"
      },
      {
        "name": "Cashew",
        "character": "The Cage Climber",
        "img": "/posters/poster_15.png"
      },
      {
        "name": "Pumpkin",
        "character": "The Wise Elder",
        "img": "/posters/poster_28.png"
      },
      {
        "name": "Buster",
        "character": "The Treat Thief",
        "img": "/posters/poster_1.png"
      },
      {
        "name": "Coco",
        "character": "The Escape Artist",
        "img": "/posters/poster_49.png"
      },
      {
        "name": "Whiskers",
        "character": "The Lookout",
        "img": "/posters/poster_12.png"
      },
      {
        "name": "Nugget",
        "character": "The Wise Elder",
        "img": "/posters/poster_40.png"
      },
      {
        "name": "Furball",
        "character": "The Squeaker",
        "img": "/posters/poster_21.png"
      }
    ],
    "director": "Christopher Nolan",
    "synopsis": "In a world where the wheel never stops turning, one hamster must face the ultimate challenge. Experience 'The Galactic Cage' like never before in this epic sci-fi tale of survival, seeds, and late-night running.",
    "genres": [
      "Sci-Fi",
      "Family"
    ],
    "mood": [
      "Furry",
      "Fast-Paced"
    ],
    "trailer_concept": "[0:00-0:10] Wide panning shot of a neon-lit, futuristic cage. A glowing water bottle drips in slow motion. 'The Galactic Cage' appears on screen.\n\n[0:10-0:20] Close-up of our majestic hamster hero looking out of a plastic tube into the vast unknown, furry synth music building.\n\n[0:20-0:30] Rapid montage: running on a hyper-drive wheel, dodging laser pointers, and a final epic leap into the bedding. Fade to black."
  },
  "33": {
    "cast": [
      {
        "name": "Marshmallow",
        "character": "The Squeaker",
        "img": "/posters/poster_2.png"
      },
      {
        "name": "Hazel",
        "character": "The Seed Hoarder",
        "img": "/posters/poster_30.png"
      },
      {
        "name": "Snickers",
        "character": "The Cage Climber",
        "img": "/posters/poster_32.png"
      },
      {
        "name": "Peanut",
        "character": "The Treat Thief",
        "img": "/posters/poster_51.png"
      },
      {
        "name": "Paws",
        "character": "The Seed Hoarder",
        "img": "/posters/poster_12.png"
      },
      {
        "name": "Oreo",
        "character": "The Biter",
        "img": "/posters/poster_13.png"
      },
      {
        "name": "Cashew",
        "character": "The Villain",
        "img": "/posters/poster_28.png"
      },
      {
        "name": "Barnaby",
        "character": "The Escape Artist",
        "img": "/posters/poster_7.png"
      },
      {
        "name": "Pumpkin",
        "character": "The Squeaker",
        "img": "/posters/poster_38.png"
      },
      {
        "name": "Whiskers",
        "character": "The Sidekick",
        "img": "/posters/poster_43.png"
      },
      {
        "name": "Bean",
        "character": "The Tunnel Navigator",
        "img": "/posters/poster_14.png"
      },
      {
        "name": "Sir Fluffs",
        "character": "The Wheel Runner",
        "img": "/posters/poster_7.png"
      }
    ],
    "director": "Wes Anderson",
    "synopsis": "In a world where the wheel never stops turning, one hamster must face the ultimate challenge. Experience 'Alien Seeds' like never before in this epic sci-fi tale of survival, seeds, and late-night running.",
    "genres": [
      "Sci-Fi",
      "Family"
    ],
    "mood": [
      "Fast-Paced",
      "Furry"
    ],
    "trailer_concept": "[0:00-0:10] Wide panning shot of a neon-lit, futuristic cage. A glowing water bottle drips in slow motion. 'Alien Seeds' appears on screen.\n\n[0:10-0:20] Close-up of our majestic hamster hero looking out of a plastic tube into the vast unknown, fast-paced synth music building.\n\n[0:20-0:30] Rapid montage: running on a hyper-drive wheel, dodging laser pointers, and a final epic leap into the bedding. Fade to black."
  },
  "34": {
    "cast": [
      {
        "name": "Buttercup",
        "character": "The Lookout",
        "img": "/posters/poster_24.png"
      },
      {
        "name": "Hazel",
        "character": "The Wheel Runner",
        "img": "/posters/poster_13.png"
      },
      {
        "name": "Paws",
        "character": "The Squeaker",
        "img": "/posters/poster_39.png"
      },
      {
        "name": "Buster",
        "character": "The Mastermind",
        "img": "/posters/poster_29.png"
      },
      {
        "name": "Whiskers",
        "character": "The Wheel Runner",
        "img": "/posters/poster_13.png"
      },
      {
        "name": "Furball",
        "character": "The Villain",
        "img": "/posters/poster_23.png"
      },
      {
        "name": "Squeaks",
        "character": "The Sidekick",
        "img": "/posters/poster_22.png"
      },
      {
        "name": "Coco",
        "character": "The Biter",
        "img": "/posters/poster_28.png"
      }
    ],
    "director": "Wes Anderson",
    "synopsis": "In a world where the wheel never stops turning, one hamster must face the ultimate challenge. Experience 'Tube Portals' like never before in this epic sci-fi tale of survival, seeds, and late-night running.",
    "genres": [
      "Sci-Fi",
      "Animation"
    ],
    "mood": [
      "Furry",
      "Intense"
    ],
    "trailer_concept": "[0:00-0:10] Wide panning shot of a neon-lit, futuristic cage. A glowing water bottle drips in slow motion. 'Tube Portals' appears on screen.\n\n[0:10-0:20] Close-up of our majestic hamster hero looking out of a plastic tube into the vast unknown, furry synth music building.\n\n[0:20-0:30] Rapid montage: running on a hyper-drive wheel, dodging laser pointers, and a final epic leap into the bedding. Fade to black."
  },
  "35": {
    "cast": [
      {
        "name": "Dusty",
        "character": "The Seed Hoarder",
        "img": "/posters/poster_40.png"
      },
      {
        "name": "Pumpkin",
        "character": "The Wise Elder",
        "img": "/posters/poster_12.png"
      },
      {
        "name": "Bean",
        "character": "The Sleeper",
        "img": "/posters/poster_36.png"
      },
      {
        "name": "Sir Fluffs",
        "character": "The Wise Elder",
        "img": "/posters/poster_23.png"
      },
      {
        "name": "Teddy",
        "character": "The Lookout",
        "img": "/posters/poster_10.png"
      },
      {
        "name": "Chubby",
        "character": "The Hero",
        "img": "/posters/poster_43.png"
      },
      {
        "name": "Pompom",
        "character": "The Lookout",
        "img": "/posters/poster_29.png"
      },
      {
        "name": "Waffles",
        "character": "The Tunnel Navigator",
        "img": "/posters/poster_7.png"
      },
      {
        "name": "Squeaks",
        "character": "The Sidekick",
        "img": "/posters/poster_17.png"
      },
      {
        "name": "Furball",
        "character": "The Villain",
        "img": "/posters/poster_19.png"
      },
      {
        "name": "Nibbles",
        "character": "The Squeaker",
        "img": "/posters/poster_10.png"
      },
      {
        "name": "Hazel",
        "character": "The Seed Hoarder",
        "img": "/posters/poster_40.png"
      },
      {
        "name": "Biscuit",
        "character": "The Tunnel Navigator",
        "img": "/posters/poster_30.png"
      },
      {
        "name": "Barnaby",
        "character": "The Cage Climber",
        "img": "/posters/poster_5.png"
      }
    ],
    "director": "Wes Anderson",
    "synopsis": "In a world where the wheel never stops turning, one hamster must face the ultimate challenge. Experience 'Laser Eyes' like never before in this epic sci-fi tale of survival, seeds, and late-night running.",
    "genres": [
      "Sci-Fi",
      "Family"
    ],
    "mood": [
      "Fast-Paced",
      "Heartwarming"
    ],
    "trailer_concept": "[0:00-0:10] Wide panning shot of a neon-lit, futuristic cage. A glowing water bottle drips in slow motion. 'Laser Eyes' appears on screen.\n\n[0:10-0:20] Close-up of our majestic hamster hero looking out of a plastic tube into the vast unknown, fast-paced synth music building.\n\n[0:20-0:30] Rapid montage: running on a hyper-drive wheel, dodging laser pointers, and a final epic leap into the bedding. Fade to black."
  },
  "36": {
    "cast": [
      {
        "name": "Buttercup",
        "character": "The Sidekick",
        "img": "/posters/poster_16.png"
      },
      {
        "name": "Nugget",
        "character": "The Seed Hoarder",
        "img": "/posters/poster_51.png"
      },
      {
        "name": "Snickers",
        "character": "The Sleeper",
        "img": "/posters/poster_7.png"
      },
      {
        "name": "Pip",
        "character": "The Villain",
        "img": "/posters/poster_2.png"
      },
      {
        "name": "Cashew",
        "character": "The Tunnel Navigator",
        "img": "/posters/poster_37.png"
      },
      {
        "name": "Squeaks",
        "character": "The Escape Artist",
        "img": "/posters/poster_25.png"
      },
      {
        "name": "Paws",
        "character": "The Tunnel Navigator",
        "img": "/posters/poster_33.png"
      },
      {
        "name": "Nibbles",
        "character": "The Biter",
        "img": "/posters/poster_30.png"
      },
      {
        "name": "Buster",
        "character": "The Wheel Runner",
        "img": "/posters/poster_29.png"
      }
    ],
    "director": "Greta Gerwig",
    "synopsis": "In a world where the wheel never stops turning, one hamster must face the ultimate challenge. Experience 'Planet Fluff' like never before in this epic sci-fi tale of survival, seeds, and late-night running.",
    "genres": [
      "Sci-Fi",
      "Adventure"
    ],
    "mood": [
      "Heartwarming",
      "Heartwarming"
    ],
    "trailer_concept": "[0:00-0:10] Wide panning shot of a neon-lit, futuristic cage. A glowing water bottle drips in slow motion. 'Planet Fluff' appears on screen.\n\n[0:10-0:20] Close-up of our majestic hamster hero looking out of a plastic tube into the vast unknown, heartwarming synth music building.\n\n[0:20-0:30] Rapid montage: running on a hyper-drive wheel, dodging laser pointers, and a final epic leap into the bedding. Fade to black."
  },
  "37": {
    "cast": [
      {
        "name": "Barnaby",
        "character": "The Mastermind",
        "img": "/posters/poster_23.png"
      },
      {
        "name": "Pip",
        "character": "The Escape Artist",
        "img": "/posters/poster_15.png"
      },
      {
        "name": "Buttercup",
        "character": "The Treat Thief",
        "img": "/posters/poster_28.png"
      },
      {
        "name": "Bean",
        "character": "The Seed Hoarder",
        "img": "/posters/poster_30.png"
      },
      {
        "name": "Oreo",
        "character": "The Hero",
        "img": "/posters/poster_2.png"
      },
      {
        "name": "Squeaks",
        "character": "The Cage Climber",
        "img": "/posters/poster_13.png"
      },
      {
        "name": "Teddy",
        "character": "The Biter",
        "img": "/posters/poster_23.png"
      },
      {
        "name": "Nugget",
        "character": "The Escape Artist",
        "img": "/posters/poster_26.png"
      },
      {
        "name": "Hazel",
        "character": "The Treat Thief",
        "img": "/posters/poster_38.png"
      },
      {
        "name": "Furball",
        "character": "The Treat Thief",
        "img": "/posters/poster_32.png"
      },
      {
        "name": "Cashew",
        "character": "The Treat Thief",
        "img": "/posters/poster_11.png"
      },
      {
        "name": "Nibbles",
        "character": "The Escape Artist",
        "img": "/posters/poster_31.png"
      }
    ],
    "director": "Wes Anderson",
    "synopsis": "In a world where the wheel never stops turning, one hamster must face the ultimate challenge. Experience 'The Cat Next Door' like never before in this epic thriller tale of survival, seeds, and late-night running.",
    "genres": [
      "Thriller",
      "Family"
    ],
    "mood": [
      "Furry",
      "Furry"
    ],
    "trailer_concept": "[0:00-0:10] Heartbeat sound effect. Pitch black. Suddenly, the cage door clicks open. The furry tension is palpable.\n\n[0:10-0:20] Fast cuts: A shadow of a house cat. The hamster stuffing cheeks with seeds. A frantic dash through the plastic tunnels.\n\n[0:20-0:30] An explosive slow-motion dive off the second level of the cage. Heavy bass drop. 'The Cat Next Door' slams onto the screen."
  },
  "38": {
    "cast": [
      {
        "name": "Chestnut",
        "character": "The Cage Climber",
        "img": "/posters/poster_3.png"
      },
      {
        "name": "Whiskers",
        "character": "The Seed Hoarder",
        "img": "/posters/poster_3.png"
      },
      {
        "name": "Mocha",
        "character": "The Hero",
        "img": "/posters/poster_19.png"
      },
      {
        "name": "Squeaks",
        "character": "The Tunnel Navigator",
        "img": "/posters/poster_23.png"
      },
      {
        "name": "Cheeks",
        "character": "The Squeaker",
        "img": "/posters/poster_40.png"
      },
      {
        "name": "Buster",
        "character": "The Mastermind",
        "img": "/posters/poster_41.png"
      },
      {
        "name": "Teddy",
        "character": "The Wheel Runner",
        "img": "/posters/poster_9.png"
      },
      {
        "name": "Pumpkin",
        "character": "The Villain",
        "img": "/posters/poster_7.png"
      },
      {
        "name": "Cashew",
        "character": "The Escape Artist",
        "img": "/posters/poster_8.png"
      },
      {
        "name": "Coco",
        "character": "The Seed Hoarder",
        "img": "/posters/poster_26.png"
      },
      {
        "name": "Buttercup",
        "character": "The Treat Thief",
        "img": "/posters/poster_31.png"
      },
      {
        "name": "Biscuit",
        "character": "The Sleeper",
        "img": "/posters/poster_10.png"
      },
      {
        "name": "Paws",
        "character": "The Wise Elder",
        "img": "/posters/poster_25.png"
      }
    ],
    "director": "Steven Spielberg",
    "synopsis": "In a world where the wheel never stops turning, one hamster must face the ultimate challenge. Experience 'Shadows in the Cage' like never before in this epic thriller tale of survival, seeds, and late-night running.",
    "genres": [
      "Thriller",
      "Animation"
    ],
    "mood": [
      "Fast-Paced",
      "Furry"
    ],
    "trailer_concept": "[0:00-0:10] Heartbeat sound effect. Pitch black. Suddenly, the cage door clicks open. The fast-paced tension is palpable.\n\n[0:10-0:20] Fast cuts: A shadow of a house cat. The hamster stuffing cheeks with seeds. A frantic dash through the plastic tunnels.\n\n[0:20-0:30] An explosive slow-motion dive off the second level of the cage. Heavy bass drop. 'Shadows in the Cage' slams onto the screen."
  },
  "39": {
    "cast": [
      {
        "name": "Barnaby",
        "character": "The Villain",
        "img": "/posters/poster_38.png"
      },
      {
        "name": "Buttercup",
        "character": "The Wise Elder",
        "img": "/posters/poster_23.png"
      },
      {
        "name": "Hazel",
        "character": "The Escape Artist",
        "img": "/posters/poster_20.png"
      },
      {
        "name": "Mocha",
        "character": "The Sidekick",
        "img": "/posters/poster_20.png"
      },
      {
        "name": "Squeaks",
        "character": "The Lookout",
        "img": "/posters/poster_1.png"
      },
      {
        "name": "Dusty",
        "character": "The Lookout",
        "img": "/posters/poster_12.png"
      },
      {
        "name": "Nugget",
        "character": "The Wheel Runner",
        "img": "/posters/poster_38.png"
      },
      {
        "name": "Paws",
        "character": "The Squeaker",
        "img": "/posters/poster_14.png"
      },
      {
        "name": "Oreo",
        "character": "The Tunnel Navigator",
        "img": "/posters/poster_3.png"
      },
      {
        "name": "Marshmallow",
        "character": "The Biter",
        "img": "/posters/poster_9.png"
      },
      {
        "name": "Chubby",
        "character": "The Treat Thief",
        "img": "/posters/poster_43.png"
      },
      {
        "name": "Sir Fluffs",
        "character": "The Seed Hoarder",
        "img": "/posters/poster_26.png"
      },
      {
        "name": "Coco",
        "character": "The Mastermind",
        "img": "/posters/poster_39.png"
      }
    ],
    "director": "Steven Spielberg",
    "synopsis": "In a world where the wheel never stops turning, one hamster must face the ultimate challenge. Experience 'Lost in the Tubes' like never before in this epic thriller tale of survival, seeds, and late-night running.",
    "genres": [
      "Thriller",
      "Family"
    ],
    "mood": [
      "Heartwarming",
      "Heartwarming"
    ],
    "trailer_concept": "[0:00-0:10] Heartbeat sound effect. Pitch black. Suddenly, the cage door clicks open. The heartwarming tension is palpable.\n\n[0:10-0:20] Fast cuts: A shadow of a house cat. The hamster stuffing cheeks with seeds. A frantic dash through the plastic tunnels.\n\n[0:20-0:30] An explosive slow-motion dive off the second level of the cage. Heavy bass drop. 'Lost in the Tubes' slams onto the screen."
  },
  "40": {
    "cast": [
      {
        "name": "Teddy",
        "character": "The Villain",
        "img": "/posters/poster_6.png"
      },
      {
        "name": "Mocha",
        "character": "The Tunnel Navigator",
        "img": "/posters/poster_33.png"
      },
      {
        "name": "Pumpkin",
        "character": "The Mastermind",
        "img": "/posters/poster_35.png"
      },
      {
        "name": "Snickers",
        "character": "The Hero",
        "img": "/posters/poster_22.png"
      },
      {
        "name": "Coco",
        "character": "The Cage Climber",
        "img": "/posters/poster_51.png"
      },
      {
        "name": "Oreo",
        "character": "The Lookout",
        "img": "/posters/poster_51.png"
      },
      {
        "name": "Bean",
        "character": "The Hero",
        "img": "/posters/poster_13.png"
      },
      {
        "name": "Squeaks",
        "character": "The Squeaker",
        "img": "/posters/poster_40.png"
      },
      {
        "name": "Paws",
        "character": "The Squeaker",
        "img": "/posters/poster_39.png"
      },
      {
        "name": "Furball",
        "character": "The Squeaker",
        "img": "/posters/poster_33.png"
      }
    ],
    "director": "Steven Spielberg",
    "synopsis": "In a world where the wheel never stops turning, one hamster must face the ultimate challenge. Experience 'Midnight Squeak' like never before in this epic thriller tale of survival, seeds, and late-night running.",
    "genres": [
      "Thriller",
      "Family"
    ],
    "mood": [
      "Intense",
      "Exciting"
    ],
    "trailer_concept": "[0:00-0:10] Heartbeat sound effect. Pitch black. Suddenly, the cage door clicks open. The intense tension is palpable.\n\n[0:10-0:20] Fast cuts: A shadow of a house cat. The hamster stuffing cheeks with seeds. A frantic dash through the plastic tunnels.\n\n[0:20-0:30] An explosive slow-motion dive off the second level of the cage. Heavy bass drop. 'Midnight Squeak' slams onto the screen."
  },
  "41": {
    "cast": [
      {
        "name": "Biscuit",
        "character": "The Tunnel Navigator",
        "img": "/posters/poster_7.png"
      },
      {
        "name": "Muffin",
        "character": "The Squeaker",
        "img": "/posters/poster_11.png"
      },
      {
        "name": "Waffles",
        "character": "The Tunnel Navigator",
        "img": "/posters/poster_18.png"
      },
      {
        "name": "Whiskers",
        "character": "The Lookout",
        "img": "/posters/poster_24.png"
      },
      {
        "name": "Coco",
        "character": "The Biter",
        "img": "/posters/poster_15.png"
      },
      {
        "name": "Oreo",
        "character": "The Mastermind",
        "img": "/posters/poster_22.png"
      },
      {
        "name": "Hazel",
        "character": "The Mastermind",
        "img": "/posters/poster_5.png"
      },
      {
        "name": "Sir Fluffs",
        "character": "The Wheel Runner",
        "img": "/posters/poster_29.png"
      }
    ],
    "director": "Greta Gerwig",
    "synopsis": "In a world where the wheel never stops turning, one hamster must face the ultimate challenge. Experience 'The Hand' like never before in this epic thriller tale of survival, seeds, and late-night running.",
    "genres": [
      "Thriller",
      "Animation"
    ],
    "mood": [
      "Squeaky",
      "Furry"
    ],
    "trailer_concept": "[0:00-0:10] Heartbeat sound effect. Pitch black. Suddenly, the cage door clicks open. The squeaky tension is palpable.\n\n[0:10-0:20] Fast cuts: A shadow of a house cat. The hamster stuffing cheeks with seeds. A frantic dash through the plastic tunnels.\n\n[0:20-0:30] An explosive slow-motion dive off the second level of the cage. Heavy bass drop. 'The Hand' slams onto the screen."
  },
  "default": {
    "cast": [
      {
        "name": "Unknown",
        "character": "Hamster",
        "img": "/posters/poster_1.png"
      }
    ],
    "director": "Unknown",
    "synopsis": "Pending vision extraction.",
    "genres": [
      "Unknown"
    ],
    "mood": [
      "Unknown"
    ],
    "trailer_concept": "No concept generated yet."
  }
};

function MovieDetail() {
      const { id } = useParams();
      const navigate = useNavigate();
      const [extractedData, setExtractedData] = React.useState(null);
      const [isPlaying, setIsPlaying] = React.useState(false);

      React.useEffect(() => {
        window.scrollTo(0, 0);
        setIsPlaying(false);
    
        // Simulate fetching from our new SQLite DB via an API
        fetch('/api/movies/' + id)
          .then(res => res.json())
          .then(data => setExtractedData(data))
          .catch(() => {
            setExtractedData(EXTRACTED_DATA.default);
          });
      }, [id]);

      if (!extractedData) return <div className="text-white pt-32 text-center text-2xl font-bold">Loading...</div>;

      const details = extractedData;
      const movieImg = details.img || '/posters_real/poster_real_1.png';

      return (
        <div className="min-h-screen bg-netflix-black text-white">
          <Navbar />
      
          {isPlaying ? (
            <div className="fixed inset-0 z-50 bg-black flex flex-col items-center justify-center">
              <button 
                onClick={() => setIsPlaying(false)}
                className="absolute top-8 left-8 text-white hover:text-gray-300 z-50 flex items-center gap-2"
              >
                <ArrowLeft className="w-6 h-6" /> Back
              </button>
          
              <div className="w-full max-w-6xl aspect-video bg-gray-900 rounded-lg overflow-hidden relative shadow-2xl border border-gray-800">
                 {extractedData.id ? (
                    <div className="absolute inset-0 flex items-center justify-center bg-black">
                       <video autoPlay loop controls className="w-full h-full object-cover z-0 relative">
                         <source src={`${import.meta.env.VITE_MEDIA_BASE || ""}/trailers/trailer_${extractedData.id}.mp4?v=${Date.now()}`} type="video/mp4" />
                         Your browser does not support the video tag.
                       </video>
                    </div>
                 ) : (
                   <div className="flex items-center justify-center h-full flex-col gap-4">
                     <Play className="w-16 h-16 text-gray-700" />
                     <p className="text-gray-500 font-medium">Trailer coming soon...</p>
                   </div>
                 )}
              </div>
            </div>
          ) : (
            <>
              {/* Background Blur Effect */}
              <div className="fixed inset-0 z-0">
                <img src={movieImg} alt="background blur" className="w-full h-full object-cover opacity-20 blur-3xl scale-110" />
                <div className="absolute inset-0 bg-netflix-black/80"></div>
              </div>

              <div className="pt-32 pb-20 px-4 md:px-12 max-w-6xl mx-auto relative z-10">
                <button onClick={() => navigate(-1)} className="mb-8 flex items-center gap-2 hover:text-gray-300 text-gray-400 transition-colors font-semibold">
                   <ArrowLeft className="w-5 h-5" /> Back to Browse
                </button>
            
                <div className="flex flex-col md:flex-row gap-12">
                  {/* Poster Column */}
                  <div className="w-full md:w-1/3 shrink-0">
                    <div className="rounded-xl overflow-hidden shadow-[0_0_40px_rgba(0,0,0,0.8)] border border-gray-800 relative group">
                      <img src={movieImg} alt={details.title} className="w-full h-auto object-cover" />
                      <div className="absolute inset-0 bg-black/40 opacity-0 group-hover:opacity-100 transition-opacity flex items-center justify-center">
                         <button onClick={() => setIsPlaying(true)} className="bg-netflix-red text-white rounded-full p-4 hover:scale-110 transition-transform shadow-lg">
                           <Play className="w-8 h-8 fill-current ml-1" />
                         </button>
                      </div>
                    </div>
                  </div>
              
                  {/* Info Column */}
                  <div className="w-full md:w-2/3 space-y-6">
                    <h1 className="text-4xl md:text-6xl font-bold tracking-tight">{details.title}</h1>
                
                    <div className="flex items-center gap-4 text-sm text-gray-400 font-bold">
                      <span className="text-green-500 font-extrabold text-base">98% Match</span>
                      <span>2026</span>
                      <span className="border border-gray-600 px-1.5 py-0.5 rounded text-xs text-gray-300">PG</span>
                      <span>1h 45m</span>
                      <span className="border border-gray-600 px-1.5 py-0.5 rounded text-xs text-gray-300">HD</span>
                    </div>
                
                    <p className="text-lg md:text-xl text-gray-200 leading-relaxed max-w-3xl">
                      {details.synopsis}
                    </p>
                
                    <div className="pt-6 border-t border-gray-800 mt-8">
                      <h3 className="text-gray-500 mb-4 font-semibold">Cast & Characters</h3>
                      <div className="flex gap-6 overflow-x-auto hide-scrollbar pb-4">
                        {(() => {
                          let castList = [];
                          if (Array.isArray(details.cast)) {
                            castList = details.cast;
                          } else if (typeof details.cast === 'string') {
                            try { castList = JSON.parse(details.cast); } catch(e) {}
                          }
                          return castList.map((actor, idx) => (
                            <div key={idx} className="flex flex-col items-center gap-2 flex-none w-24 text-center group cursor-pointer">
                              <div className="w-16 h-16 rounded-full overflow-hidden border-2 border-gray-700 shadow-md group-hover:border-netflix-red transition-colors bg-gray-800 flex items-center justify-center">
                                <img src={actor.img} alt={actor.name} className="w-full h-full object-cover text-transparent" 
                                     onError={(e) => { e.target.style.display = 'none'; e.target.parentNode.innerHTML = '<span class="text-xs text-gray-500">Processing...</span>'; }} />
                              </div>
                              <div>
                                <p className="text-gray-300 text-xs font-medium leading-tight group-hover:text-white transition-colors">{actor.name}</p>
                                <p className="text-gray-500 text-[10px] leading-tight mt-0.5">{actor.character}</p>
                              </div>
                            </div>
                          ));
                        })()}
                      </div>
                    </div>
                
                    <div className="text-sm md:text-base text-gray-400 space-y-3 pt-4 border-t border-gray-800">
                      <p className="hidden"><span className="text-gray-500 w-32 inline-block shrink-0">Cast:</span></p>
                      <p className="flex"><span className="text-gray-500 w-32 inline-block shrink-0">Director:</span> <span className="text-gray-300">{details.director || "Unknown"}</span></p>
                      <p className="flex"><span className="text-gray-500 w-32 inline-block shrink-0">Genres:</span> <span>{(details.genres || []).map((g, i, arr) => <React.Fragment key={i}><span className="text-white hover:underline cursor-pointer">{g}</span>{i < arr.length - 1 ? ', ' : ''}</React.Fragment>)}</span></p>
                      <p className="flex"><span className="text-gray-500 w-32 inline-block shrink-0">This movie is:</span> <span>{(details.mood || []).map((m, i, arr) => <React.Fragment key={i}><span className="text-white hover:underline cursor-pointer">{m}</span>{i < arr.length - 1 ? ', ' : ''}</React.Fragment>)}</span></p>
                    </div>
                    
                    {/* Inspired By Section */}
                    <div className="text-sm md:text-base text-gray-400 space-y-3 pt-4 border-t border-gray-800">
                      <p className="flex items-center">
                        <span className="text-yellow-500 w-32 inline-block shrink-0 font-semibold uppercase tracking-wider text-xs">Inspired By:</span>
                        <span className="text-white italic">{details.inspiration || "Original Cinematic Masterpiece"}</span>
                      </p>
                    </div>

                    <div className="flex gap-4 pt-8">
                      <button onClick={() => setIsPlaying(true)} className="flex items-center justify-center gap-2 bg-white text-black px-8 py-3 rounded hover:bg-white/80 transition-colors font-bold text-lg md:text-xl min-w-[140px]">
                         <Play className="w-6 h-6 fill-current" /> Play
                      </button>
                      <button className="flex items-center justify-center gap-2 bg-gray-600/70 text-white px-8 py-3 rounded hover:bg-gray-600/50 transition-colors font-bold text-lg md:text-xl backdrop-blur-sm min-w-[140px]" title="My List (Coming Soon)">
                         <Plus className="w-6 h-6" /> My List
                      </button>
                    </div>
                  </div>
                </div>
              </div>
            </>
          )}
        </div>
      );
    }

function VoiceDetail() {
  const { id } = useParams();
  const navigate = useNavigate();
  const [movie, setMovie] = React.useState(null);

  React.useEffect(() => {
    window.scrollTo(0, 0);
    fetch('/api/movies/' + id)
      .then(res => res.json())
      .then(data => setMovie(data))
      .catch(() => setMovie({ title: "Unknown", img: "/posters_real/poster_real_1.png" }));
  }, [id]);

  if (!movie) return <div className="text-white pt-32 text-center text-2xl font-bold">Voiceover not found</div>;

  return (
    <div className="min-h-screen bg-netflix-black text-white flex flex-col items-center justify-center p-8">
      <Navbar />
      <div className="z-10 relative bg-gray-900/80 p-12 rounded-2xl border border-gray-800 shadow-2xl max-w-2xl w-full text-center mt-20">
        <button onClick={() => navigate(-1)} className="absolute top-6 left-6 flex items-center gap-2 hover:text-gray-300 text-gray-400 transition-colors font-semibold">
           <ArrowLeft className="w-5 h-5" /> Back
        </button>
        <div className="w-32 h-32 mx-auto mb-6 rounded-full overflow-hidden border-4 border-netflix-red shadow-[0_0_20px_rgba(229,9,20,0.5)]">
           <img src={movie.img || movie.poster_filename} alt={movie.title} className="w-full h-full object-cover" />
        </div>
        <h1 className="text-3xl font-bold mb-2">{movie.title}</h1>
        <p className="text-gray-400 mb-8 font-medium">Original Voiceover Generation</p>
        
        <div className="w-full bg-black/50 p-6 rounded-xl border border-gray-800 flex justify-center custom-audio">
           {movie.id ? (
             <audio controls autoPlay className="w-full outline-none">
                <source src={`/voiceovers/${movie.id}.mp3?v=${Date.now()}`} type="audio/mpeg" />
                Your browser does not support the audio element.
             </audio>
           ) : (
             <p className="text-gray-500 font-medium">Voiceover coming soon...</p>
           )}
        </div>
      </div>
      
      {/* Background Blur */}
      <div className="fixed inset-0 z-0 pointer-events-none">
        <img src={movie.img || movie.poster_filename} alt="background blur" className="w-full h-full object-cover opacity-20 blur-3xl scale-110" />
        <div className="absolute inset-0 bg-netflix-black/80"></div>
      </div>
    </div>
  );
}

export default function App() {
  return (
    <Router>
      <div className="bg-netflix-black text-white min-h-screen font-sans overflow-x-hidden selection:bg-netflix-red selection:text-white">
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/movie/:id" element={<MovieDetail />} />
          <Route path="/voice/:id" element={<VoiceDetail />} />
        </Routes>
      </div>
    </Router>
  );
}
