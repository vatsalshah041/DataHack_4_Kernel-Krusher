// import logo from './logo.svg';
import './App.css';
import Home from './components/Home';
// import { Navbar } from './components/Navbar';
const { Navbar } = require('./components/Navbar'); // Replace with the actual path to your Navbar component

function App() {
  return (
    <div style={{backgroundColor:"#ffe28c"}}>
      {/* <Navbar/> */}
      <Home/>
    </div>
  );
}

export default App;
